# Quickstart Guide: RAG Chatbot API Integration

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Docusaurus frontend)
- Poetry or pip for Python dependency management
- Existing RAG agent implementation in agent.py

## Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install fastapi uvicorn python-multipart
   ```

2. **Create the FastAPI application** (`backend/api.py`):
   ```python
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from typing import List, Optional
   import agent  # Import the existing RAG agent
   import datetime

   app = FastAPI(title="RAG Chatbot API")

   class QueryRequest(BaseModel):
       message: str
       session_id: Optional[str] = None

   class ChatResponse(BaseModel):
       response: str
       sources: List[str]
       timestamp: str
       grounding_confidence: Optional[float] = None

   class ApiResponse(BaseModel):
       success: bool
       data: Optional[ChatResponse] = None
       error: Optional[str] = None

   @app.post("/chat", response_model=ApiResponse)
   async def chat_endpoint(query: QueryRequest):
       try:
           # Validate input
           if not query.message or not query.message.strip():
               raise HTTPException(status_code=400,
                                 detail="Query message is required and cannot be empty")

           # Process query through RAG agent
           response = agent.process_query(query.message)

           # Format response
           chat_response = ChatResponse(
               response=response.get('answer', ''),
               sources=response.get('sources', []),
               timestamp=datetime.datetime.now().isoformat(),
               grounding_confidence=response.get('confidence', None)
           )

           return ApiResponse(success=True, data=chat_response)
       except Exception as e:
           return ApiResponse(success=False, error=str(e))

   @app.get("/health")
   async def health_check():
       return {"status": "healthy"}
   ```

3. **Run the backend server**:
   ```bash
   cd backend
   uvicorn api:app --reload --port 8000
   ```

## Frontend Setup

1. **Create the chatbot component** (`book_frontend/src/components/Chatbot/Chatbot.jsx`):
   ```jsx
   import React, { useState } from 'react';
   import './Chatbot.css';

   const Chatbot = () => {
     const [messages, setMessages] = useState([]);
     const [inputValue, setInputValue] = useState('');
     const [isLoading, setIsLoading] = useState(false);

     const handleSubmit = async (e) => {
       e.preventDefault();
       if (!inputValue.trim()) return;

       // Add user message to chat
       const userMessage = { type: 'user', content: inputValue, timestamp: new Date() };
       setMessages(prev => [...prev, userMessage]);
       setInputValue('');
       setIsLoading(true);

       try {
         const response = await fetch('http://localhost:8000/chat', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ message: inputValue })
         });

         const data = await response.json();

         if (data.success) {
           const botMessage = {
             type: 'bot',
             content: data.data.response,
             sources: data.data.sources,
             timestamp: new Date()
           };
           setMessages(prev => [...prev, botMessage]);
         } else {
           const errorMessage = {
             type: 'error',
             content: data.error || 'An error occurred',
             timestamp: new Date()
           };
           setMessages(prev => [...prev, errorMessage]);
         }
       } catch (error) {
         const errorMessage = {
           type: 'error',
           content: 'Failed to connect to chatbot service',
           timestamp: new Date()
         };
         setMessages(prev => [...prev, errorMessage]);
       } finally {
         setIsLoading(false);
       }
     };

     return (
       <div className="chatbot-container">
         <div className="chatbot-messages">
           {messages.map((msg, index) => (
             <div key={index} className={`message ${msg.type}`}>
               <div className="message-content">{msg.content}</div>
               {msg.sources && msg.sources.length > 0 && (
                 <div className="sources">
                   Sources: {msg.sources.join(', ')}
                 </div>
               )}
             </div>
           ))}
           {isLoading && <div className="message bot">Thinking...</div>}
         </div>
         <form onSubmit={handleSubmit} className="chatbot-input-form">
           <input
             type="text"
             value={inputValue}
             onChange={(e) => setInputValue(e.target.value)}
             placeholder="Ask about the book content..."
             disabled={isLoading}
           />
           <button type="submit" disabled={isLoading}>
             Send
           </button>
         </form>
       </div>
     );
   };

   export default Chatbot;
   ```

2. **Add CSS styling** (`book_frontend/src/components/Chatbot/Chatbot.css`):
   ```css
   .chatbot-container {
     position: fixed;
     bottom: 20px;
     right: 20px;
     width: 350px;
     height: 500px;
     border: 1px solid #ccc;
     border-radius: 8px;
     display: flex;
     flex-direction: column;
     background: white;
     box-shadow: 0 4px 12px rgba(0,0,0,0.15);
     z-index: 1000;
   }

   .chatbot-messages {
     flex: 1;
     overflow-y: auto;
     padding: 15px;
   }

   .message {
     margin-bottom: 10px;
     padding: 8px 12px;
     border-radius: 8px;
     max-width: 80%;
   }

   .message.user {
     background-color: #e3f2fd;
     margin-left: auto;
   }

   .message.bot {
     background-color: #f5f5f5;
   }

   .message.error {
     background-color: #ffebee;
     color: #c62828;
   }

   .sources {
     font-size: 0.8em;
     color: #666;
     margin-top: 5px;
   }

   .chatbot-input-form {
     display: flex;
     padding: 10px;
     border-top: 1px solid #eee;
   }

   .chatbot-input-form input {
     flex: 1;
     padding: 8px;
     border: 1px solid #ccc;
     border-radius: 4px;
     margin-right: 5px;
   }

   .chatbot-input-form button {
     padding: 8px 15px;
     background-color: #1976d2;
     color: white;
     border: none;
     border-radius: 4px;
     cursor: pointer;
   }

   .chatbot-input-form button:disabled {
     background-color: #bbdefb;
     cursor: not-allowed;
   }
   ```

3. **Integrate the component globally** in Docusaurus by modifying the theme configuration.

## Testing

1. **Start the backend**:
   ```bash
   cd backend
   uvicorn api:app --reload --port 8000
   ```

2. **Test the API directly**:
   ```bash
   curl -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "What are the key principles of humanoid robotics?"}'
   ```

3. **Start the frontend** (in a separate terminal):
   ```bash
   cd book_frontend
   npm start
   ```

4. **Verify functionality** by using the chatbot interface on any page of the book.