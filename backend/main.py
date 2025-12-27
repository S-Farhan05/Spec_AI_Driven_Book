"""
Documentation Ingestion Pipeline
URL crawling, text chunking, embedding generation, and Qdrant storage
"""
import os
import logging
import asyncio
import argparse
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException
from tqdm import tqdm
import time
import re

from config import Config
from clients import CohereClient, QdrantClientWrapper, initialize_clients
from utils import (
    retry_with_exponential_backoff,
    validate_url,
    normalize_url,
    is_valid_docusaurus_url,
    count_tokens,
    count_tokens_cohere
)
from crawler import DocusaurusCrawler
from chunker import TextChunker
from embedder import Embedder
from storage import Storage
from models import CrawledPage

# Configure logging
def setup_logging():
    """Set up logging configuration for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("ingestion_pipeline.log")
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()




# Main application
app = FastAPI(
    title="Documentation Ingestion API",
    description="API for ingesting Docusaurus documentation into vector storage",
    version="1.0.0"
)


# API Models
class IngestionRequest(BaseModel):
    url: str
    collection_name: str = "docs_embeddings"
    chunk_size: int = 500
    max_depth: int = 3
    delay_between_requests: float = 1.0


class IngestionResponse(BaseModel):
    job_id: str
    status: str
    message: str
    started_at: datetime


class IngestionStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    pages_processed: int
    chunks_created: int
    embeddings_generated: int
    records_stored: int
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


# Placeholder for job tracking (in a real implementation, use a database)
job_status_store = {}


@app.get("/")
def read_root():
    return {"message": "Documentation Ingestion Pipeline API"}


@app.post("/ingest", response_model=IngestionResponse)
def start_ingestion(request: IngestionRequest):
    # This would start a background task in a real implementation
    # For now, we'll return a placeholder response
    job_id = f"job_{int(time.time())}"
    job_status_store[job_id] = {
        "status": "pending",
        "progress": 0.0,
        "pages_processed": 0,
        "chunks_created": 0,
        "embeddings_generated": 0,
        "records_stored": 0,
        "started_at": datetime.now()
    }

    return IngestionResponse(
        job_id=job_id,
        status="pending",
        message="Ingestion process started",
        started_at=datetime.now()
    )


@app.get("/ingest/status/{job_id}", response_model=IngestionStatus)
def get_ingestion_status(job_id: str):
    if job_id not in job_status_store:
        raise HTTPException(status_code=404, detail="Job not found")

    status = job_status_store[job_id]
    return IngestionStatus(
        job_id=job_id,
        **status
    )


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Validate that required configurations are present
        missing_vars = Config.get_missing_vars()
        if missing_vars:
            return {"status": "error", "message": f"Missing required environment variables: {missing_vars}"}

        # Try to validate connections to external services
        # For now, just return success - in a real implementation,
        # you might check connections to Cohere and Qdrant
        return {"status": "healthy", "message": "Documentation Ingestion Pipeline is running"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    """Main entry point for the ingestion pipeline"""
    parser = argparse.ArgumentParser(description="Documentation Ingestion Pipeline")
    parser.add_argument("--url", type=str, help="Base URL of the Docusaurus documentation site to ingest")
    parser.add_argument("--collection", type=str, default="docs_embeddings", help="Name of the Qdrant collection to store embeddings in")
    parser.add_argument("--chunk-size", type=int, default=500, help="Target size for text chunks in tokens")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum depth to crawl from base URL")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between HTTP requests in seconds")
    parser.add_argument("--step", type=str, choices=["crawl", "chunk", "embed", "store", "all"],
                       default="all", help="Specific pipeline step to run")

    args = parser.parse_args()

    if args.url:
        # Run the ingestion pipeline
        logger.info(f"Starting ingestion for URL: {args.url}")

        # Initialize clients
        cohere_client, qdrant_client = initialize_clients()

        # Create pipeline components
        crawler = DocusaurusCrawler({
            'base_url': args.url,
            'max_depth': args.max_depth,
            'delay_between_requests': args.delay
        })

        chunker = TextChunker(
            min_chunk_size=Config.CHUNK_SIZE_MIN,
            max_chunk_size=args.chunk_size,
            overlap=Config.CHUNK_OVERLAP
        )

        embedder = Embedder(cohere_client)
        storage = Storage(qdrant_client)

        try:
            if args.step == "all" or args.step == "crawl":
                # Run crawling step
                logger.info("Running crawling step...")
                crawled_pages = crawler.crawl()
                logger.info(f"Crawling completed: {len(crawled_pages)} pages crawled")

            if args.step == "all" or args.step == "chunk":
                # Run chunking step
                logger.info("Running chunking step...")
                if 'crawled_pages' not in locals():
                    # If we didn't crawl in this run, we need to crawl first
                    crawled_pages = crawler.crawl()

                chunks = chunker.chunk_pages(crawled_pages)
                logger.info(f"Chunking completed: {len(chunks)} chunks created")

            if args.step == "all" or args.step == "embed":
                # Run embedding step
                logger.info("Running embedding step...")
                if 'chunks' not in locals():
                    # If we didn't chunk in this run, we need to crawl and chunk first
                    crawled_pages = crawler.crawl()
                    chunks = chunker.chunk_pages(crawled_pages)

                chunks_with_embeddings = embedder.generate_embeddings_for_chunks(chunks)
                logger.info(f"Embedding completed: {len(chunks_with_embeddings)} chunks with embeddings")

            if args.step == "all" or args.step == "store":
                # Run storage step
                logger.info("Running storage step...")
                if 'chunks_with_embeddings' not in locals():
                    # If we didn't embed in this run, we need to go through the full pipeline
                    crawled_pages = crawler.crawl()
                    chunks = chunker.chunk_pages(crawled_pages)
                    chunks_with_embeddings = embedder.generate_embeddings_for_chunks(chunks)

                # Set up the collection
                storage.setup_collection()

                # Store the embeddings
                records_stored = storage.store_chunks(chunks_with_embeddings)
                logger.info(f"Storage completed: {records_stored} records stored in Qdrant")

            logger.info("Ingestion pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error during ingestion pipeline: {str(e)}")
            raise
    else:
        # Run as API server
        logger.info("Starting API server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()