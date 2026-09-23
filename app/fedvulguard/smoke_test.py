from pathlib import Path

from app.tools.fedvulguard_tool import run_fedvulguard_analysis


def main() -> None:
    source = Path("contracts/samples/reentrancy.sol").read_text(encoding="utf-8")
    result = run_fedvulguard_analysis.invoke({"source_code": source})
    labels = {prediction["label"] for prediction in result["predictions"]}
    if result["status"] != "success":
        raise RuntimeError("FedVulGuard-compatible baseline 未完成")
    if "SWC-107" not in labels:
        raise RuntimeError("基线未检测到 SWC-107")
    print(result)


if __name__ == "__main__":
    main()
