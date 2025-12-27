"""
Configuration management module for the Documentation Ingestion Pipeline
Handles environment variables and application settings
"""
import os
from typing import Optional

# Load environment variables if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not available, environment variables must be set externally
    pass


class Config:
    """Configuration class to manage application settings"""

    # Cohere API configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant Cloud configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "docs_embeddings")

    # Crawler configuration
    CRAWLER_DELAY_BETWEEN_REQUESTS: float = float(os.getenv("CRAWLER_DELAY_BETWEEN_REQUESTS", "1.0"))
    CRAWLER_TIMEOUT: int = int(os.getenv("CRAWLER_TIMEOUT", "30"))
    CRAWLER_MAX_DEPTH: int = int(os.getenv("CRAWLER_MAX_DEPTH", "3"))
    CRAWLER_USER_AGENT: str = os.getenv("CRAWLER_USER_AGENT", "DocIngestionBot/1.0")

    # Chunking configuration
    CHUNK_SIZE_MIN: int = int(os.getenv("CHUNK_SIZE_MIN", "200"))
    CHUNK_SIZE_MAX: int = int(os.getenv("CHUNK_SIZE_MAX", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # Deployed URL for testing
    DEPLOYED_VERCAL_URL: str = os.getenv("DEPLOYED_VERCAL_URL", "")

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration values are present"""
        required_vars = [
            cls.COHERE_API_KEY,
            cls.QDRANT_URL,
            cls.QDRANT_API_KEY
        ]

        return all(var != "" for var in required_vars)

    @classmethod
    def get_missing_vars(cls) -> list:
        """Get list of missing required environment variables"""
        missing = []

        if not cls.COHERE_API_KEY:
            missing.append("COHERE_API_KEY")
        if not cls.QDRANT_URL:
            missing.append("QDRANT_URL")
        if not cls.QDRANT_API_KEY:
            missing.append("QDRANT_API_KEY")

        return missing