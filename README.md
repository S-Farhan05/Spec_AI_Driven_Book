"# AI-Powered Documentation Platform

An AI-powered documentation platform built with Docusaurus, featuring an embedded Retrieval-Augmented Generation (RAG) chatbot. The chatbot answers questions strictly from the book's content and supports a special mode where answers are generated only from user-selected text.

## 🚀 Project Overview

This project aims to help users explore and understand large technical documentation using AI without hallucinations. The platform provides context-aware Q&A based on your documentation content, leveraging advanced retrieval techniques to ensure accurate and reliable responses.

## 🛠️ Tech Stack

- **Docusaurus** - Documentation Frontend
- **FastAPI** - Backend API Framework
- **OpenAI Agents / ChatKit** - AI Processing
- **Qdrant Cloud** - Vector Database for semantic search
- **Neon Serverless PostgreSQL** - Relational Database
- **Python** - Backend Language
- **Embedded Chat UI** - Interactive question answering

## ✨ Key Features

- **Context-aware Q&A** - Answers based only on your documentation content
- **Retrieval-based answering** - Uses vector search for semantic understanding
- **Selected-text-only mode** - Answers generated only from user-selected text
- **Hallucination prevention** - Strict context grounding ensures accuracy
- **Clean architecture** - Well-separated frontend, backend, and retrieval layers
- **Real-time interaction** - Interactive chat interface for seamless experience

## 🏗️ Architecture

The platform follows a clean separation of concerns:
- **Frontend**: Docusaurus-based documentation site with embedded chat UI
- **Backend**: FastAPI services handling AI processing and vector database interactions
- **Storage**: Qdrant Cloud for vector embeddings, Neon PostgreSQL for metadata
- **AI Layer**: OpenAI Agents for natural language processing and response generation

## 🚀 Setup Instructions

### Prerequisites
- Node.js (for Docusaurus frontend)
- Python 3.8+ (for FastAPI backend)
- API keys for OpenAI and Qdrant Cloud
- PostgreSQL connection (Neon Serverless)

### Frontend Setup
```bash
cd book_frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Run the chatbot API server (required for frontend)
uvicorn api:app --reload

# Or alternatively:
python api.py
```

The backend will run on `http://localhost:8000`

**Note:** If port 8000 is already in use by another application, specify a different port:
```bash
uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

### Environment Variables
Create a `.env` file with the following:
```
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgresql_url
```

## 📖 Usage

1. **Standard Q&A Mode**: Ask questions about your documentation content
2. **Selected-text-only Mode**: Highlight specific text and ask questions limited to that context
3. **Search**: Use the vector search to find relevant documentation sections
4. **Chat History**: Review previous conversations and responses

## 🎯 Special Features

### Selected-Text-Only Mode
The platform includes a unique feature where users can select specific text portions and ask questions that are answered strictly from the selected context. This provides granular control over the AI's response source and ensures maximum relevance.

### Hallucination Prevention
The system implements strict context grounding mechanisms to prevent AI hallucinations, ensuring all responses are based on actual documentation content.

## 🏗️ Development

The project is structured to allow easy extension and customization:
- Easy integration with different documentation formats
- Configurable AI model settings
- Pluggable vector database support
- Customizable UI components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 👥 Author
Syed Farhan Iqbal (Owner)


