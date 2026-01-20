from app.rag.types import RAGState
from app.rag.prompts.validation import VALIDATION_PROMPT
from app.llm.anthropic_client import get_default_llm

def validator_node(state: RAGState) -> RAGState:
    """Validate query safety"""

    llm = get_default_llm()
    chain = VALIDATION_PROMPT | llm

    result = chain.invoke({"query": state["query"]})

    content = (result.content or "").upper()
    is_valid = "APPROVED" in content and "REJECTED" not in content

    return {
        **state,
        "query_validated": is_valid,
        "warning": None if is_valid else "Medical query rejected for safety reasons."
    }