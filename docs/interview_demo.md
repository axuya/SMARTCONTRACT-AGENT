# Interview Demo

## 1. 启动服务

```bash
cd ~/Desktop/SmartContract-Security-Agent
source .venv/bin/activate
uvicorn app.main:app --reload
```

## 2. 打开 API 文档

访问：

```text
http://127.0.0.1:8000/docs
```

选择 `POST /audit`，输入一个包含外部调用后再更新余额的 Solidity 合约。

## 3. 现场解释链路

```text
请求进入 FastAPI
→ AuditWorkflow 调用 Slither
→ 本地基线识别 SWC-107
→ RAG 检索 SWC-107 修复知识
→ 合并重复发现
→ 返回 AuditReport JSON
```

如果演示 Agent 能力，使用 `/audit-agent`：

```text
请求进入 FastAPI
→ 百炼 Qwen 判断并调用多个 LangChain Tool
→ ToolMessage 返回检测结果
→ Agent 生成中文审计分析
→ API 同时返回 Tool Trace 和结构化报告
```

## 4. 面试时的边界说明

当前版本重点展示 Agent 工具编排、静态分析、RAG 和结构化输出。阿里云百炼 Qwen 已完成多 Tool Calling 验证；原始 FedVulGuard 权重仍未接入，当前使用的是兼容接口的本地轻量基线。
