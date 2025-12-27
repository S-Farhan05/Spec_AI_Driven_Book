# Documentation Ingestion Pipeline

A Python-based backend service for ingesting Docusaurus documentation into vector storage for RAG applications.

## Features

- Crawls and parses Docusaurus documentation sites
- Extracts and chunks text content with semantic awareness
- Generates embeddings using Cohere models
- Stores embeddings in Qdrant Cloud with preserved metadata
- Provides API endpoints for programmatic access
- Modular execution for individual pipeline steps

## Prerequisites

- Python 3.11+
- Cohere API key
- Qdrant Cloud account and API key

## Setup

1. Clone the repository and navigate to the backend directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your configuration:
   ```bash
   cp .env.example .env
   ```
4. Update the `.env` file with your Cohere and Qdrant credentials

## Usage

### Command Line Interface

Run the complete ingestion pipeline:
```bash
python main.py --url "https://your-docusaurus-site.com" --collection "my_docs" --chunk-size 500
```

Or use the deployed URL from environment variables:
```bash
python main.py --url "$DEPLOYED_VERCAL_URL" --collection "my_docs" --chunk-size 500
```

Run individual pipeline steps:
```bash
# Just crawl
python main.py --url "https://your-docusaurus-site.com" --step crawl

# Just chunk
python main.py --url "https://your-docusaurus-site.com" --step chunk

# Just generate embeddings
python main.py --url "https://your-docusaurus-site.com" --step embed

# Just store in Qdrant
python main.py --url "https://your-docusaurus-site.com" --step store
```

### API Server

Start the API server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### `POST /ingest`

Start documentation ingestion process

**Request Body:**
```json
{
  "url": "https://example-docusaurus-site.com",
  "collection_name": "docs_embeddings",
  "chunk_size": 500,
  "max_depth": 3,
  "delay_between_requests": 1.0
}
```

**Response:**
```json
{
  "job_id": "job_1698765432",
  "status": "pending",
  "message": "Ingestion process started",
  "started_at": "2023-10-31T12:00:00Z"
}
```

### `GET /ingest/status/{job_id}`

Get ingestion job status

**Response:**
```json
{
  "job_id": "job_1698765432",
  "status": "completed",
  "progress": 1.0,
  "pages_processed": 25,
  "chunks_created": 120,
  "embeddings_generated": 120,
  "records_stored": 120
}
```

### `GET /health`

Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Documentation Ingestion Pipeline is running"
}
```

## Configuration

All configuration is handled through environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL of your Qdrant Cloud cluster
- `QDRANT_API_KEY`: API key for Qdrant Cloud access
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings in
- `CRAWLER_DELAY_BETWEEN_REQUESTS`: Delay in seconds between requests (default: 1.0)
- `CRAWLER_TIMEOUT`: Request timeout in seconds (default: 30)
- `CRAWLER_MAX_DEPTH`: Maximum depth to crawl (default: 3)
- `CHUNK_SIZE_MIN`: Minimum chunk size in tokens (default: 200)
- `CHUNK_SIZE_MAX`: Maximum chunk size in tokens (default: 1000)
- `DEPLOYED_VERCAL_URL`: URL of deployed documentation site for testing (optional)

## Architecture

The pipeline consists of the following components:

1. **Crawler**: Discovers and extracts content from Docusaurus sites
2. **Chunker**: Splits content into semantically coherent chunks
3. **Embedder**: Generates vector embeddings using Cohere models
4. **Storage**: Stores embeddings in Qdrant Cloud with metadata

## Success Criteria

- 95% of provided Docusaurus book URLs are successfully crawled and parsed
- Text chunks are generated with appropriate size (between 200-1000 tokens)
- Embedding generation completes with 99% success rate when Cohere API is available
- All vector embeddings are successfully stored in Qdrant Cloud with preserved metadata
- Documentation ingestion pipeline completes within 30 minutes for a medium-sized documentation site