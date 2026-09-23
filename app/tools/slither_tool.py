import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from langchain_core.tools import tool


def _resolve_executable(env_name: str, executable_name: str) -> str | None:
    configured_path = os.getenv(env_name, "").strip()
    if configured_path:
        configured = Path(configured_path).expanduser()
        if configured.is_file() and configured.stat().st_mode & 0o111:
            return str(configured)

    discovered = shutil.which(executable_name)
    if discovered:
        return discovered

    candidates = [
        Path.home() / f"miniconda3/bin/{executable_name}",
        Path.home() / f"miniforge3/bin/{executable_name}",
        Path.home() / f".local/bin/{executable_name}",
        Path(f"/opt/homebrew/bin/{executable_name}"),
        Path(f"/usr/local/bin/{executable_name}"),
    ]
    for candidate in candidates:
        if candidate.is_file() and candidate.stat().st_mode & 0o111:
            return str(candidate)
    return None


def _resolve_slither_path() -> str | None:
    return _resolve_executable("SLITHER_PATH", "slither")


def _resolve_solc_path() -> str | None:
    return _resolve_executable("SOLC_PATH", "solc")


@tool
def run_slither_analysis(
    source_code: str,
    contract_name: str = "Contract.sol",
    timeout_seconds: int = 30,
) -> dict[str, object]:
    """Run Slither on Solidity source code and return structured detector results."""
    slither_path = _resolve_slither_path()
    if slither_path is None:
        return {
            "status": "error",
            "error_type": "slither_not_found",
            "message": "Slither executable was not found in PATH or known installation paths",
            "detectors": [],
        }
    solc_path = _resolve_solc_path()

    if not source_code.strip():
        return {
            "status": "error",
            "error_type": "empty_source_code",
            "message": "Solidity source code is empty",
            "detectors": [],
        }

    safe_filename = Path(contract_name).name or "Contract.sol"
    if not safe_filename.endswith(".sol"):
        safe_filename += ".sol"

    with tempfile.TemporaryDirectory(prefix="smartcontract-slither-") as temp_dir:
        source_path = Path(temp_dir) / safe_filename
        source_path.write_text(source_code, encoding="utf-8")
        command = [slither_path, str(source_path), "--json", "-"]
        if solc_path:
            command.extend(["--solc", solc_path])

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error_type": "timeout",
                "message": f"Slither exceeded {timeout_seconds} seconds",
                "detectors": [],
            }
        except OSError as exc:
            return {
                "status": "error",
                "error_type": "process_start_failed",
                "message": str(exc),
                "detectors": [],
            }

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {
            "status": "compile_error" if completed.returncode else "invalid_output",
            "error_type": "slither_json_parse_failed",
            "message": completed.stderr[-2000:] or completed.stdout[-2000:],
            "detectors": [],
        }

    results = payload.get("results", {})
    detectors = results.get("detectors", [])
    return {
        "status": "success" if completed.returncode == 0 or detectors else "analysis_completed_with_errors",
        "return_code": completed.returncode,
        "detector_count": len(detectors),
        "detectors": detectors,
        "compilation_stderr": completed.stderr[-2000:],
    }
