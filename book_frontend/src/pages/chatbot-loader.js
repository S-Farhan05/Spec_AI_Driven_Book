// This file is used to load the chatbot component on all pages
import React, { useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import Chatbot from '../components/Chatbot/Chatbot';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Function to initialize the chatbot when the DOM is ready
function initializeChatbot() {
  if (typeof document !== 'undefined') {
    const chatbotRoot = document.getElementById('chatbot-root');
    if (chatbotRoot) {
      const root = createRoot(chatbotRoot);
      root.render(<Chatbot />);
    }
  }
}

// Wait for the DOM to be fully loaded before initializing the chatbot
function ChatbotLoader() {
  useEffect(() => {
    if (typeof document !== 'undefined') {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeChatbot);
      } else {
        // DOM is already ready, initialize immediately
        initializeChatbot();
      }

      // Also handle potential dynamic content loading in SPAs
      if (typeof window !== 'undefined') {
        // For client-side navigation in Docusaurus
        window.addEventListener('load', initializeChatbot);

        // Listen for Docusaurus-specific events if available
        if (window.addEventListener) {
          window.addEventListener('routeChange', initializeChatbot);
        }
      }
    }
  }, []);

  return null;
}

// Export the component wrapped in BrowserOnly to ensure it only runs on the client
export default function ChatbotLoaderPage() {
  return <BrowserOnly>{() => <ChatbotLoader />}</BrowserOnly>;
}