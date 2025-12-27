# Quickstart: RAG Retrieval Validation Framework

## Overview

The RAG Retrieval Validation Framework provides tools to validate that your documentation ingestion pipeline is working correctly. It connects to Qdrant Cloud, executes similarity searches with sample queries, validates metadata preservation, and provides comprehensive test reporting.

## Prerequisites

- Python 3.11+
- Access to Qdrant Cloud with pre-existing embeddings
- Valid Cohere API key for embedding generation (if needed for testing)
- Pre-populated Qdrant collection with documentation embeddings

## Setup

1. **Install dependencies** (if not already installed):
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables** in `.env`:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=docs_embeddings
   ```

3. **Verify your environment**:
   ```bash
   python -c "from config import Config; print('Config loaded:', Config.validate())"
   ```

## Basic Usage

### Run Complete Validation Suite

```bash
cd backend
python retrieval.py --validate-all
```

This will:
- Connect to Qdrant Cloud
- Execute sample queries against the collection
- Validate metadata integrity
- Generate a comprehensive report

### Run Specific Validation Tests

```bash
# Test connectivity only
python retrieval.py --validate-connectivity

# Test retrieval with custom queries
python retrieval.py --validate-retrieval --queries "What is digital twin?" "How does ROS2 work?"

# Test metadata preservation
python retrieval.py --validate-metadata
```

### Interactive Validation

```bash
# Run in interactive mode to test custom queries
python retrieval.py --interactive
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--collection` | Qdrant collection name | From .env |
| `--queries-file` | JSON file with test queries | test_queries.json |
| `--min-relevance` | Minimum relevance threshold | 0.6 |
| `--top-k` | Number of results to retrieve per query | 5 |
| `--test-category` | Category of tests to run | all |

## Sample Test Queries

The framework includes predefined test queries for common documentation topics:

- Technical queries: "How to implement ROS2 navigation?"
- Conceptual queries: "What is embodied AI?"
- Cross-module queries: "How does perception integrate with action?"

## Validation Metrics

The framework reports on these key metrics:

- **Connectivity**: Successful connection to Qdrant Cloud
- **Retrieval Success Rate**: Percentage of queries returning results
- **Metadata Integrity**: Preservation of URL, module, and section information
- **Semantic Relevance**: Accuracy of retrieved content to query intent
- **Performance**: Query response times and throughput

## Custom Test Queries

To add custom test queries, create a JSON file:

```json
[
  {
    "query": "What is digital twin simulation?",
    "expected_keywords": ["digital twin", "simulation", "modeling"],
    "expected_module": "digital-twin",
    "min_relevance_score": 0.7
  },
  {
    "query": "Explain ROS2 navigation system",
    "expected_keywords": ["ROS2", "navigation", "path planning"],
    "expected_module": "ros2",
    "min_relevance_score": 0.65
  }
]
```

Then run validation with:
```bash
python retrieval.py --queries-file my_custom_tests.json
```

## Troubleshooting

- **Connection errors**: Verify Qdrant URL and API key in .env
- **No results**: Check that the collection contains embeddings
- **Low relevance**: May indicate issues with embedding quality or indexing
- **Missing metadata**: Indicates problems in the ingestion pipeline