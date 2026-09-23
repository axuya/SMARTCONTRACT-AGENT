from pathlib import Path

from app.tools.slither_tool import run_slither_analysis


def main() -> None:
    source_path = Path("contracts/samples/reentrancy.sol")
    result = run_slither_analysis.invoke(
        {
            "source_code": source_path.read_text(encoding="utf-8"),
            "contract_name": source_path.name,
            "timeout_seconds": 30,
        }
    )
    print(f"status={result['status']}")
    print(f"detector_count={result.get('detector_count', 0)}")
    for detector in result.get("detectors", []):
        print(f"check={detector.get('check')}")
        print(f"impact={detector.get('impact')}")


if __name__ == "__main__":
    main()

