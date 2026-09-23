from typing import Any

from app.agent.audit_workflow import AuditWorkflow
from app.security.report_models import AuditReport, VulnerabilityFinding


SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def _normalise_severity(value: str) -> str:
    value = value.lower()
    return value if value in SEVERITY_RANK else "low"


def _slither_confidence(value: str) -> float:
    return {"high": 0.90, "medium": 0.75, "low": 0.55}.get(value.lower(), 0.50)


def _location_from_detector(detector: dict[str, Any], contract_name: str) -> str:
    lines = []
    for element in detector.get("elements", []):
        lines.extend(element.get("source_mapping", {}).get("lines", []))
    if lines:
        return f"{contract_name}:L{min(lines)}"
    return contract_name


def _slither_finding(detector: dict[str, Any], contract_name: str) -> VulnerabilityFinding:
    check = detector.get("check", "unknown")
    if check.startswith("reentrancy"):
        vulnerability_id = "SWC-107"
        vulnerability_type = "reentrancy"
        recommendation = "Apply Checks-Effects-Interactions or a reviewed reentrancy guard."
    elif "integer" in check or "underflow" in check or "overflow" in check:
        vulnerability_id = "SWC-101"
        vulnerability_type = "integer overflow or underflow"
        recommendation = "Use checked arithmetic and validate numeric bounds."
    else:
        vulnerability_id = check
        vulnerability_type = check
        recommendation = "Review the Slither detector details and apply the documented mitigation."

    return VulnerabilityFinding(
        id=vulnerability_id,
        type=vulnerability_type,
        severity=_normalise_severity(detector.get("impact", "low")),
        location=_location_from_detector(detector, contract_name),
        evidence=detector.get("description", ""),
        confidence=_slither_confidence(detector.get("confidence", "low")),
        explanation=detector.get("description", "Slither reported this detector result."),
        recommendation=recommendation,
        sources=["slither"],
    )


def _baseline_finding(prediction: dict[str, Any], contract_name: str) -> VulnerabilityFinding:
    mapping = {
        "SWC-107": ("reentrancy", "Apply Checks-Effects-Interactions or a reviewed reentrancy guard."),
        "SWC-101": ("integer overflow or underflow", "Use checked arithmetic and validate numeric bounds."),
    }
    vulnerability_type, recommendation = mapping.get(
        prediction["label"], (prediction["label"], "Review the evidence and apply a verified mitigation.")
    )
    return VulnerabilityFinding(
        id=prediction["label"],
        type=vulnerability_type,
        severity="high" if prediction["label"] == "SWC-107" else "medium",
        location=contract_name,
        evidence=prediction.get("evidence", ""),
        confidence=float(prediction.get("confidence", 0.0)),
        explanation="FedVulGuard-compatible local baseline detected this pattern.",
        recommendation=recommendation,
        sources=["fedvulguard-compatible-baseline"],
    )


def _merge_findings(findings: list[VulnerabilityFinding]) -> list[VulnerabilityFinding]:
    merged: dict[str, VulnerabilityFinding] = {}
    for finding in findings:
        current = merged.get(finding.id)
        if current is None:
            merged[finding.id] = finding
            continue
        current.sources = sorted(set(current.sources + finding.sources))
        current.confidence = max(current.confidence, finding.confidence)
        if finding.evidence and finding.evidence not in current.evidence:
            current.evidence = f"{current.evidence}\n{finding.evidence}"
    return list(merged.values())


def build_audit_report(source_code: str, contract_name: str = "Contract.sol") -> AuditReport:
    workflow_result = AuditWorkflow().run(source_code, contract_name)
    slither_execution = next(item for item in workflow_result.tool_executions if item.tool == "slither")
    baseline_execution = next(item for item in workflow_result.tool_executions if item.tool == "fedvulguard")

    slither_detectors = slither_execution.result.get("detectors", [])
    baseline_predictions = baseline_execution.result.get("predictions", [])
    findings = [_slither_finding(item, contract_name) for item in slither_detectors]
    findings.extend(_baseline_finding(item, contract_name) for item in baseline_predictions)
    findings = _merge_findings(findings)

    risk_level = "low"
    if findings:
        risk_level = max(findings, key=lambda item: SEVERITY_RANK[item.severity]).severity
    summary = (
        f"发现 {len(findings)} 个合并后的安全发现，最高风险等级为 {risk_level}."
        if findings
        else "当前工具未发现明确的安全问题。"
    )
    return AuditReport(
        contract_name=contract_name,
        risk_level=risk_level,
        summary=summary,
        vulnerabilities=findings,
        static_analysis=[
            {
                "check": item.get("check"),
                "impact": item.get("impact"),
                "confidence": item.get("confidence"),
            }
            for item in slither_detectors
        ],
        model_analysis=baseline_predictions,
        knowledge_references=workflow_result.knowledge_references,
        tool_trace=[
            {"tool": item.tool, "status": item.status}
            for item in workflow_result.tool_executions
        ],
    )

