// API service for chatbot communication
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ChatbotAPI {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async chat(message, sessionId = null) {
    try {
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Chat API error:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Health check error:', error);
      return { status: 'unhealthy', error: error.message };
    }
  }

  // Method to test API connectivity
  async testConnection() {
    try {
      const result = await this.healthCheck();
      return result.status === 'healthy';
    } catch (error) {
      return false;
    }
  }
}

// Create and export a singleton instance
const chatbotAPI = new ChatbotAPI();
export default chatbotAPI;

// Export the class for potential instantiation with custom config
export { ChatbotAPI };