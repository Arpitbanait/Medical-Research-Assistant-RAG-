"""Embedding model initialization and utilities."""
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import login
import os
from app.config import settings


@lru_cache(maxsize=1)
def get_embeddings():
    """Lazily initialize the embedding model (cached)."""
    token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_TOKEN")
    if token:
        try:
            login(token=token)
        except Exception:
            # Proceed without login if token handling fails
            pass

    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
