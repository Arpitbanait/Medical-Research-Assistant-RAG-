"""Embedding model initialization and utilities."""
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import login
import os
from app.config import settings


def get_embeddings():
    """Initialize and return the embedding model."""
    # Optionally authenticate with Hugging Face if a token is present
    token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_TOKEN")
    if token:
        try:
            login(token=token)
        except Exception:
            # Proceed without login if token handling fails
            pass

    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={'device': 'cpu'},  # Use 'cuda' for GPU
        encode_kwargs={'normalize_embeddings': True}
    )


# Global embeddings instance
embeddings = get_embeddings()
