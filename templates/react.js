import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io.connect('https://127.0.0.1:4444');

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    socket.on('bot_response', response => {
      setMessages([...messages, { author: 'bot', message: response }]);
    });
  }, [messages]);

  const handleSubmit = event => {
    event.preventDefault();
    setMessages([...messages, { author: 'user', message: inputValue }]);
    socket.emit('message', inputValue);
    setInputValue('');
  };

  const handleChange = event => {
    setInputValue(event.target.value);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chatbot-message ${message.author}`}>
            <p>{message.message}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chatbot-input">
        <input
          type="text"
          value={inputValue}
          onChange={handleChange}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chatbot;
