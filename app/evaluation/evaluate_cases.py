import json
from pathlib import Path

from app.security.report_builder import build_audit_report
from app.tools.slither_tool import run_slither_analysis


CASES = [
    ("safe.sol", set()),
    ("integer_overflow.sol", {"SWC-101"}),
    ("reentrancy.sol", {"SWC-107"}),
    ("invalid.sol", set()),
]


def evaluate_case(filename: str, expected_ids: set[str]) -> dict[str, object]:
    contracts_dir = Path(__file__).parents[2] / "contracts" / "samples"
    source_code = (contracts_dir / filename).read_text(encoding="utf-8")
    report = build_audit_report(source_code, filename)
    slither_result = run_slither_analysis.invoke(
        {"source_code": source_code, "contract_name": filename}
    )
    actual_ids = sorted(
        finding.id for finding in report.vulnerabilities if finding.id.startswith("SWC-")
    )
    passed = expected_ids.issubset(set(actual_ids))
    if not expected_ids:
        if filename == "invalid.sol":
            passed = not actual_ids and slither_result["status"] == "compile_error"
        else:
            passed = not actual_ids
    return {
        "case": filename,
        "passed": passed,
        "expected_vulnerabilities": sorted(expected_ids),
        "actual_vulnerabilities": actual_ids,
        "risk_level": report.risk_level,
        "slither_status": slither_result["status"],
        "tool_trace": report.tool_trace,
    }


def main() -> None:
    results = [evaluate_case(filename, expected_ids) for filename, expected_ids in CASES]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    if not all(item["passed"] for item in results):
        raise SystemExit("evaluation_failed")
    print(f"evaluation_summary=passed:{len(results)}/{len(results)}")


if __name__ == "__main__":
    main()
