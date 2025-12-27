# Quickstart: URL Ingestion and Embedding Pipeline

## Prerequisites

- Python 3.11 or higher
- uv package manager
- Cohere API key
- Qdrant Cloud account and API key
- Access to a deployed Docusaurus documentation site

## Setup

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd humanoid_robotics_book
   ```

2. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

3. **Install dependencies using uv**:
   ```bash
   uv sync
   # Or if starting fresh:
   uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file to include your API keys:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_COLLECTION_NAME=docs_embeddings
   ```

## Basic Usage

### Run the complete ingestion pipeline:
```bash
cd backend
python main.py --url "https://your-docusaurus-site.com" --collection "my_docs"
```

### Run with specific configuration:
```bash
python main.py --url "https://your-docusaurus-site.com" --chunk-size 500 --max-depth 2
```

### Run individual pipeline steps:
```bash
# Just crawl and extract content
python main.py --url "https://your-docusaurus-site.com" --step crawl

# Just chunk the content
python main.py --url "https://your-docusaurus-site.com" --step chunk

# Just generate embeddings
python main.py --url "https://your-docusaurus-site.com" --step embed

# Just store in Qdrant
python main.py --url "https://your-docusaurus-site.com" --step store
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Base URL of Docusaurus documentation site | Required |
| `--collection` | Qdrant collection name | "docs_embeddings" |
| `--chunk-size` | Target size for text chunks in tokens | 500 |
| `--max-depth` | Maximum depth to crawl from base URL | 3 |
| `--delay` | Delay between requests (seconds) | 1 |
| `--timeout` | Request timeout (seconds) | 30 |
| `--step` | Specific pipeline step to run | "all" |

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL of your Qdrant Cloud cluster
- `QDRANT_API_KEY`: API key for Qdrant Cloud access
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings in

## Example .env File

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=https://your-cluster-url.qdrant.tech:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=robotics_docs
```

## Verification

After running the pipeline successfully, you can verify:

1. **Check Qdrant collection**: Verify that vectors were stored with proper metadata
2. **Count records**: Check that the expected number of chunks were created
3. **Sample retrieval**: Test that you can retrieve relevant chunks based on semantic similarity

## Troubleshooting

- **Rate limit errors**: Ensure you're respecting API rate limits; adjust delay between requests if needed
- **Connection errors**: Verify that the Docusaurus site is accessible and that your Qdrant credentials are correct
- **Memory issues**: For large documentation sites, consider processing in batches or increasing system memory
- **Authentication errors**: Double-check your API keys in the environment variables