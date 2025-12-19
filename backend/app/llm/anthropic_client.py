"""Anthropic Claude client initialization."""
from langchain_anthropic import ChatAnthropic
from app.config import settings


def get_llm(temperature: float = None, streaming: bool = False):
    """Initialize Anthropic Claude LLM."""
    if temperature is None:
        temperature = settings.llm_temperature
    
    return ChatAnthropic(
        model=settings.anthropic_model,
        anthropic_api_key=settings.anthropic_api_key,
        temperature=temperature,
        max_tokens=settings.llm_max_tokens,
        streaming=streaming
    )


# Global LLM instances
llm = get_llm()  # Default deterministic LLM
llm_creative = get_llm(temperature=0.7)  # For query rewriting
llm_streaming = get_llm(streaming=True)  # For SSE endpoints
