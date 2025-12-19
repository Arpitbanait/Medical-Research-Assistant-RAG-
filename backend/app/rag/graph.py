from langgraph.graph import StateGraph, END,START
from typing import TypedDict, List , Annotated
import operator
from .nodes import validator_node, retriever_node, filter_node, generator_node, scorer_node


class RAGState(TypedDict):
    """Workflow state"""
    query: str
    documents: List
    answer: str
    confidence : float
    sources: List[dict]
    query_validated: bool
    warning : str
    citation_indices: List[int]


workflow = StateGraph(RAGState)

workflow.add_node("validate",validator_node)
workflow.add_node("retrieve",retriever_node)
workflow.add_node("filter", filter_node)
workflow.add_node("generate", generator_node)
workflow.add_node("score", scorer_node)


def should_proceed(state: RAGState) -> bool:
    """Determine if validation passed and we should proceed to retrieval"""
    return state.get("query_validated", False)


workflow.add_edge(START, "validate")
workflow.add_conditional_edges(
    "validate",
    should_proceed,
    {
        True: "retrieve",
        False: END
    }
)
workflow.add_edge("retrieve","filter")
workflow.add_edge("filter","generate")
workflow.add_edge("generate","score")
workflow.add_edge("score", END)

rag_graph = workflow.compile()