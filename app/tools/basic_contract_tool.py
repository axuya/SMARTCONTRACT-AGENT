import re

from langchain_core.tools import tool


@tool
def get_contract_basic_info(source_code: str) -> dict[str, object]:
    """Analyze basic structural information from Solidity source code."""
    contract_names = re.findall(r"\bcontract\s+([A-Za-z_][A-Za-z0-9_]*)", source_code)
    function_names = re.findall(
        r"\bfunction\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", source_code
    )
    external_call_patterns = [
        r"\.call\s*(?:\{|\()",
        r"\.send\s*\(",
        r"\.transfer\s*\(",
    ]
    external_call_detected = any(
        re.search(pattern, source_code) for pattern in external_call_patterns
    )

    return {
        "line_count": len(source_code.splitlines()),
        "contract_names": contract_names,
        "function_names": function_names,
        "function_count": len(function_names),
        "external_call_detected": external_call_detected,
    }
