from functools import lru_cache

from langchain_core.tools import tool

from app.rag.indexer import load_vector_store


@lru_cache(maxsize=1)
def _get_retriever():
    return load_vector_store().as_retriever(search_kwargs={"k": 3})


@tool
def search_security_knowledge(query: str) -> list[dict[str, object]]:
    """Retrieve relevant smart contract security knowledge for an audit question."""
    documents = _get_retriever().invoke(query)
    return [
        {
            "source": document.metadata.get("source", "unknown"),
            "content": document.page_content,
        }
        for document in documents
    ]

