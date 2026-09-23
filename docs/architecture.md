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