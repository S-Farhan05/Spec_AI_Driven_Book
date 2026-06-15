import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import datetime
import traceback
from models.chat import ChatRequest, ChatResponse as ChatResponseModel, ChatAPIResponse

# Import the RAG agent
import agent

app = FastAPI(title="RAG Chatbot API")

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://spec-ai-driven-book.vercel.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for the API"""
    error_msg = f"An unexpected error occurred: {str(exc)}"
    print(error_msg)  # For debugging
    print(traceback.format_exc())  # Print full traceback

    response = ChatAPIResponse(
        success=False,
        error=error_msg
    )
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler for the API"""
    response = ChatAPIResponse(
        success=False,
        error=f"HTTP Error {exc.status_code}: {exc.detail}"
    )
    return response

@app.post("/chat", response_model=ChatAPIResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """Chat endpoint that forwards queries to the RAG agent and returns responses"""
    try:
        # Validate input
        if not chat_request.message or not chat_request.message.strip():
            raise HTTPException(status_code=400,
                              detail="Query message is required and cannot be empty")

        # Process query through RAG agent with timeout
        try:
            # Set a timeout for the agent query (e.g., 30 seconds)
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, agent.query_agent, chat_request.message),
                timeout=30.0  # 30 seconds timeout
            )
        except asyncio.TimeoutError:
            return ChatAPIResponse(
                success=False,
                error="Request timeout: The query took too long to process"
            )

        # Format response
        chat_response = ChatResponseModel(
            response=result.agent_response,
            sources=[chunk.url for chunk in result.retrieved_chunks if chunk.url] if result.retrieved_chunks else [],
            timestamp=datetime.datetime.now().isoformat(),
            grounding_confidence=result.confidence_score
        )

        return ChatAPIResponse(success=True, data=chat_response)
    except HTTPException:
        raise
    except Exception as e:
        return ChatAPIResponse(success=False, error=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)