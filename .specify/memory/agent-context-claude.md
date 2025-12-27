# Agent Context: RAG Chatbot API Integration

## Project Context
- **Feature**: RAG Chatbot API Integration
- **Branch**: 001-rag-chatbot-api-integration
- **Date**: 2025-12-27
- **Technology Stack**: FastAPI, Docusaurus, React, OpenAI Agent SDK

## Backend Components
- **api.py**: FastAPI application with chat endpoint
- **agent.py**: RAG agent implementation (existing)
- **requirements.txt**: Python dependencies (FastAPI, uvicorn, etc.)

## Frontend Components
- **book_frontend/src/components/Chatbot/**: Global chatbot UI component
- **book_frontend/src/services/api.js**: API communication service
- **Docusaurus integration**: Global component injection

## API Contract
- **Endpoint**: POST /chat
- **Request**: { message: string, session_id?: string }
- **Response**: { success: boolean, data?: { response: string, sources: string[], timestamp: string, grounding_confidence?: number }, error?: string }

## Key Requirements
- Content-grounded responses only
- Error handling and timeouts
- Global availability across all book pages
- Consistent UI/UX experience
- Integration with existing RAG agent

## Files Created/Modified
- backend/api.py
- book_frontend/src/components/Chatbot/Chatbot.jsx
- book_frontend/src/components/Chatbot/Chatbot.css
- specs/001-rag-chatbot-api-integration/plan.md
- specs/001-rag-chatbot-api-integration/research.md
- specs/001-rag-chatbot-api-integration/data-model.md
- specs/001-rag-chatbot-api-integration/contracts/api-contract.yaml
- specs/001-rag-chatbot-api-integration/quickstart.md