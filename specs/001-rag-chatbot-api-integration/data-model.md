# Data Model: RAG Chatbot API Integration

## Entities

### Query
**Description**: Represents a user's input to the RAG chatbot system
**Fields**:
- `message`: string - The user's query text
- `timestamp`: datetime - When the query was submitted
- `session_id`: string (optional) - Identifier for conversation session
- `user_id`: string (optional) - Identifier for the user (if implemented)

**Validation Rules**:
- `message` must be between 1 and 2000 characters
- `message` cannot be empty or contain only whitespace
- `timestamp` is automatically generated

### Response
**Description**: Represents the RAG agent's response to a user query
**Fields**:
- `response`: string - The AI-generated response text
- `sources`: array of strings - References to book content used in response
- `timestamp`: datetime - When the response was generated
- `query_id`: string - Reference to the original query
- `grounding_confidence`: number (0-1) - Confidence level in content grounding

**Validation Rules**:
- `response` must be between 1 and 10000 characters
- `sources` array must contain valid book content references
- `grounding_confidence` must be between 0 and 1

### API Request
**Description**: Structure of requests sent from frontend to backend
**Fields**:
- `query`: Query object - The user's query information
- `options`: object (optional) - Additional request options

**Validation Rules**:
- Must contain a valid Query object
- `options` must conform to expected structure if present

### API Response
**Description**: Structure of responses sent from backend to frontend
**Fields**:
- `success`: boolean - Whether the request was successful
- `data`: Response object - The response data if successful
- `error`: string (optional) - Error message if unsuccessful
- `timestamp`: datetime - When the response was created

**Validation Rules**:
- `success` must be a boolean value
- If `success` is false, `error` must be present
- If `success` is true, `data` must be present

## State Transitions

### Query Processing Flow
1. **Submitted**: Query received by API endpoint
2. **Processing**: RAG agent processing the query
3. **Completed**: Response generated and returned to frontend
4. **Error**: If any step fails, error state is returned

## Relationships

- Each Query generates exactly one Response
- Each Response references the original Query via `query_id`
- Multiple Queries can be part of the same session via `session_id`