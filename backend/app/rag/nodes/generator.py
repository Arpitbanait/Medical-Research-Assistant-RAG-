from app.rag.types import RAGState
from app.rag.prompts.generation import GENERATION_PROMPT
from app.rag.prompts.templates import format_sources
from app.rag.utils.citations import extract_citations
from app.llm.anthropic_client import get_default_llm


def generator_node(state: RAGState) -> RAGState:
    """Generate grounded answer"""

    if not state.get("documents"):
        return {
            **state,
            "answer": "Insufficient research evidence available.",
            "sources": [],
            "citation_indices": []
        }
    
    context = "\n\n".join([
        f"[{i}] {doc.page_content}\nSource: {doc.metadata.get('title','Unknown')}"
        for i, doc in enumerate(state["documents"], 1)
    ])

    llm = get_default_llm()
    chain = GENERATION_PROMPT | llm

    response = chain.invoke({
        "context": context,
        "query": state["query"]
    })

    answer_text = response.content or ""

    # Extract citations
    citations = extract_citations(answer_text)

    # Format sources
    sources = format_sources(state["documents"])

    return {
        **state,
        "answer": answer_text,
        "sources": sources,
        "citation_indices": citations
    }
