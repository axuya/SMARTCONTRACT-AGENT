# SmartContract Security Agent

基于 LangChain 的智能合约安全审计 Agent。

当前阶段：Phase 12，已使用阿里云百炼完成基础 LangChain Tool Calling 验证。

当前已实现：

- FastAPI 最小服务
- `/health` 健康检查接口
- Pydantic Settings 配置读取
- 基础日志配置
- LangChain 依赖声明
- LangChain LLM 客户端
- Qwen/OpenAI-compatible 和 Ollama 配置入口
- Ollama 本地 Qwen 模型真实调用验证
- 第一个 LangChain Tool Calling 示例代码
- LangChain 多 Tool Agent
- Slither 结构化分析 Tool
- Chroma + HuggingFace Embedding RAG Tool
- FedVulGuard-compatible 本地基线 Tool
- 统一审计工作流基础
- 结构化审计报告生成
- FastAPI `/audit` 接口
- FastAPI `/audit-agent` Agent 接口
- 真实 Solidity 测试案例
- Docker 配置和项目文档
- 面试演示流程和保守版简历草稿

本地多案例评估：

```bash
source .venv/bin/activate
python -m app.evaluation.evaluate_cases
```

当前四个案例评估结果为 `4/4` 通过；该命令不调用云端 LLM。

当前未实现：

- 原始 FedVulGuard 模型权重接入
- Docker 镜像构建验证（本机 Docker daemon 尚未运行）

多 Tool Agent 调试：

```bash
source .venv/bin/activate
python -m app.agent.multi_tool_smoke_test
```

## Phase 3：测试 Tool Calling

```bash
LLM_PROVIDER=ollama \
LLM_MODEL=qwen3:4b \
python -m app.agent.basic_tool_smoke_test
```

使用支持原生工具调用的云端模型测试时，输出应包含：

```text
tool_message_count=1
tool_name=get_contract_basic_info
```

说明：本机 Ollama 的 qwen3 模型未作为 Tool Calling 验证模型；阿里云百炼 Qwen API 已完成真实基础 Tool Calling 验证。

## Phase 4：测试 Slither Tool

```bash
source .venv/bin/activate
python -m app.tools.slither_smoke_test
```

该 Tool 会：

- 将 Solidity 源码写入临时目录；
- 调用 Slither 的 JSON 输出模式；
- 解析 detector 结果；
- 处理 Slither 不存在、空源码、编译失败和超时；
- 返回 Agent 可以消费的结构化字典。

## Phase 6：测试 RAG Security Knowledge Tool

```bash
source .venv/bin/activate
python -m app.rag.smoke_test
```

首次运行会下载 Embedding 模型并在 `chroma_data/` 创建本地向量索引。
当前知识库包含 SWC-101 和 SWC-107 文档。

## Phase 5：FedVulGuard-compatible 本地基线

当前实现了一个轻量、本地可运行的规则基线，覆盖 SWC-101 和 SWC-107。它不是原始 FedVulGuard 模型权重，而是保持相同 Tool 接口的可替换基线。

```bash
source .venv/bin/activate
python -m app.fedvulguard.smoke_test
```

后续如果获得原始模型的调用方式，只需替换适配器实现，不需要修改 Agent 其他模块。

## Phase 7：运行统一审计工作流

当前工作流会真实执行 Slither、FedVulGuard 适配器和 RAG，并汇总工具状态与知识引用。
LLM 的动态工具选择和最终报告综合会在云端 Tool Calling 可用后接入。

```bash
source .venv/bin/activate
python -m app.agent.audit_workflow_smoke_test
```

## Phase 8：测试结构化审计报告

```bash
source .venv/bin/activate
python -m app.security.report_smoke_test
```

## Phase 9：测试 FastAPI `/audit`

```bash
source .venv/bin/activate
python -m app.api.smoke_test
```

启动服务：

```bash
uvicorn app.main:app --reload
```

接口：

```text
POST http://127.0.0.1:8000/audit
```

## Phase 2：测试 LLM 调用

复制配置模板：

```bash
cp .env.example .env
```

然后在 `.env` 中填写本地 API Key：

```text
LLM_API_KEY=<your_api_key>
```

运行：

```bash
source .venv/bin/activate
python -m app.llm.smoke_test
```

该命令会通过 LangChain 调用一次真实模型并打印回答。

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

## Phase 10：运行真实 Solidity 测试

```bash
source .venv/bin/activate
pytest -q
```

测试案例位于 `contracts/samples/`，包括正常合约、SWC-101、SWC-107 和编译失败合约。

## 项目文档

- [架构说明](docs/architecture.md)
- [API 使用说明](docs/api.md)
- [项目状态](docs/project_status.md)
- [面试演示](docs/interview_demo.md)
- [简历草稿](docs/resume_draft.md)

## Docker

```bash
docker build -t smartcontract-security-agent .
docker run --rm -p 8000:8000 smartcontract-security-agent
```
