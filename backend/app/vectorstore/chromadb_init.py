"""ChromaDB vector store initialization."""
import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from app.vectorstore.embeddings import embeddings
from app.config import settings


def get_chroma_path() -> str:
    """Get absolute path to ChromaDB storage."""
    backend_root = Path(__file__).parent.parent.parent
    chroma_path = backend_root / settings.chroma_db_path
    
    # Ensure directory exists
    chroma_path.mkdir(parents=True, exist_ok=True)
    
    return str(chroma_path)


def initialize_vectorstore(persist_directory: str = None) -> Chroma:
    """Initialize or load existing ChromaDB vectorstore."""
    if persist_directory is None:
        persist_directory = get_chroma_path()
    
    vectorstore = Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    
    return vectorstore


def get_vectorstore() -> Chroma:
    """Get the global vectorstore instance."""
    return initialize_vectorstore()
