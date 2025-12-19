from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application configuration using environment variables"""

    # Application
    app_name: str = "Medical Research RAG API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API
    api_prefix: str = "/api"
    allowed_origins: list[str] = ["http://localhost:8080", "http://localhost:3000"]
    
    # Anthropic LLM
    anthropic_api_key: str
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096
    
    # Vector Database
    vectorstore_type: str = "chroma"  # chroma or faiss
    chroma_db_path: str = "data/chroma_db"
    chroma_collection_name: str = "medical_research"
    
    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # RAG Pipeline
    retrieval_top_k: int = 8
    filter_top_k: int = 5
    min_year_threshold: int = 2020
    min_quality_score: float = 0.5
    confidence_threshold: float = 0.3
    
    # Query Validation
    unsafe_keywords: list[str] = [
        "dose for me",
        "emergency",
        "diagnose me",
        "prescribe",
        "am i",
        "do i have",
        "should i take",
    ]
    
    # Caching (Optional)
    redis_url: Optional[str] = None
    cache_ttl: int = 3600  # seconds
    
    # Logging
    log_level: str = "INFO"
    
    # Data Sources
    pubmed_api_key: Optional[str] = None
    pubmed_email: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
