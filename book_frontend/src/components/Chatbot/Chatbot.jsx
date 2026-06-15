import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize session and messages (without localStorage persistence)
  useEffect(() => {
    // Create a new session ID for each visit
    const newSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    setSessionId(newSessionId);

    // Always start with a fresh welcome message
    setMessages([
      {
        type: 'bot',
        content: 'Hello! I\'m your book assistant. Ask me anything about the humanoid robotics content.',
        timestamp: new Date()
      }
    ]);
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to retry API call with exponential backoff
  const fetchWithRetry = async (url, options, maxRetries = 3) => {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
      } catch (error) {
        if (attempt === maxRetries) {
          throw error; // If we've exhausted retries, throw the error
        }
        // Wait before retrying (exponential backoff: 1s, 2s, 4s)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 500));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !sessionId) return;

    // Add user message to chat
    const userMessage = {
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use retry logic for the API call
      const data = await fetchWithRetry('https://s-farhan-rag-backend.hf.space/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: inputValue,
          session_id: sessionId
        })
      }, 3); // Retry up to 3 times

      if (data.success && data.data) {
        let finalContent = data.data.response;
        const confidence = data.data.grounding_confidence;

        // If confidence is low, provide a more user-friendly message without technical jargon
        if (confidence !== undefined && confidence !== null && confidence < 0.5) {
          if (confidence < 0.2) {
            finalContent = "I couldn't find relevant information in the humanoid robotics book to answer your question. Please make sure your question is related to the book content about digital twins, ROS2, navigation, VLA models, or other humanoid robotics topics.";
          } else {
            finalContent += "\n\nNote: I found some related information, but it may not fully answer your question. For better results, try asking a more specific question about the humanoid robotics book content.";
          }
        }

        const botMessage = {
          type: 'bot',
          content: finalContent,
          sources: data.data.sources || [],
          timestamp: new Date(),
          confidence: data.data.grounding_confidence
        };

        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          type: 'error',
          content: data.error || 'An error occurred while processing your request',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: 'Failed to connect to the chatbot service. Please make sure the backend is running. The request failed after multiple attempts.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '16px'
          }}>
            🤖
          </div>
          <div>
            <h3 style={{
              margin: 0,
              fontSize: '16px',
              fontWeight: '600',
              background: 'linear-gradient(45deg, #667eea, #764ba2)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>
              AI Assistant
            </h3>
            <div style={{
              fontSize: '10px',
              color: '#888',
              marginTop: '-4px'
            }}>
              {isLoading ? 'Typing...' : 'Online'}
            </div>
          </div>
        </div>
        {isLoading && (
          <div className="loading-indicator">
            <div className="loading-spinner"></div>
          </div>
        )}
      </div>
      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-content">{msg.content}</div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong> {msg.sources.slice(0, 3).join(', ')}
                {msg.sources.length > 3 && ` and ${msg.sources.length - 3} more`}
              </div>
            )}
            {msg.confidence !== undefined && msg.confidence !== null && (
              <div className="confidence">
                Confidence: {(msg.confidence * 100).toFixed(1)}%
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span className="typing-indicator-text">Processing your query...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="chatbot-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={isLoading ? "Processing previous message..." : "Ask about the book content..."}
          disabled={isLoading}
          className={`chatbot-input ${isLoading ? 'disabled' : ''}`}
        />
        <button type="submit" disabled={isLoading} className={`chatbot-send-button ${isLoading ? 'disabled' : ''}`}>
          {isLoading ? (
            <>
              <span className="button-spinner"></span>
              Processing...
            </>
          ) : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chatbot;