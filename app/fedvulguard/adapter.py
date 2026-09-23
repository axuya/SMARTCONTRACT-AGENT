import re
from typing import Protocol

from pydantic import BaseModel, Field


class FedVulGuardPrediction(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str = ""


class FedVulGuardResult(BaseModel):
    status: str
    predictions: list[FedVulGuardPrediction] = Field(default_factory=list)
    message: str = ""
    model_name: str = "fedvulguard-compatible-baseline"
    implementation_type: str = "rule_based_baseline"


class FedVulGuardAdapter(Protocol):
    def predict(self, source_code: str) -> FedVulGuardResult:
        ...


class FedVulGuardBaselineAdapter:
    """Small local baseline that keeps the FedVulGuard Tool contract runnable."""

    def predict(self, source_code: str) -> FedVulGuardResult:
        if not source_code.strip():
            return FedVulGuardResult(
                status="error",
                message="Solidity source code is empty",
            )

        lines = source_code.splitlines()
        predictions: list[FedVulGuardPrediction] = []

        external_call_lines = [
            index + 1
            for index, line in enumerate(lines)
            if re.search(r"\.(call|send|transfer)\s*(?:\{|\()", line)
        ]
        state_update_lines = [
            index + 1
            for index, line in enumerate(lines)
            if re.search(r"\-=|\+=|--|\+\+", line)
        ]
        if external_call_lines and any(
            update_line > external_call_lines[0] for update_line in state_update_lines
        ):
            predictions.append(
                FedVulGuardPrediction(
                    label="SWC-107",
                    confidence=0.82,
                    evidence=(
                        f"External call detected near line {external_call_lines[0]} "
                        "before a later state update."
                    ),
                )
            )

        old_solidity_version = re.search(
            r"pragma\s+solidity\s+\^?0\.([0-7])\.", source_code
        )
        unchecked_arithmetic = "unchecked" in source_code and bool(
            re.search(r"\b\w+\s*(\+=|\-=|\+\+|--)", source_code)
        )
        if old_solidity_version or unchecked_arithmetic:
            reason = (
                "Solidity version is below 0.8.0"
                if old_solidity_version
                else "Unchecked arithmetic pattern detected"
            )
            predictions.append(
                FedVulGuardPrediction(
                    label="SWC-101",
                    confidence=0.76,
                    evidence=reason,
                )
            )

        return FedVulGuardResult(
            status="success",
            predictions=predictions,
            message="Local FedVulGuard-compatible baseline analysis completed.",
        )
