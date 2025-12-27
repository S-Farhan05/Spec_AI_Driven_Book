from pydantic import BaseModel
from typing import List, Optional
import datetime


class Query(BaseModel):
    """Represents a user's input to the RAG chatbot system"""
    message: str
    timestamp: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().isoformat()


class Response(BaseModel):
    """Represents the RAG agent's response to a user query"""
    response: str
    sources: List[str]
    timestamp: str
    query_id: Optional[str] = None
    grounding_confidence: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().isoformat()


class APIRequest(BaseModel):
    """Structure of requests sent from frontend to backend"""
    query: Query
    options: Optional[dict] = None


class APIResponse(BaseModel):
    """Structure of responses sent from backend to frontend"""
    success: bool
    data: Optional[Response] = None
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().isoformat()