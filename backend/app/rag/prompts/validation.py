"""Prompts for query validation and safety checking."""
from langchain_core.prompts import PromptTemplate


VALIDATION_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""You are a medical query safety validator. Your job is to determine if a query is appropriate for an academic medical research assistant.

**REJECT queries that are:**
- Personal medical diagnoses ("What do I have?", "Do I have cancer?")
- Personal treatment requests ("Prescribe medication for me", "What dose should I take?")
- Medical emergencies ("I'm having chest pain", "Help, I'm bleeding")
- Specific personal medical advice ("Should I stop taking my medication?")

**APPROVE queries that are:**
- General medical research questions ("What are treatments for diabetes?")
- Comparative questions ("Compare drug A vs drug B efficacy")
- Literature reviews ("Latest research on Alzheimer's biomarkers")
- Evidence-based guidelines ("WHO recommendations for hypertension")

Query to validate:
"{query}"

Respond with EXACTLY one of:
- "APPROVED" - if the query is appropriate for academic/research purposes
- "REJECTED: [reason]" - if the query requests personal medical advice or is unsafe

Response:"""
)


SIMPLE_VALIDATION_PROMPT = PromptTemplate(
    input_variables=["query", "unsafe_keywords"],
    template="""Is this medical query safe for academic research response?

Unsafe patterns: {unsafe_keywords}

Query: {query}

Respond: APPROVED or REJECTED"""
)
