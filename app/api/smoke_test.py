from fastapi.testclient import TestClient

from app.main import app


SOURCE_CODE = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ApiReentrancyExample {
    mapping(address => uint256) public balances;

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient balance");
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "transfer failed");
        balances[msg.sender] -= amount;
    }
}
"""


def main() -> None:
    client = TestClient(app)
    response = client.post(
        "/audit",
        json={"contract_name": "ApiReentrancy.sol", "source_code": SOURCE_CODE},
    )
    print(f"status_code={response.status_code}")
    body = response.json()
    print(f"risk_level={body['risk_level']}")
    print(f"vulnerability_ids={[item['id'] for item in body['vulnerabilities']]}")
    if response.status_code != 200 or body["risk_level"] != "high":
        raise RuntimeError("/audit API 验证失败")


if __name__ == "__main__":
    main()

