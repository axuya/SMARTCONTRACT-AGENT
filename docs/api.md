# API 使用说明

## Health

```http
GET /health
```

## Audit

```http
POST /audit
Content-Type: application/json
```

请求：

```json
{
  "contract_name": "Reentrancy.sol",
  "source_code": "contract Example {}"
}
```

启动服务：

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

## Agent Audit

```http
POST /audit-agent
Content-Type: application/json
```

该接口需要本地 `.env` 配置百炼 Qwen API Key，会真实执行多 Tool Agent，并返回：

- Agent 最终审计说明；
- Agent Tool Calling 轨迹；
- 确定性结构化 AuditReport。

真实验证结果：HTTP 200，成功调用 Slither、FedVulGuard-compatible baseline 和 RAG，并返回 high 风险报告。

`/audit-agent` 的最终 `report` 字段由 LangChain Structured Output 解析为 Pydantic `AuditReport`。

如果服务进程找不到 Slither，可以在 `.env` 中显式配置：

```env
SLITHER_PATH=/Users/你的用户名/miniconda3/bin/slither
SOLC_PATH=/Users/你的用户名/miniconda3/bin/solc
```
