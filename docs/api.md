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
