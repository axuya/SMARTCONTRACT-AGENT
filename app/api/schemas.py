from pydantic import BaseModel, Field

from app.security.report_models import AuditReport


class AuditRequest(BaseModel):
    source_code: str = Field(min_length=1)
    contract_name: str = Field(default="Contract.sol", min_length=1)


class AgentAuditResponse(BaseModel):
    report: AuditReport
    agent_analysis: str
    agent_tool_trace: list[dict[str, str]]
