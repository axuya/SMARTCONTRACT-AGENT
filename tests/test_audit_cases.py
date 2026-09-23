from pathlib import Path

import pytest

from app.security.report_builder import build_audit_report
from app.tools.slither_tool import run_slither_analysis


CONTRACTS_DIR = Path(__file__).parents[1] / "contracts" / "samples"


@pytest.mark.parametrize(
    ("filename", "expected_ids"),
    [
        ("safe.sol", set()),
        ("integer_overflow.sol", {"SWC-101"}),
        ("reentrancy.sol", {"SWC-107"}),
    ],
)
def test_expected_vulnerability_detection(filename: str, expected_ids: set[str]) -> None:
    source = (CONTRACTS_DIR / filename).read_text(encoding="utf-8")
    report = build_audit_report(source, filename)
    actual_ids = {finding.id for finding in report.vulnerabilities if finding.id.startswith("SWC-")}
    assert expected_ids.issubset(actual_ids)
    if not expected_ids:
        assert not actual_ids


def test_invalid_solidity_returns_structured_compile_error() -> None:
    source = (CONTRACTS_DIR / "invalid.sol").read_text(encoding="utf-8")
    result = run_slither_analysis.invoke(
        {"source_code": source, "contract_name": "invalid.sol"}
    )
    assert result["status"] == "compile_error"
    assert result["detectors"] == []

