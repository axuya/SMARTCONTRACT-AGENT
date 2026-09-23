from fastapi.testclient import TestClient

from app.api.smoke_test import SOURCE_CODE
from app.main import app


def main() -> None:
    response = TestClient(app).post(
        "/audit-agent",
        json={"contract_name": "AgentReentrancy.sol", "source_code": SOURCE_CODE},
    )
    print(f"status_code={response.status_code}")
    body = response.json()
    print(f"risk_level={body['report']['risk_level']}")
    print(f"agent_tool_trace={body['agent_tool_trace']}")
    if response.status_code != 200:
        raise RuntimeError(response.text)
    if not body["agent_tool_trace"]:
        raise RuntimeError("Agent tool trace 为空")


if __name__ == "__main__":
    main()

