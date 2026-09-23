import logging

from fastapi import APIRouter, HTTPException

from app.api.schemas import AuditRequest
from app.api.schemas import AgentAuditResponse
from app.agent.multi_tool_agent import MultiToolAuditAgent
from app.agent.structured_synthesizer import StructuredReportSynthesizer
from app.security.report_builder import build_audit_report
from app.security.report_models import AuditReport


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/audit", response_model=AuditReport)
def audit_contract(request: AuditRequest) -> AuditReport:
    try:
        return build_audit_report(request.source_code, request.contract_name)
    except Exception as exc:
        logger.exception("Audit failed for contract %s", request.contract_name)
        raise HTTPException(status_code=500, detail="Audit execution failed") from exc


@router.post("/audit-agent", response_model=AgentAuditResponse)
def audit_contract_with_agent(request: AuditRequest) -> AgentAuditResponse:
    try:
        agent_result = MultiToolAuditAgent().run(
            source_code=request.source_code,
            contract_name=request.contract_name,
        )
        report = build_audit_report(request.source_code, request.contract_name)
        structured_report = StructuredReportSynthesizer().synthesize(
            report, agent_result["final_answer"]
        )
        return AgentAuditResponse(
            report=structured_report,
            agent_analysis=agent_result["final_answer"],
            agent_tool_trace=agent_result["tool_trace"],
        )
    except Exception as exc:
        logger.exception("Agent audit failed for contract %s", request.contract_name)
        raise HTTPException(status_code=500, detail="Agent audit execution failed") from exc
