"""Anthropic Claude client initialization."""
from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from app.config import settings


@lru_cache(maxsize=None)
def get_llm(temperature: float | None = None, streaming: bool = False):
    """Lazily initialize Anthropic Claude LLM (cached per config)."""
    temp_val = settings.llm_temperature if temperature is None else temperature
    return ChatAnthropic(
        model=settings.anthropic_model,
        anthropic_api_key=settings.anthropic_api_key,
        temperature=temp_val,
        max_tokens=settings.llm_max_tokens,
        streaming=streaming,
    )


def get_default_llm():
    return get_llm()


def get_creative_llm():
    return get_llm(temperature=0.7)


def get_streaming_llm():
    return get_llm(streaming=True)
