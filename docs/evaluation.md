# 真实合约案例评估

## 运行

```bash
source .venv/bin/activate
python -m app.evaluation.evaluate_cases
```

该评估脚本使用本地 Slither、FedVulGuard-compatible baseline、RAG 工作流，
不会调用云端 LLM，因此不会产生 API 费用。

## 当前案例

| 文件 | 预期覆盖 |
| --- | --- |
| `safe.sol` | 无明确漏洞 |
| `integer_overflow.sol` | SWC-101 |
| `reentrancy.sol` | SWC-107 |
| `invalid.sol` | 编译错误处理 |

云端 Agent 的 Tool Calling 和 Structured Output 使用：

```bash
python -m app.api.agent_smoke_test
```

该命令需要 `.env` 中配置百炼 API Key，会产生 API 调用费用。
