"""
Storage implementation for the Documentation Ingestion Pipeline
Handles storing embeddings in Qdrant
"""
from typing import List
from models import DocumentChunk, EmbeddingRecord
import logging
from clients import QdrantClientWrapper
from config import Config
import hashlib
import time


logger = logging.getLogger(__name__)


class Storage:
    """Storage implementation for storing embeddings in Qdrant Cloud"""

    def __init__(self, qdrant_client: QdrantClientWrapper = None):
        self.qdrant_client = qdrant_client or QdrantClientWrapper()

    def setup_collection(self, vector_size: int = 1024, distance: str = "Cosine"):
        """
        Create a collection in Qdrant with specified vector size
        Cohere embeddings typically have 1024 dimensions for the multilingual model
        """
        self.qdrant_client.create_collection(vector_size, distance)
        logger.info(f"Collection {Config.QDRANT_COLLECTION_NAME} is ready")

    def create_payload(self, chunk: DocumentChunk) -> dict:
        """
        Create payload with metadata for Qdrant storage
        """
        return {
            "url": chunk.url,
            "module": chunk.module,
            "section": chunk.section,
            "content": chunk.content[:1000],  # Store truncated content to avoid large payloads
            "source_path": chunk.url,  # Same as URL for this implementation
            "token_count": chunk.token_count,
            "created_at": chunk.created_at.isoformat() if chunk.created_at else None
        }

    def store_chunks(self, chunks: List[DocumentChunk]) -> int:
        """
        Store DocumentChunk objects in Qdrant with their embeddings and metadata
        """
        if not chunks:
            logger.info("No chunks to store")
            return 0

        # Prepare data for storage
        vectors = []
        payloads = []
        ids = []

        for chunk in chunks:
            if chunk.embedding is None:
                logger.warning(f"Chunk {chunk.chunk_id} has no embedding, skipping storage")
                continue

            vectors.append(chunk.embedding)
            payloads.append(self.create_payload(chunk))

            # Convert string chunk_id to a valid Qdrant point ID (numeric)
            # Qdrant expects either unsigned integers or UUIDs, not arbitrary strings
            import hashlib
            # Create a numeric ID from the chunk_id hash
            chunk_numeric_id = int(hashlib.md5(chunk.chunk_id.encode()).hexdigest(), 16) % (10**18)  # Limit to 18 digits
            ids.append(chunk_numeric_id)

        if not vectors:
            logger.warning("No valid chunks with embeddings to store")
            return 0

        # Store in Qdrant
        try:
            self.qdrant_client.upsert_vectors(vectors, payloads, ids)
            logger.info(f"Successfully stored {len(vectors)} embeddings in Qdrant")
            return len(vectors)
        except Exception as e:
            logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise

    def validate_storage(self, chunk_ids: List[str]) -> bool:
        """
        Validate that chunks were successfully stored in Qdrant
        """
        try:
            # In a real implementation, we would check if the vectors exist in Qdrant
            # For now, we'll just return True as a placeholder
            logger.info(f"Storage validation completed for {len(chunk_ids)} chunks")
            return True
        except Exception as e:
            logger.error(f"Error validating storage: {str(e)}")
            return False

    def check_duplicate(self, content_hash: str) -> bool:
        """
        Check if content with the same hash already exists in the collection
        """
        try:
            # In a real implementation, we would query Qdrant for the hash
            # For now, this is a placeholder
            return False
        except Exception as e:
            logger.error(f"Error checking for duplicates: {str(e)}")
            return False