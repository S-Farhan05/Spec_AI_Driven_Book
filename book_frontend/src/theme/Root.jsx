import React, { useEffect, useState } from 'react';
import Chatbot from '../components/Chatbot/Chatbot';

// Root component that wraps the entire Docusaurus application
export default function Root({children}) {
  const [isClient, setIsClient] = useState(false);
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  useEffect(() => {
    // Ensure we're on the client side before rendering
    setIsClient(true);
  }, []);

  const toggleChatbot = () => {
    setIsChatbotOpen(!isChatbotOpen);
  };

  // Add styles for animations
  useEffect(() => {
    if (isClient) {
      // Create style element for keyframe animations
      const styleId = 'chatbot-animations';
      if (!document.getElementById(styleId)) {
        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = `
          @keyframes blinkingText {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
          }

          @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }

          .chatbot-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6), 0 0 30px rgba(102, 126, 234, 0.5);
          }
        `;
        document.head.appendChild(style);
      }
    }
  }, [isClient]);

  return (
    <>
      {children}
      {isClient && (
        <div>
          {/* Chatbot Toggle Button */}
          {!isChatbotOpen && (
            <div style={{
              position: 'fixed',
              bottom: '20px',
              right: '20px',
              zIndex: 1000,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center'
            }}>
              <div style={{
                backgroundColor: 'transparent',
                padding: '2px 8px',
                borderRadius: '10px',
                fontSize: '12px',
                marginBottom: '5px',
                whiteSpace: 'nowrap',
                animation: 'blinkingText 2s infinite'
              }}>
                <span style={{
                  background: 'linear-gradient(45deg, #667eea, #764ba2)',
                  backgroundSize: '300% 300%',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  animation: 'gradientShift 3s ease infinite',
                  fontWeight: 'bold',
                  textShadow: '0 0 5px rgba(255,255,255,0.5)'
                }}>
                  AI Assistant
                </span>
              </div>
              <button
                onClick={toggleChatbot}
                className="chatbot-button"
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '60px',
                  height: '60px',
                  fontSize: '24px',
                  cursor: 'pointer',
                  boxShadow: '0 6px 16px rgba(102, 126, 234, 0.4), 0 0 20px rgba(102, 126, 234, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transition: 'all 0.3s ease',
                  position: 'relative',
                  overflow: 'hidden'
                }}
                aria-label="Open chatbot"
              >
                <span style={{
                  position: 'relative',
                  zIndex: 1
                }}>
                  🤖
                </span>
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  background: 'radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 70%)',
                  opacity: 0.3,
                  zIndex: 0
                }}></div>
              </button>
            </div>
          )}

          {/* Chatbot Container */}
          {isChatbotOpen && (
            <div style={{
              position: 'fixed',
              bottom: '20px',
              right: '20px',
              zIndex: 1000,
              boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)',
              borderRadius: '16px',
              width: '400px',
              height: '500px',
              overflow: 'hidden',
              background: 'linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%)',
              border: '1px solid #444'
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '16px 20px',
                background: 'linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%)',
                color: 'white',
                borderBottom: '1px solid #333'
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px'
                }}>
                  <div style={{
                    width: '28px',
                    height: '28px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '14px'
                  }}>
                    🤖
                  </div>
                  <div>
                    <div style={{
                      fontSize: '15px',
                      fontWeight: '600',
                      background: 'linear-gradient(45deg, #667eea, #764ba2)',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      backgroundClip: 'text',
                      margin: 0
                    }}>
                      AI Assistant
                    </div>
                    <div style={{
                      fontSize: '10px',
                      color: '#888',
                      marginTop: '-4px'
                    }}>
                      Online
                    </div>
                  </div>
                </div>
                <button
                  onClick={toggleChatbot}
                  style={{
                    background: 'rgba(255, 255, 255, 0.1)',
                    border: 'none',
                    color: '#e0e0e0',
                    fontSize: '18px',
                    cursor: 'pointer',
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.2s ease',
                    marginLeft: '10px'
                  }}
                  aria-label="Close chatbot"
                >
                  ×
                </button>
              </div>
              <div style={{
                height: 'calc(100% - 60px)',
                overflow: 'hidden'
              }}>
                <Chatbot />
              </div>
            </div>
          )}
        </div>
      )}
    </>
  );
}