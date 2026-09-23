import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from app.config import get_settings
from app.llm.client import build_chat_model
from app.tools.fedvulguard_tool import run_fedvulguard_analysis
from app.tools.rag_tool import search_security_knowledge
from app.tools.slither_tool import run_slither_analysis


class MultiToolAuditAgent:
    def __init__(self, max_iterations: int = 6) -> None:
        self.model = build_chat_model(get_settings())
        self.tools = [
            run_slither_analysis,
            run_fedvulguard_analysis,
            search_security_knowledge,
        ]
        self.tool_map = {tool.name: tool for tool in self.tools}
        self.max_iterations = max_iterations

    def run(self, source_code: str, contract_name: str = "Contract.sol") -> dict[str, Any]:
        model_with_tools = self.model.bind_tools(self.tools)
        messages = [
            SystemMessage(
                content=(
                    "你是智能合约安全审计 Agent。必须使用工具完成审计，不要凭空编造检测结果。"
                    "对于用户提供的 Solidity 源码，至少调用 Slither、FedVulGuard-compatible baseline，"
                    "并根据检测结果调用 security knowledge RAG。最后用中文总结工具真实返回的结果。"
                )
            ),
            HumanMessage(
                content=(
                    f"请审计合约 {contract_name}，并说明每个工具的结果。\n\n"
                    f"```solidity\n{source_code}\n```"
                )
            ),
        ]
        trace: list[dict[str, str]] = []

        for _ in range(self.max_iterations):
            response = model_with_tools.invoke(messages)
            messages.append(response)
            if not response.tool_calls:
                return {
                    "final_answer": response.content,
                    "tool_trace": trace,
                    "message_count": len(messages),
                }

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool = self.tool_map.get(tool_name)
                if tool is None:
                    raise RuntimeError(f"模型请求了未注册工具: {tool_name}")

                arguments = dict(tool_call.get("args", {}))
                if tool_name == run_slither_analysis.name:
                    arguments.setdefault("contract_name", contract_name)
                tool_result = tool.invoke(arguments)
                trace_item = {
                    "tool": tool_name,
                    "status": str(tool_result.get("status", "success"))
                    if isinstance(tool_result, dict)
                    else "success",
                }
                if isinstance(tool_result, dict):
                    for key in ("error_type", "message", "return_code", "detector_count"):
                        if key in tool_result:
                            trace_item[key] = str(tool_result[key])[:500]
                trace.append(trace_item)
                messages.append(
                    ToolMessage(
                        name=tool_name,
                        tool_call_id=tool_call["id"],
                        content=json.dumps(tool_result, ensure_ascii=False),
                    )
                )

        raise RuntimeError("Agent exceeded maximum Tool Calling iterations")
