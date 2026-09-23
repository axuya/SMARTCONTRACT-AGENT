from app.security.report_models import AuditWorkflowResult, ToolExecution
from app.tools.fedvulguard_tool import run_fedvulguard_analysis
from app.tools.rag_tool import search_security_knowledge
from app.tools.slither_tool import run_slither_analysis


class AuditWorkflow:
    """Run the currently available audit tools and collect one audit context."""

    def run(self, source_code: str, contract_name: str = "Contract.sol") -> AuditWorkflowResult:
        slither_result = run_slither_analysis.invoke(
            {
                "source_code": source_code,
                "contract_name": contract_name,
                "timeout_seconds": 30,
            }
        )
        fedvulguard_result = run_fedvulguard_analysis.invoke(
            {"source_code": source_code}
        )

        detector_names = [
            detector.get("check", "")
            for detector in slither_result.get("detectors", [])
        ]
        knowledge_query = (
            "smart contract security vulnerabilities and remediation "
            + " ".join(detector_names)
        )
        knowledge_results = search_security_knowledge.invoke(
            {"query": knowledge_query}
        )

        executions = [
            ToolExecution(
                tool="slither",
                status=str(slither_result.get("status", "unknown")),
                result=slither_result,
            ),
            ToolExecution(
                tool="fedvulguard",
                status=str(fedvulguard_result.get("status", "unknown")),
                result=fedvulguard_result,
            ),
            ToolExecution(
                tool="rag_security_knowledge",
                status="success",
                result={"result_count": len(knowledge_results)},
            ),
        ]
        return AuditWorkflowResult(
            status="preflight_completed",
            contract_name=contract_name,
            tool_executions=executions,
            knowledge_references=knowledge_results,
        )

