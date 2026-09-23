from langchain_core.tools import tool

from app.fedvulguard.adapter import FedVulGuardBaselineAdapter


@tool
def run_fedvulguard_analysis(source_code: str) -> dict[str, object]:
    """Run the local FedVulGuard-compatible baseline detector."""
    result = FedVulGuardBaselineAdapter().predict(source_code)
    return result.model_dump()
