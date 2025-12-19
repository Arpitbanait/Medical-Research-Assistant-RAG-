"""Redis caching for query responses (optional optimization)."""

import json
import hashlib
from typing import Optional
from app.config import settings

# Optional Redis caching - uncomment if using Redis
# import redis

# redis_client = redis.from_url(settings.redis_url) if settings.redis_url else None


def get_cache_key(query: str) -> str:
    """Generate cache key from query."""
    return f"rag_query:{hashlib.md5(query.encode()).hexdigest()}"


def get_cached_response(query: str) -> Optional[dict]:
    """Retrieve cached response if available."""
    # if not redis_client:
    #     return None
    # 
    # key = get_cache_key(query)
    # cached = redis_client.get(key)
    # 
    # if cached:
    #     return json.loads(cached)
    
    return None


def cache_response(query: str, response: dict, ttl: int = 3600):
    """Cache response for future queries."""
    # if not redis_client:
    #     return
    # 
    # key = get_cache_key(query)
    # redis_client.setex(key, ttl, json.dumps(response))
    
    pass


def clear_cache():
    """Clear all cached responses."""
    # if redis_client:
    #     for key in redis_client.scan_iter("rag_query:*"):
    #         redis_client.delete(key)
    
    pass
