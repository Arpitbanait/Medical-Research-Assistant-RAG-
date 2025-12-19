"""Citation extraction and validation utilities."""
import re
from typing import List, Tuple


def extract_citations(text: str) -> List[int]:
    """Extract citation numbers from text like [1], [2], [3]."""
    pattern = r'\[(\d+)\]'
    matches = re.findall(pattern, text)
    return [int(m) for m in matches]


def validate_citations(text: str, num_sources: int) -> Tuple[bool, List[str]]:
    """Validate that all citations reference valid sources."""
    citations = extract_citations(text)
    errors = []
    
    for citation in citations:
        if citation < 1 or citation > num_sources:
            errors.append(f"Citation [{citation}] references non-existent source (valid range: 1-{num_sources})")
    
    return len(errors) == 0, errors


def align_citations_with_sources(text: str, sources: List[dict]) -> dict:
    """Map citations in text to actual source objects."""
    citations = extract_citations(text)
    unique_citations = sorted(set(citations))
    
    cited_sources = []
    for idx in unique_citations:
        if 0 < idx <= len(sources):
            cited_sources.append(sources[idx - 1])
    
    return {
        "cited_indices": unique_citations,
        "cited_sources": cited_sources,
        "citation_count": len(citations),
        "unique_citation_count": len(unique_citations)
    }


def format_citation(source: dict, index: int) -> str:
    """Format a source as a citation string."""
    authors = ", ".join(source.get('authors', [])[:3])
    if len(source.get('authors', [])) > 3:
        authors += " et al."
    
    journal = source.get('journal', 'Unknown')
    year = source.get('year', 'N/A')
    title = source.get('title', 'Untitled')
    
    return f"[{index}] {authors}. {title}. {journal}, {year}."
