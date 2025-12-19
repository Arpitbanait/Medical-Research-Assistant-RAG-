import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.rag.nodes.retriever import retriever_node
from app.rag.nodes.filter import filter_node
from app.rag.types import RAGState

# Test retrieval directly
test_query = "What are the benefits of metformin for Type 2 Diabetes?"

initial_state: RAGState = {
    "query": test_query,
    "documents": [],
    "answer": "",
    "sources": [],
    "confidence": 0.0,
    "processing_time_ms": 0.0,
    "query_validated": False,
    "warning_message": None,
    "citations_in_text": []
}

print(f"Testing retrieval for: {test_query}\n")

# Test retriever
state_after_retrieval = retriever_node(initial_state)
print(f"After retrieval: {len(state_after_retrieval['documents'])} documents found")
for i, doc in enumerate(state_after_retrieval['documents'][:3]):
    print(f"  {i+1}. {doc.metadata.get('title', 'Unknown')[:50]}...")

# Test filter
state_after_filter = filter_node(state_after_retrieval)
print(f"\nAfter filter: {len(state_after_filter['documents'])} documents")
for i, doc in enumerate(state_after_filter['documents'][:3]):
    metadata = doc.metadata
    print(f"  {i+1}. {metadata.get('title', 'Unknown')}")
    print(f"      Year: {metadata.get('year')}, PubMed: {metadata.get('pubmedId')}")

