"""
Embedding generation for the Documentation Ingestion Pipeline
"""
from typing import List
from models import DocumentChunk
import logging
from clients import CohereClient
from config import Config


logger = logging.getLogger(__name__)


class Embedder:
    """Embedding generation using Cohere API"""

    def __init__(self, cohere_client: CohereClient = None):
        self.cohere_client = cohere_client or CohereClient()
        self.model = "embed-multilingual-v3.0"  # Using multilingual model as default

    def generate_embeddings_for_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """
        Generate embeddings for a list of DocumentChunk objects
        """
        if not chunks:
            logger.info("No chunks to generate embeddings for")
            return []

        # Extract text content from chunks
        texts = [chunk.content for chunk in chunks]

        # Generate embeddings in batches to respect API limits
        batch_size = 96  # Cohere's recommended batch size
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            logger.info(f"Processing embedding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            try:
                batch_embeddings = self.cohere_client.generate_embeddings(
                    texts=batch_texts,
                    model=self.model
                )
                all_embeddings.extend(batch_embeddings)
            except Exception as e:
                logger.error(f"Error generating embeddings for batch starting at index {i}: {str(e)}")
                # In a real implementation, you might want to retry or handle this differently
                raise

        # Assign embeddings back to chunks
        for i, chunk in enumerate(chunks):
            if i < len(all_embeddings):
                chunk.embedding = all_embeddings[i]
            else:
                logger.error(f"No embedding returned for chunk {chunk.chunk_id}")

        logger.info(f"Generated embeddings for {len(chunks)} chunks")
        return chunks

    def validate_embedding_dimensions(self, embedding: List[float], expected_size: int = 1024) -> bool:
        """
        Validate that an embedding has the expected dimensions
        Cohere's multilingual-v3.0 model produces 1024-dimensional embeddings
        """
        if len(embedding) != expected_size:
            logger.error(f"Embedding has {len(embedding)} dimensions, expected {expected_size}")
            return False
        return True

    def validate_embeddings_for_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """
        Validate that all chunks have properly sized embeddings
        """
        all_valid = True
        for chunk in chunks:
            if chunk.embedding is None:
                logger.error(f"Chunk {chunk.chunk_id} has no embedding")
                all_valid = False
            elif not self.validate_embedding_dimensions(chunk.embedding):
                logger.error(f"Chunk {chunk.chunk_id} has invalid embedding dimensions")
                all_valid = False

        return all_valid