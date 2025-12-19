
from app.rag.types import RAGState
from app.config import settings


def filter_node(state: RAGState) -> RAGState:
    """Filter low-quality documents"""

    high_quality = []

    for doc in state.get("documents", []):
        metadata = getattr(doc, "metadata", {})
        year = metadata.get("year", 2000)
        pubmed_id = metadata.get("pubmedId", "")
        
        # Calculate quality score
        quality = 0.0
        
        # Recent research (2020+) is higher quality
        if year >= 2020:
            quality += 0.5
        elif year >= 2015:
            quality += 0.3
        else:
            quality += 0.1
            
        # Has pubmed ID
        if pubmed_id:
            quality += 0.5
        else:
            quality += 0.3  # Give credit even without pubmed ID
        
        high_quality.append({
            "doc": doc,
            "quality_score": quality
        })

    # Sort by quality and take top documents
    top_docs = sorted(high_quality, key=lambda x: x["quality_score"], reverse=True)[:settings.filter_top_k]

    return {
        **state,
        "documents": [d["doc"] for d in top_docs]
    }