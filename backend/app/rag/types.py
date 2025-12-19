from typing import TypedDict, List, Optional


class RAGState(TypedDict):
    """Workflow state shared across LangGraph nodes"""
    query: str
    documents: List
    answer: str
    confidence: float
    sources: List[dict]
    query_validated: bool
    warning: Optional[str]
    citation_indices: List[int]
