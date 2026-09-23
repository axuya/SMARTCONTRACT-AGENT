from app.tools.rag_tool import search_security_knowledge


def main() -> None:
    results = search_security_knowledge.invoke(
        {"query": "外部调用发生在余额更新之前，可能重复提取资金"}
    )
    if not any(result["source"] == "swc-107.md" for result in results):
        raise RuntimeError("RAG 检索未命中 swc-107.md")
    print(f"result_count={len(results)}")
    for result in results:
        print(f"source={result['source']}")
        print(f"content_preview={result['content'][:180]}")


if __name__ == "__main__":
    main()
