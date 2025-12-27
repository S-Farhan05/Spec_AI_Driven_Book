"""
Utility functions for the Documentation Ingestion Pipeline
"""
import time
import random
import re
from typing import Callable, Type, Tuple
from functools import wraps
import requests


def retry_with_exponential_backoff(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if retries == max_retries - 1:
                        raise e

                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (backoff_factor ** retries), max_delay)
                    jitter = random.uniform(0, delay * 0.1)  # Add up to 10% jitter
                    time.sleep(delay + jitter)
                    retries += 1
            return func(*args, **kwargs)  # Final attempt
        return wrapper
    return decorator


def validate_url(url: str) -> bool:
    """
    Validate if a string is a properly formatted URL
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def normalize_url(url: str) -> str:
    """
    Normalize URL by ensuring it has proper scheme and removing trailing slashes
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Remove trailing slash if present (but keep the base domain slash)
    if url.endswith('/'):
        url = url.rstrip('/')

    return url


def is_valid_docusaurus_url(url: str) -> bool:
    """
    Check if URL appears to be a Docusaurus site by looking for common patterns
    """
    try:
        response = requests.head(url, timeout=10)
        # Check if it's a valid response
        if response.status_code < 400:
            # Check headers or make a light request to check for Docusaurus indicators
            # This is a basic check - in a real implementation, we might look for
            # specific Docusaurus-related HTML elements or headers
            return True
        return False
    except requests.RequestException:
        return False


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a text string.
    This is a simplified implementation - in a real scenario, you might use tiktoken or similar.
    For Cohere embeddings, we'll use a simple approximation: 1 token ~ 4 characters for English text.
    """
    # Simple approximation: 1 token is roughly 4 characters for English text
    # This is a conservative estimate - actual tokenizers may vary
    if not text:
        return 0

    # More accurate token counting would use a specific tokenizer
    # For now, using character-based approximation
    # In a real implementation, you might use: len(encoding.encode(text))
    return len(text) // 4


def count_tokens_cohere(text: str) -> int:
    """
    Count tokens specifically for Cohere models.
    This is an approximation - Cohere's tokenizer would give exact count.
    """
    if not text:
        return 0

    # This is a simplified approach
    # In a real implementation, you would use Cohere's tokenizer
    words = text.split()
    # Rough approximation: 1.3 tokens per word on average
    return int(len(words) * 1.3)