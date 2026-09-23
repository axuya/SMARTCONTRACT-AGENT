from pathlib import Path

from app.agent.multi_tool_agent import MultiToolAuditAgent
from app.agent.structured_synthesizer import StructuredReportSynthesizer
from app.security.report_builder import build_audit_report


def main() -> None:
    source_path = Path("contracts/samples/reentrancy.sol")
    source = source_path.read_text(encoding="utf-8")
    agent_result = MultiToolAuditAgent().run(source, source_path.name)
    deterministic_report = build_audit_report(source, source_path.name)
    structured_report = StructuredReportSynthesizer().synthesize(
        deterministic_report, agent_result["final_answer"]
    )
    print(f"report_type={type(structured_report).__name__}")
    print(f"risk_level={structured_report.risk_level}")
    print(f"vulnerability_ids={[item.id for item in structured_report.vulnerabilities]}")
    if not any(item.id == "SWC-107" for item in structured_report.vulnerabilities):
        raise RuntimeError("Structured Output 丢失 SWC-107")


if __name__ == "__main__":
    main()

