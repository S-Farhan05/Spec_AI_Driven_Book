from pydantic import BaseModel
from typing import List, Optional
import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    sources: List[str]
    timestamp: str
    grounding_confidence: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().isoformat()


class ChatAPIResponse(BaseModel):
    """API response wrapper for chat endpoint"""
    success: bool
    data: Optional[ChatResponse] = None
    error: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)