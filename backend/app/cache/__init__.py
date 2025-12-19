"""Cache module initialization."""

from app.cache.redis_cache import get_cached_response, cache_response, clear_cache

__all__ = ["get_cached_response", "cache_response", "clear_cache"]
