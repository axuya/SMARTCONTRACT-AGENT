# SmartContract Security Agent

基于 LangChain 的智能合约安全审计 Agent。

启动服务：

```bash
uvicorn app.main:app --reload
```

接口：

```text
POST http://127.0.0.1:8000/audit
```


如果使用本机 Ollama，可以直接运行已验证的本地模型：

```bash
LLM_PROVIDER=ollama LLM_MODEL=qwen3:0.6b python -m app.llm.smoke_test
```

## 本地启动

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/health
```

## Docker

```bash
docker build -t smartcontract-security-agent .
docker run --rm -p 8000:8000 smartcontract-security-agent
```
