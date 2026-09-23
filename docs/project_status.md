# Project Status

更新时间：2026-09-22

## 已完成并验证

- Python 3.14 项目初始化和虚拟环境。
- FastAPI `/health` 和 `/audit`。
- Slither 真实静态分析。
- SWC-101、SWC-107 轻量本地基线 Tool。
- Chroma + HuggingFace Embedding RAG。
- 统一审计工作流。
- 结构化审计报告。
- 4 个真实测试案例，pytest 全部通过。
- 阿里云百炼 Qwen API 的真实 LangChain Tool Calling。
- 多 Tool Agent 动态调用 Slither、基线检测和 RAG。
- FastAPI `/audit-agent` 已通过真实百炼 API 验证。
- Slither 检测结果状态已区分“检测到发现”和“真正执行失败”。
- LLM Structured Output 已接入 `/audit-agent`。

## 已实现

- LangChain Tool Calling 代码。
- Qwen/OpenAI-compatible LLM 客户端。

本机 Ollama 仅用于普通 LLM 调用；云端 Qwen API 已完成基础 `tool_calls` 验证。

## 当前明确未完成

- 原始 FedVulGuard 模型权重接入。
- Docker 镜像构建验证，原因是本机 Docker daemon 未运行。
