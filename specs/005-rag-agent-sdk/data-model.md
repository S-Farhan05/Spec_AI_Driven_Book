# Data Model: RAG Agent Construction with OpenAI Agent SDK

## Agent Configuration Model
**Entity**: AgentConfig
**Fields**:
- `agent_id`: str - Unique identifier for the agent instance
- `openai_api_key`: str - API key for OpenAI services
- `qdrant_url`: str - URL for Qdrant vector database
- `qdrant_api_key`: str - API key for Qdrant access
- `collection_name`: str - Name of the Qdrant collection to search
- `retrieval_top_k`: int - Number of chunks to retrieve (default: 5)
- `relevance_threshold`: float - Minimum relevance score for inclusion (default: 0.5)
- `model_name`: str - Name of the OpenAI model to use (default: "gpt-4")

## Retrieved Chunk Model
**Entity**: RetrievedChunk
**Fields**:
- `chunk_id`: str - Unique identifier for the content chunk
- `content`: str - The actual text content retrieved
- `url`: str - Source URL for the content
- `module`: str - Module or section identifier
- `section`: str - Specific section within the module
- `relevance_score`: float - Similarity score to the query (0.0-1.0)
- `token_count`: int - Number of tokens in the content

## Agent Query Model
**Entity**: AgentQuery
**Fields**:
- `query_id`: str - Unique identifier for the query
- `original_query`: str - The user's original question
- `processed_query`: str - Query after any preprocessing
- `retrieved_chunks`: List[RetrievedChunk] - Chunks retrieved from Qdrant
- `agent_response`: str - The agent's generated response
- `confidence_score`: float - Agent's confidence in the response
- `timestamp`: datetime - When the query was processed

## Tool Response Model
**Entity**: ToolResponse
**Fields**:
- `tool_name`: str - Name of the tool that was called
- `status`: str - Success or failure status
- `retrieved_content`: List[RetrievedChunk] - Content retrieved by the tool
- `execution_time_ms`: float - Time taken to execute the tool
- `error_message`: Optional[str] - Error details if status is failure

## Validation Test Model
**Entity**: ValidationTest
**Fields**:
- `test_id`: str - Unique identifier for the test
- `query`: str - The question to ask the agent
- `expected_keywords`: List[str] - Keywords expected in the response
- `expected_module`: str - Expected source module for the answer
- `min_relevance_threshold`: float - Minimum relevance score required
- `test_category`: str - Category of the test (e.g., "factual", "contextual")
- `expected_outcome`: str - Expected result of the test

## State Management Model
**Entity**: AgentState
**Fields**:
- `session_id`: str - Unique identifier for the conversation session
- `history`: List[Dict] - Conversation history with user and agent messages
- `context_chunks`: List[RetrievedChunk] - Chunks currently in context
- `last_query_time`: datetime - Time of last query
- `context_ttl`: int - Time-to-live for context in seconds