import React from 'react';
import Chatbot from '../Chatbot/Chatbot';

const LayoutWrapper = ({ children }) => {
  return (
    <div style={{ position: 'relative' }}>
      {children}
      <div style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 1000
      }}>
        <Chatbot />
      </div>
    </div>
  );
};

export default LayoutWrapper;