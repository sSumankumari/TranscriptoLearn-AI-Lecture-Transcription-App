import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, MessageCircle, User, Bot, Loader2 } from 'lucide-react';

const ChatBot = ({ videoId }) => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: 'Hello! I can answer questions about this video. What would you like to know?',
      timestamp: new Date()
    }
  ]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!currentQuestion.trim()) return;

    const userMessage = {
      type: 'user',
      content: currentQuestion,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentQuestion('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/ask-question', {
        video_id: videoId,
        question: currentQuestion
      });

      const botMessage = {
        type: 'bot',
        content: response.data.answer,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const suggestedQuestions = [
    "What are the main topics covered in this video?",
    "Can you explain the key concepts?",
    "What are the important takeaways?",
    "Are there any examples given?"
  ];

  const handleSuggestedQuestion = (question) => {
    setCurrentQuestion(question);
  };

  return (
    <div className="flex flex-col h-96 border border-gray-200 rounded-lg">
      {/* Header */}
      <div className="flex items-center space-x-2 p-4 border-b border-gray-200 bg-gray-50 rounded-t-lg">
        <MessageCircle className="text-blue-500" size={20} />
        <h3 className="font-semibold text-gray-800">Ask Questions About This Video</h3>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex space-x-2 max-w-xs lg:max-w-md ${
              message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
            }`}>
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-blue-500 text-white' 
                  : message.isError 
                    ? 'bg-red-500 text-white'
                    : 'bg-gray-300 text-gray-700'
              }`}>
                {message.type === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              
              <div className={`px-4 py-2 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-500 text-white'
                  : message.isError
                    ? 'bg-red-100 text-red-800 border border-red-300'
                    : 'bg-gray-100 text-gray-800'
              }`}>
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <p className={`text-xs mt-1 ${
                  message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  {formatTime(message.timestamp)}
                </p>
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="flex space-x-2">
              <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <Bot size={16} />
              </div>
              <div className="bg-gray-100 px-4 py-2 rounded-lg flex items-center space-x-2">
                <Loader2 className="animate-spin" size={16} />
                <span className="text-sm text-gray-600">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions (only show if no messages from user yet) */}
      {messages.length === 1 && (
        <div className="p-3 border-t border-gray-200 bg-gray-50">
          <p className="text-xs text-gray-600 mb-2">Suggested questions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuestion(question)}
                className="text-xs px-2 py-1 bg-white border border-gray-300 rounded-full hover:bg-blue-50 hover:border-blue-300 transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={currentQuestion}
            onChange={(e) => setCurrentQuestion(e.target.value)}
            placeholder="Ask a question about this video..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!currentQuestion.trim() || isLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center"
          >
            {isLoading ? (
              <Loader2 className="animate-spin" size={16} />
            ) : (
              <Send size={16} />
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatBot;