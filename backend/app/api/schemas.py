from typing import List, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Citation source model"""
    id: str
    title: str
    authors: List[str]
    journal: str
    year: int
    pubmedId: str
    url: str
    relevance_score: Optional[float] = Field(default=0.0, ge=0.0, le=1.0)


class QueryRequest(BaseModel):
    """Frontend request payload"""
    query: str = Field(min_length=10, max_length=500)
    session_id: Optional[str] = None
    include_guidelines: bool = True


class RAGResponse(BaseModel):
    """Response to send back to frontend"""
    answer: str
    sources: List[Source]
    confidence: float = Field(ge=0.0, le=1.0)
    processing_time_ms: float
    query_validated: bool
    warning_message: Optional[str] = None
    citations_in_text: List[int]


class HealthCheck(BaseModel):
    status: str
    vectorstore_loaded: bool
    llm_available: bool

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Source(BaseModel):
    """Citation source model"""
    id: str
    title: str
    authors: List[str]
    journal: str
    year: int
    pubmedId: str
    url: str
    relevance_score: Optional[float] = Field(default=0.0, le=1.0, ge=0.0)

class QueryRequest(BaseModel):
    """Frontend request payload"""
    query: str = Field(..., min_length=10, max_length=500)
    session_id: Optional[str] = None
    include_guidelines: bool = True

class RAGResponse(BaseModel):
    """Response to send back to frontend"""
    answer: str
    sources: List[Source]
    confidence: float = Field(ge=0.0, le=1.0)
    processing_time_ms: float
    query_validated: bool
    warning_message: Optional[str] = None
    citations_in_text: List[int]  # [1], [2] indices

class HealthCheck(BaseModel):
    status: str
    vectorstore_loaded: bool
    llm_available: bool