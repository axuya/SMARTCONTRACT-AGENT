# Architecture

```text
Client
  │
  ▼
FastAPI /audit
  │
  ▼
AuditWorkflow
  ├── Slither Tool
  ├── FedVulGuard-compatible baseline Tool
  └── RAG Security Knowledge Tool
        │
        ├── HuggingFace Embedding
        └── Chroma
  │
  ▼
Structured AuditReport
```

## Current implementation status

- Slither：已真实运行并返回 detector 结果；检测到漏洞时即使 CLI 返回码为 255，只要 JSON 完整仍标记为 `success`。
- FedVulGuard-compatible baseline：已实现 SWC-101、SWC-107 轻量规则检测。
- RAG：已使用 SWC-101、SWC-107 文档建立 Chroma 索引并检索。
- FastAPI：已实现 `/health` 和 `/audit`。
- LLM Tool Calling：代码已准备，等待可用云端模型完成真实 `tool_calls` 验证。
- 原始 FedVulGuard 权重：未接入，当前基线不是原始科研模型。
