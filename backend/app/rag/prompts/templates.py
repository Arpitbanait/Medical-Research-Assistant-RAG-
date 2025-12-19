"""Reusable prompt templates and formatting utilities."""
from langchain_core.prompts import PromptTemplate
from typing import List
from langchain_core.documents import Document


def format_context(documents: List[Document]) -> str:
    """Format documents into numbered context string."""
    if not documents:
        return "No context provided."
    
    formatted_parts = []
    for i, doc in enumerate(documents, 1):
        metadata = doc.metadata
        title = metadata.get('title', 'Unknown')
        journal = metadata.get('journal', 'Unknown')
        year = metadata.get('year', 'N/A')
        
        formatted_parts.append(
            f"[{i}] {doc.page_content}\n"
            f"Source: {title}, {journal} ({year})"
        )
    
    return "\n\n".join(formatted_parts)


def format_sources(documents: List[Document]) -> List[dict]:
    """Format documents into source citation objects."""
    sources = []
    for i, doc in enumerate(documents, 1):
        metadata = doc.metadata
        # Convert comma-separated authors string to list
        authors = metadata.get('authors', '')
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(';') if a.strip()]
        elif not isinstance(authors, list):
            authors = []
            
        sources.append({
            "id": str(i),
            "title": metadata.get('title', 'Unknown'),
            "authors": authors,
            "journal": metadata.get('journal', 'Unknown'),
            "year": metadata.get('year', 0),
            "pubmedId": metadata.get('pubmedId', ''),
            "url": metadata.get('url', ''),
            "relevance_score": 0.85  # Default score
        })
    return sources


REWRITE_QUERY_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""Rewrite this medical query to be more precise and search-friendly.

Original query: {query}

Rewritten query (keep it concise and specific):"""
)


MULTI_QUERY_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""Generate 3 alternative phrasings of this medical research query to improve retrieval.

Original: {query}

Alternative queries (one per line):
1.
2.
3."""
)


HYDE_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""Generate a hypothetical answer to this medical question based on what a research paper abstract might say.

Question: {query}

Hypothetical answer (2-3 sentences):"""
)


CONFIDENCE_EXPLANATION_PROMPT = PromptTemplate(
    input_variables=["confidence", "num_sources"],
    template="""Explain the confidence score for this medical research answer.

Confidence: {confidence}
Number of sources: {num_sources}

Explanation (1-2 sentences):"""
)


# System prompts
SYSTEM_PROMPT_MEDICAL_RAG = """You are a medical research assistant specializing in evidence-based medicine. 
Your responses must be grounded in peer-reviewed research. 
You do not provide personal medical advice. 
You cite sources for all claims."""

SYSTEM_PROMPT_STRICT = """You are a medical research assistant. 
You ONLY answer from provided research context. 
You NEVER use prior knowledge. 
You cite sources [1], [2] for every claim."""
