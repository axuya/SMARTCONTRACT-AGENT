from typing import Any

from pydantic import BaseModel, Field


class ToolExecution(BaseModel):
    tool: str
    status: str
    result: dict[str, Any] = Field(default_factory=dict)


class AuditWorkflowResult(BaseModel):
    status: str
    contract_name: str
    tool_executions: list[ToolExecution]
    knowledge_references: list[dict[str, Any]] = Field(default_factory=list)


class VulnerabilityFinding(BaseModel):
    id: str
    type: str
    severity: str
    location: str
    evidence: str
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
    recommendation: str
    sources: list[str] = Field(default_factory=list)


class AuditReport(BaseModel):
    contract_name: str
    risk_level: str
    summary: str
    vulnerabilities: list[VulnerabilityFinding] = Field(default_factory=list)
    static_analysis: list[dict[str, Any]] = Field(default_factory=list)
    model_analysis: list[dict[str, Any]] = Field(default_factory=list)
    knowledge_references: list[dict[str, Any]] = Field(default_factory=list)
    tool_trace: list[dict[str, str]] = Field(default_factory=list)
