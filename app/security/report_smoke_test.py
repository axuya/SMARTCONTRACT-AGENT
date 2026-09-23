import json
from pathlib import Path

from app.security.report_builder import build_audit_report


def main() -> None:
    source_path = Path("contracts/samples/reentrancy.sol")
    report = build_audit_report(
        source_path.read_text(encoding="utf-8"), source_path.name
    )
    if report.risk_level != "high":
        raise RuntimeError("结构化报告没有正确计算 high 风险等级")
    if not any(item.id == "SWC-107" for item in report.vulnerabilities):
        raise RuntimeError("结构化报告缺少 SWC-107")
    print(json.dumps(report.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

