from app.rag.types import RAGState
from app.rag.utils.scoring import calculate_confidence


def scorer_node(state: RAGState) -> RAGState:
    """Calculate confidence score"""

    sources = state.get("sources", [])
    answer = state.get("answer", "")
    citations = state.get("citation_indices", [])

    if not sources or not answer:
        return {**state, "confidence": 0.0}

    num_sources = len(sources)
    avg_relevance = (sum(s.get("relevance_score", 0.8) for s in sources) / max(1, num_sources)) if num_sources else 0.0

    confidence = calculate_confidence(
        num_sources=num_sources,
        avg_relevance=avg_relevance,
        answer_text=answer,
        citation_count=len(citations)
    )

    return {
        **state,
        "confidence": confidence
    }