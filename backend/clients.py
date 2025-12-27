"""
Client setup for external services (Cohere, Qdrant)
"""
from typing import Optional, List
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import Config
import logging


logger = logging.getLogger(__name__)


class CohereClient:
    """Wrapper for Cohere API client with error handling"""

    def __init__(self):
        if not Config.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(Config.COHERE_API_KEY)
        self.model = "embed-multilingual-v3.0"  # Using multilingual model as default

    def generate_embeddings(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Generate embeddings for a list of texts with automatic rate limit handling
        """
        import time
        import random

        max_retries = 5
        retry_count = 0

        while retry_count < max_retries:
            try:
                model = model or self.model
                response = self.client.embed(
                    texts=texts,
                    model=model,
                    input_type="search_document"  # Using search_document as default input type
                )
                return [embedding for embedding in response.embeddings]
            except cohere.errors.TooManyRequestsError as e:
                logger.warning(f"Rate limit exceeded (429), sleeping before retry (attempt {retry_count + 1}/{max_retries}): {str(e)}")
                if retry_count == max_retries - 1:
                    raise
                retry_count += 1
                time.sleep(random.uniform(60, 90))  # Random sleep between 60-90 seconds
            except Exception as e:
                # Check if it's a rate limit error with status code 429
                if hasattr(e, 'status_code') and e.status_code == 429:
                    logger.warning(f"Rate limit exceeded (429), sleeping before retry (attempt {retry_count + 1}/{max_retries}): {str(e)}")
                    if retry_count == max_retries - 1:
                        raise
                    retry_count += 1
                    time.sleep(random.uniform(60, 90))  # Random sleep between 60-90 seconds
                else:
                    logger.error(f"Error generating embeddings: {str(e)}")
                    raise

    def validate_api_key(self) -> bool:
        """
        Validate if the Cohere API key is valid by making a simple request
        """
        try:
            # Test with a simple embedding request
            test_embedding = self.client.embed(
                texts=["test"],
                model=self.model,
                input_type="search_document"
            )
            return len(test_embedding.embeddings) > 0
        except Exception as e:
            logger.error(f"Error validating Cohere API key: {str(e)}")
            return False


class QdrantClientWrapper:
    """Wrapper for Qdrant client with error handling"""

    def __init__(self):
        if not Config.QDRANT_URL or not Config.QDRANT_API_KEY:
            raise ValueError("QDRANT_URL or QDRANT_API_KEY environment variables are not set")

        self.client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
        )
        self.collection_name = Config.QDRANT_COLLECTION_NAME

    def create_collection(self, vector_size: int = 1024, distance: str = "Cosine"):
        """
        Create a collection in Qdrant with specified vector size
        Cohere embeddings typically have 1024 dimensions for the multilingual model
        """
        try:
            # Check if collection already exists
            try:
                self.client.get_collection(self.collection_name)
                logger.info(f"Collection {self.collection_name} already exists")
                return
            except:
                # Collection doesn't exist, create it
                pass

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=distance
                )
            )
            logger.info(f"Created collection {self.collection_name} with {vector_size} dimensions")
        except Exception as e:
            logger.error(f"Error creating Qdrant collection: {str(e)}")
            raise

    def upsert_vectors(self, vectors, payloads, ids):
        """
        Store vectors with their payloads in Qdrant
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=models.Batch(
                    ids=ids,
                    vectors=vectors,
                    payloads=payloads
                )
            )
        except Exception as e:
            logger.error(f"Error upserting vectors to Qdrant: {str(e)}")
            raise

    def validate_connection(self) -> bool:
        """
        Validate if the Qdrant connection is working
        """
        try:
            # Try to get collection info
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Successfully connected to Qdrant collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error validating Qdrant connection: {str(e)}")
            return False


# Initialize clients
def initialize_clients():
    """Initialize and return Cohere and Qdrant clients"""
    cohere_client = None
    qdrant_client = None

    # Initialize Cohere client
    try:
        cohere_client = CohereClient()
        logger.info("Cohere client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Cohere client: {str(e)}")
        raise

    # Initialize Qdrant client
    try:
        qdrant_client = QdrantClientWrapper()
        logger.info("Qdrant client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant client: {str(e)}")
        raise

    return cohere_client, qdrant_client