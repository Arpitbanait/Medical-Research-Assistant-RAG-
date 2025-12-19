"""Confidence scoring utilities for RAG responses."""
from typing import List


def calculate_confidence(
    num_sources: int,
    avg_relevance: float,
    answer_text: str,
    citation_count: int = 0
) -> float:
    """Calculate confidence score for a RAG answer."""
    
    # Base confidence from source quantity (0-0.5)
    source_score = min(0.5, (num_sources / 10) * 0.5)
    
    # Relevance quality score (0-0.3)
    relevance_score = avg_relevance * 0.3
    
    # Citation density bonus (0-0.2)
    words = len(answer_text.split())
    citation_density = citation_count / max(1, words / 50)  # Citations per 50 words
    citation_score = min(0.2, citation_density * 0.1)
    
    confidence = source_score + relevance_score + citation_score
    
    # Penalties
    if "insufficient" in answer_text.lower():
        confidence = min(confidence, 0.2)
    
    if num_sources < 2:
        confidence *= 0.6  # Penalize single-source answers
    
    return min(1.0, max(0.0, confidence))


def get_confidence_level(confidence: float) -> str:
    """Convert numeric confidence to human-readable level."""
    if confidence >= 0.8:
        return "High"
    elif confidence >= 0.5:
        return "Medium"
    else:
        return "Low"


def explain_confidence(confidence: float, num_sources: int) -> str:
    """Generate explanation for confidence score."""
    level = get_confidence_level(confidence)
    
    if level == "High":
        return f"High confidence based on {num_sources} high-quality sources with consistent findings."
    elif level == "Medium":
        return f"Moderate confidence with {num_sources} sources. Additional research may provide more clarity."
    else:
        return f"Low confidence. Limited sources ({num_sources}) or insufficient evidence for this query."
