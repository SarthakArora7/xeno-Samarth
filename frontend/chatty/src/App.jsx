import React, { useState, useRef, useEffect } from 'react';

const SimpleChatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Function to convert URLs to clickable links
  const renderTextWithLinks = (text) => {
    if (!text) return text;
    
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);
    
    return parts.map((part, index) => {
      if (part.match(urlRegex)) {
        return (
          <a
            key={index}
            href={part}
            target="_blank"
            rel="noopener noreferrer"
            style={styles.link}
          >
            {part}
          </a>
        );
      }
      return part;
    });
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    // Add user message
    const userMessage = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call your Flask backend
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      
      const data = await response.json();
      
      // Add bot response with rendered links
      setMessages(prev => [...prev, { text: data.reply, sender: 'bot' }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        text: "Sorry, I'm having trouble connecting to the chatbot.", 
        sender: 'bot' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatContainer}>
        <div style={styles.messages}>
          {messages.map((msg, index) => (
            <div 
              key={index} 
              style={{
                ...styles.message,
                ...(msg.sender === 'user' ? styles.userMessage : styles.botMessage)
              }}
            >
              {renderTextWithLinks(msg.text)}
            </div>
          ))}
          <div ref={messagesEndRef} />
          {isLoading && (
            <div style={styles.botMessage}>
              <div style={styles.typingIndicator}>
                <span>•</span><span>•</span><span>•</span>
              </div>
            </div>
          )}
        </div>
        
        <div style={styles.inputContainer}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your question..."
            style={styles.input}
            disabled={isLoading}
          />
          <button 
            onClick={handleSend} 
            style={styles.button}
            disabled={isLoading || !input.trim()}
          >
            Ask
          </button>
        </div>
      </div>
    </div>
  );
};

// Updated styles with link styling
const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px'
  },
  chatContainer: {
    width: '100%',
    maxWidth: '600px',
    height: '80vh',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    overflow: 'hidden'
  },
  messages: {
    flex: 1,
    padding: '20px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  message: {
    maxWidth: '80%',
    padding: '12px 16px',
    borderRadius: '18px',
    lineHeight: '1.4',
    wordBreak: 'break-word',
    whiteSpace: 'pre-wrap' // Preserve line breaks and spaces
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007bff',
    color: 'white',
    borderBottomRightRadius: '4px',
    '& a': {
      color: '#cce4ff',
      textDecoration: 'underline'
    }
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#f0f0f0',
    color: '#333',
    borderBottomLeftRadius: '4px',
    '& a': {
      color: '#0066cc',
      textDecoration: 'underline'
    }
  },
  link: {
    color: '#0066cc',
    textDecoration: 'underline',
    wordBreak: 'break-all' // Ensure long URLs don't overflow
  },
  inputContainer: {
    display: 'flex',
    padding: '12px',
    borderTop: '1px solid #eee',
    backgroundColor: 'white'
  },
  input: {
    flex: 1,
    padding: '12px',
    border: '1px solid #ddd',
    borderRadius: '24px',
    outline: 'none',
    fontSize: '16px'
  },
  button: {
    marginLeft: '12px',
    padding: '0 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '24px',
    cursor: 'pointer',
    fontSize: '16px',
    transition: 'background-color 0.2s',
    ':disabled': {
      backgroundColor: '#cccccc',
      cursor: 'not-allowed'
    }
  },
  typingIndicator: {
    display: 'flex',
    gap: '4px',
    'span': {
      fontSize: '32px',
      opacity: 0,
      animation: 'typingAnimation 1.4s infinite'
    },
    'span:nth-child(1)': { animationDelay: '0s' },
    'span:nth-child(2)': { animationDelay: '0.2s' },
    'span:nth-child(3)': { animationDelay: '0.4s' }
  }
};

export default SimpleChatbot;