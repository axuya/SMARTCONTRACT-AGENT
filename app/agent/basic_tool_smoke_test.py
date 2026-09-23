import json

from langchain_core.messages import HumanMessage, ToolMessage

from app.config import get_settings
from app.llm.client import build_chat_model
from app.tools.basic_contract_tool import get_contract_basic_info


CONTRACT_SOURCE = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Vault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "transfer failed");
        balances[msg.sender] -= amount;
    }
}
"""


def main() -> None:
    model = build_chat_model(get_settings())
    model_with_tools = model.bind_tools([get_contract_basic_info])
    user_message = HumanMessage(
        content=(
            "你是智能合约安全分析助手。必须调用 get_contract_basic_info，"
            "然后根据工具结果回答。请分析下面的 Solidity 合约基础结构。\n\n"
            f"```solidity\n{CONTRACT_SOURCE}\n```"
        )
    )

    first_response = model_with_tools.invoke([user_message])
    tool_calls = first_response.tool_calls
    if not tool_calls:
        raise RuntimeError("模型没有返回 tool_calls，Tool Calling 验证失败")

    tool_messages = []
    for tool_call in tool_calls:
        if tool_call["name"] != get_contract_basic_info.name:
            raise RuntimeError(f"模型请求了未注册的工具: {tool_call['name']}")
        tool_result = get_contract_basic_info.invoke(tool_call["args"])
        tool_messages.append(
            ToolMessage(
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
                content=json.dumps(tool_result, ensure_ascii=False),
            )
        )

    final_response = model_with_tools.invoke(
        [user_message, first_response, *tool_messages]
    )

    print(f"tool_message_count={len(tool_messages)}")
    for message in tool_messages:
        print(f"tool_name={message.name}")
        print(f"tool_result={message.content}")
    print("final_answer=")
    print(final_response.content)


if __name__ == "__main__":
    main()
