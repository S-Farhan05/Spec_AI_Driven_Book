# RAG Chatbot API Documentation

## Overview
The RAG Chatbot API provides a conversational interface to query book content using a Retrieval-Augmented Generation (RAG) system. The API connects user queries to a vector database of book content and generates responses grounded in the source material.

## Base URL
```
http://localhost:8000
```

## Endpoints

### POST /chat
Submit a query to the RAG chatbot and receive a response grounded in book content.

#### Request
```json
{
  "message": "string (required) - The user's query message",
  "session_id": "string (optional) - Session identifier for conversation continuity"
}
```

#### Response
```json
{
  "success": "boolean - Whether the request was successful",
  "data": {
    "response": "string - The AI-generated response",
    "sources": "string[] - List of sources used in the response",
    "timestamp": "string - ISO timestamp of the response",
    "grounding_confidence": "number (0-1) - Confidence level in content grounding"
  },
  "error": "string (optional) - Error message if success is false"
}
```

#### Example Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key principles of humanoid robotics?",
    "session_id": "session_12345"
  }'
```

#### Example Response
```json
{
  "success": true,
  "data": {
    "response": "The key principles of humanoid robotics include...",
    "sources": [
      "chapter_3.md",
      "section_5.2.md"
    ],
    "timestamp": "2025-12-27T10:00:00Z",
    "grounding_confidence": 0.85
  }
}
```

### GET /health
Check the health status of the API service.

#### Response
```json
{
  "status": "string - Health status ('healthy' or 'unhealthy')",
  "timestamp": "string - ISO timestamp of the check"
}
```

#### Example Request
```bash
curl http://localhost:8000/health
```

#### Example Response
```json
{
  "status": "healthy",
  "timestamp": "2025-12-27T10:00:00Z"
}
```

## Error Handling
The API follows standard HTTP status codes and returns structured error responses:

- `400 Bad Request`: Invalid request format or missing required fields
- `408 Request Timeout`: Query took too long to process
- `500 Internal Server Error`: Unexpected server error

## Response Format
All responses follow the same structure:
```json
{
  "success": true,
  "data": { ... },  // Present when success is true
  "error": "..."    // Present when success is false
}
```

## Content Grounding
All responses are grounded in the book content with:
- Source attribution for all information provided
- Confidence scores indicating how well the response is supported by the content
- Citations to specific sections when possible

## Session Management
The API supports session continuity through the optional `session_id` parameter, allowing for contextual conversations.