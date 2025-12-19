from langchain_chroma import Chroma
from app.rag.types import RAGState
from app.config import settings
from app.vectorstore.embeddings import get_embeddings
import os

# Get absolute path relative to backend root (4 levels up from retriever.py in app/rag/nodes/)
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
chroma_path = os.path.join(BACKEND_ROOT, settings.chroma_db_path)

# Lazy load vectorstore to ensure embeddings are initialized
_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        embeddings = get_embeddings()
        _vectorstore = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=embeddings,
            persist_directory=chroma_path
        )
    return _vectorstore


def retriever_node(state: RAGState) -> RAGState:
    """Retrieve relevant documents"""
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(state["query"], k=8)

    return {
        **state,
        "documents": docs
    }