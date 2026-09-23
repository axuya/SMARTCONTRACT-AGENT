from pathlib import Path

from app.agent.multi_tool_agent import MultiToolAuditAgent


def main() -> None:
    source_path = Path("contracts/samples/reentrancy.sol")
    result = MultiToolAuditAgent().run(
        source_code=source_path.read_text(encoding="utf-8"),
        contract_name=source_path.name,
    )
    tool_names = [item["tool"] for item in result["tool_trace"]]
    print(f"tool_trace={result['tool_trace']}")
    print(f"tool_names={tool_names}")
    print("final_answer=")
    print(result["final_answer"])
    required_tools = {
        "run_slither_analysis",
        "run_fedvulguard_analysis",
        "search_security_knowledge",
    }
    if not required_tools.issubset(set(tool_names)):
        raise RuntimeError(f"多 Tool Agent 未调用全部工具: {required_tools - set(tool_names)}")


if __name__ == "__main__":
    main()

