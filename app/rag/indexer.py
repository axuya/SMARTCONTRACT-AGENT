from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
VECTOR_DIR = PROJECT_ROOT / "chroma_data"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def load_knowledge_documents() -> list[Document]:
    documents = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": path.name},
            )
        )
    if not documents:
        raise FileNotFoundError(f"No knowledge documents found in {KNOWLEDGE_DIR}")
    return documents


def build_vector_store() -> Chroma:
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = splitter.split_documents(load_knowledge_documents())
    return Chroma.from_documents(
        documents=chunks,
        embedding=build_embeddings(),
        persist_directory=str(VECTOR_DIR),
        collection_name="security_knowledge",
    )


def load_vector_store() -> Chroma:
    if not VECTOR_DIR.exists():
        return build_vector_store()
    return Chroma(
        persist_directory=str(VECTOR_DIR),
        embedding_function=build_embeddings(),
        collection_name="security_knowledge",
    )

