import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.llm.client import build_chat_model
from app.security.report_models import AuditReport


class StructuredReportSynthesizer:
    def __init__(self) -> None:
        # 百炼的 OpenAI 兼容接口对 response_format=json_schema 的返回形态
        # 可能出现单元素数组；使用 function_calling 可以让 LangChain 从
        # tool arguments 中直接解析 Pydantic 对象。
        self.model = build_chat_model(get_settings()).with_structured_output(
            AuditReport,
            method="function_calling",
        )

    def synthesize(self, report: AuditReport, agent_analysis: str) -> AuditReport:
        source_report = json.dumps(report.model_dump(), ensure_ascii=False, indent=2)
        return self.model.invoke(
            [
                SystemMessage(
                    content=(
                        "你是智能合约安全审计报告整理器。必须严格依据给定的确定性检测结果和 Agent 分析，"
                        "输出符合 AuditReport Schema 的结构化对象。不要新增工具没有检测到的漏洞，"
                        "不要修改工具证据中的事实。可以压缩解释和修复建议，但必须保留漏洞 ID、风险等级、"
                        "位置、置信度、工具来源和知识库引用。"
                    )
                ),
                HumanMessage(
                    content=(
                        "下面是确定性审计报告：\n"
                        f"{source_report}\n\n"
                        "下面是 Agent 分析：\n"
                        f"{agent_analysis[:12000]}"
                    )
                ),
            ]
        )
