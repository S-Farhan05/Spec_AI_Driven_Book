# API Contract: RAG Agent Construction

## Agent Query Interface

### Endpoint: `/query`
**Method**: POST
**Purpose**: Submit a natural language query to the RAG agent

#### Request
```json
{
  "query": "What is digital twin simulation?",
  "session_id": "optional-session-identifier",
  "options": {
    "top_k": 5,
    "relevance_threshold": 0.5
  }
}
```

#### Response
```json
{
  "query_id": "unique-query-identifier",
  "answer": "Digital twin simulation is a virtual representation of a physical object or system that spans its lifecycle...",
  "confidence_score": 0.85,
  "retrieved_chunks": [
    {
      "chunk_id": "chunk-identifier",
      "content": "Digital twin simulation involves creating a virtual model that mirrors a physical system...",
      "url": "https://source-url.com",
      "module": "digital-twin",
      "section": "introduction",
      "relevance_score": 0.87
    }
  ],
  "sources": [
    {
      "url": "https://source-url.com",
      "module": "digital-twin",
      "section": "introduction"
    }
  ],
  "timestamp": "2025-12-25T10:30:00Z"
}
```

#### Error Response
```json
{
  "error": {
    "code": "RETRIEVAL_ERROR",
    "message": "Failed to retrieve relevant content from Qdrant",
    "details": "Connection timeout to Qdrant service"
  }
}
```

## Agent Status Interface

### Endpoint: `/status`
**Method**: GET
**Purpose**: Check the status of the RAG agent service

#### Response
```json
{
  "status": "healthy",
  "services": {
    "openai_agent": "connected",
    "qdrant_connection": "connected",
    "qdrant_collection": "docs_embeddings",
    "vector_count": 349
  },
  "timestamp": "2025-12-25T10:30:00Z"
}
```

## Agent Initialization Interface

### Endpoint: `/initialize`
**Method**: POST
**Purpose**: Initialize the RAG agent with configuration parameters

#### Request
```json
{
  "config": {
    "openai_api_key": "sk-...",
    "qdrant_url": "https://...",
    "qdrant_api_key": "...",
    "collection_name": "docs_embeddings",
    "model_name": "gpt-4",
    "retrieval_top_k": 5,
    "relevance_threshold": 0.5
  }
}
```

#### Response
```json
{
  "status": "initialized",
  "agent_id": "agent-identifier",
  "connected_services": {
    "openai": true,
    "qdrant": true
  },
  "timestamp": "2025-12-25T10:30:00Z"
}
```

## Validation Contract

### Validation Endpoint: `/validate`
**Method**: POST
**Purpose**: Validate agent behavior with sample queries

#### Request
```json
{
  "validation_queries": [
    {
      "query": "What is digital twin simulation?",
      "expected_keywords": ["digital twin", "simulation", "modeling"],
      "expected_module": "digital-twin"
    }
  ]
}
```

#### Response
```json
{
  "validation_results": [
    {
      "query": "What is digital twin simulation?",
      "relevance_score": 0.85,
      "keywords_found": ["digital twin", "simulation"],
      "module_correct": true,
      "validation_passed": true
    }
  ],
  "overall_success_rate": 1.0,
  "timestamp": "2025-12-25T10:30:00Z"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `RETRIEVAL_ERROR` | Failed to retrieve content from Qdrant |
| `AGENT_ERROR` | Error in agent processing |
| `VALIDATION_ERROR` | Validation failed |
| `CONFIG_ERROR` | Configuration error |
| `CONNECTION_ERROR` | Connection to external service failed |