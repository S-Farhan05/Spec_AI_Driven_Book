"""
Data models for the Documentation Ingestion Pipeline
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class DocumentChunk:
    """Represents a segment of text extracted from documentation with associated metadata and vector embedding"""
    chunk_id: str
    content: str
    embedding: Optional[List[float]] = None
    url: str = ""
    module: str = ""
    section: str = ""
    source_path: str = ""
    token_count: int = 0
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CrawledPage:
    """Represents an individual page or section from the Docusaurus documentation site"""
    page_id: str
    url: str
    title: str = ""
    content: str = ""
    module: str = ""
    section: str = ""
    links: List[str] = None
    status_code: int = 0
    fetched_at: datetime = None

    def __post_init__(self):
        if self.links is None:
            self.links = []
        if self.fetched_at is None:
            self.fetched_at = datetime.now()


@dataclass
class EmbeddingRecord:
    """Represents a vector embedding record stored in Qdrant with associated metadata"""
    record_id: str
    vector: List[float]
    payload: Dict[str, Any]
    collection_name: str

    def __post_init__(self):
        # Add any initialization logic if needed
        pass


@dataclass
class CrawlConfiguration:
    """Configuration parameters for the crawling process"""
    base_url: str
    include_patterns: List[str] = None
    exclude_patterns: List[str] = None
    max_depth: int = 3
    delay_between_requests: float = 1.0
    timeout: int = 30
    user_agent: str = "DocIngestionBot/1.0"

    def __post_init__(self):
        if self.include_patterns is None:
            self.include_patterns = [".*"]  # Include all by default
        if self.exclude_patterns is None:
            self.exclude_patterns = [r".*\.json$", r".*\.xml$"]  # Exclude JSON and XML files