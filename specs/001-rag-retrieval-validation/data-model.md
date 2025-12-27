# Data Model: RAG Retrieval Validation

## Entity: RetrievedChunk
**Description**: Represents a text chunk returned from vector search with associated metadata and relevance score

**Fields**:
- `chunk_id` (string): Unique identifier for the chunk in Qdrant
- `content` (string): The actual text content retrieved from the vector database
- `embedding` (list[float]): Vector embedding of the content (1024 dimensions for Cohere multilingual model)
- `url` (string): Original URL where this content was sourced from
- `module` (string): Module/section name from the documentation structure
- `section` (string): Specific section within the module
- `source_path` (string): Path within the documentation site
- `relevance_score` (float): Similarity score returned by the vector search (0.0-1.0)
- `token_count` (int): Number of tokens in the chunk
- `created_at` (datetime): Timestamp when chunk was originally created

**Validation Rules**:
- `content` must not be empty
- `embedding` must have the correct dimensions (1024 for Cohere multilingual-v3.0 model)
- `url` must be a valid URL
- `relevance_score` must be between 0.0 and 1.0
- `token_count` must be positive

## Entity: QueryResult
**Description**: Contains the original query, retrieved chunks, relevance scores, and metadata about the search operation

**Fields**:
- `query_id` (string): Unique identifier for this query operation
- `original_query` (string): The text query that was submitted
- `retrieved_chunks` (list[RetrievedChunk]): List of chunks returned by the similarity search
- `query_time_ms` (float): Time taken to execute the search in milliseconds
- `retrieval_timestamp` (datetime): When the query was executed
- `metadata_validation_passed` (bool): Whether all metadata fields were correctly preserved
- `semantic_relevance_score` (float): Overall relevance score of results to the query (0.0-1.0)
- `total_chunks_found` (int): Total number of chunks returned by the search

**Validation Rules**:
- `original_query` must not be empty
- `retrieved_chunks` list must contain at least one chunk for successful queries
- `query_time_ms` must be positive
- `semantic_relevance_score` must be between 0.0 and 1.0

## Entity: RetrievalTest
**Description**: Defines a test case with a sample query and expected results for validation purposes

**Fields**:
- `test_id` (string): Unique identifier for the test case
- `query` (string): The sample query to test
- `expected_keywords` (list[string]): Keywords that should appear in relevant results
- `expected_module` (string): Expected module that should be represented in results
- `expected_section` (string): Expected section that should be represented in results
- `min_relevance_threshold` (float): Minimum relevance score for acceptable results (0.0-1.0)
- `test_category` (string): Category of test (e.g., "technical", "conceptual", "cross-module")
- `created_at` (datetime): When the test was created

**Validation Rules**:
- `query` must not be empty
- `expected_keywords` must contain at least one keyword
- `min_relevance_threshold` must be between 0.0 and 1.0

## Entity: QdrantConnection
**Description**: Handles connection to Qdrant Cloud with error handling and validation

**Fields**:
- `client` (QdrantClient): The active Qdrant client instance
- `connection_url` (string): URL of the Qdrant Cloud cluster
- `api_key` (string): API key for Qdrant Cloud access (masked for security)
- `collection_name` (string): Name of the collection to query
- `connected` (bool): Whether the connection is currently active
- `last_connection_attempt` (datetime): When the last connection attempt was made
- `connection_attempts` (int): Number of connection attempts made

**Validation Rules**:
- `connection_url` must be a valid URL
- `api_key` must be present and valid
- `collection_name` must not be empty

## Relationships

```
QdrantConnection 1 -> * QueryResult
QueryResult 1 -> * RetrievedChunk
RetrievalTest 1 -> 1 QueryResult (when executed)
```

A single `QdrantConnection` can execute multiple `QueryResult` operations, each `QueryResult` contains multiple `RetrievedChunk` entities, and a `RetrievalTest` produces one `QueryResult` when executed.

## State Transitions

### QueryResult
- `initialized` → `executing` → `completed` → `validated`
  - When a query is first created
  - When the similarity search is in progress
  - When the search completes and results are received
  - When validation of results is completed

### QdrantConnection
- `disconnected` → `connecting` → `connected` → `validating`
  - Initial state when client is created
  - When attempting to establish connection
  - When connection is successfully established
  - When validating collection and access