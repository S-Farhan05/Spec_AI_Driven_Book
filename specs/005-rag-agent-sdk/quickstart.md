# Quickstart: RAG Agent Construction with OpenAI Agent SDK

## Prerequisites

1. **Python Environment**: Python 3.11 or higher
2. **API Keys**:
   - OpenAI API key with Agent SDK access
   - Qdrant Cloud URL and API key for your vector database
3. **Dependencies**: Install required packages
4. **Pre-indexed Content**: Book content must already be stored in Qdrant

## Setup

### 1. Install Dependencies
```bash
pip install openai-agent-sdk qdrant-client python-dotenv pydantic cohere requests
```

### 2. Configure Environment Variables
Create a `.env` file in your project root:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key  # For query embedding if needed
```

### 3. Prepare Qdrant Collection
Ensure your book content is stored in Qdrant with proper metadata (URL, module, section).

## Running the Agent

### 1. Basic Usage
```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Ask a question about your book content
response = agent.query("What is digital twin simulation?")
print(response.answer)
print(f"Confidence: {response.confidence_score}")
print(f"Sources: {response.sources}")
```

### 2. Interactive Mode
```python
from agent import RAGAgent

agent = RAGAgent()

while True:
    user_input = input("Ask a question about the book: ")
    if user_input.lower() in ['quit', 'exit']:
        break

    response = agent.query(user_input)
    print(f"Answer: {response.answer}")
    print(f"Sources: {response.sources}")
```

## Key Components

### Agent Architecture
- **OpenAI Agent SDK**: Core agent functionality
- **Qdrant Tool**: Custom retrieval tool that fetches relevant content
- **Context Manager**: Ensures responses are grounded in retrieved content
- **Response Validator**: Ensures quality and relevance of responses

### Retrieval Process
1. User query is processed and converted to embeddings
2. Qdrant tool performs semantic search in the vector database
3. Relevant chunks are retrieved based on similarity scores
4. Agent generates response using retrieved context
5. Response is validated for accuracy and attribution

## Validation

### Test Sample Queries
```python
from agent import RAGAgent

agent = RAGAgent()

test_queries = [
    "What is digital twin simulation?",
    "Explain ROS2 navigation",
    "How does VLA work?",
    "What are Isaac modules?"
]

for query in test_queries:
    response = agent.query(query)
    print(f"Query: {query}")
    print(f"Answer: {response.answer[:200]}...")
    print(f"Relevance: {response.confidence_score}")
    print("---")
```

## Configuration Options

### Customization Parameters
- `top_k`: Number of chunks to retrieve (default: 5)
- `relevance_threshold`: Minimum relevance score (default: 0.5)
- `model_name`: OpenAI model to use (default: "gpt-4")

### Example Custom Configuration
```python
agent = RAGAgent(
    retrieval_top_k=3,
    relevance_threshold=0.6,
    model_name="gpt-4-turbo"
)
```

## Troubleshooting

### Common Issues
1. **No Results**: Check that your Qdrant collection contains the expected content
2. **Low Relevance**: Adjust the relevance threshold or check embedding consistency
3. **API Errors**: Verify your API keys are correct and have sufficient permissions

### Performance Tips
- Optimize your embeddings to match the query format
- Use appropriate top_k values based on content complexity
- Monitor token usage to manage costs