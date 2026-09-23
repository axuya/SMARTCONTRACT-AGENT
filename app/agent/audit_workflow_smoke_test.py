from pathlib import Path

from app.agent.audit_workflow import AuditWorkflow


def main() -> None:
    source_path = Path("contracts/samples/reentrancy.sol")
    result = AuditWorkflow().run(
        source_code=source_path.read_text(encoding="utf-8"),
        contract_name=source_path.name,
    )
    if result.status != "preflight_completed":
        raise RuntimeError("统一审计工作流未完成")
    if not any(item.tool == "slither" for item in result.tool_executions):
        raise RuntimeError("工作流缺少 Slither 执行记录")
    if not any(item.status == "success" and item.tool == "fedvulguard" for item in result.tool_executions):
        raise RuntimeError("工作流没有正确执行 FedVulGuard-compatible baseline")
    if not any(item["source"] == "swc-107.md" for item in result.knowledge_references):
        raise RuntimeError("工作流知识检索未命中 SWC-107")

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
