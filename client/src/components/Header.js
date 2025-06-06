import React from 'react';
import { BookOpen, Brain } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <BookOpen size={32} className="text-white" />
              <Brain size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">TranscriptoLearn</h1>
              <p className="text-blue-100 text-sm">AI-Powered Lecture Learning Assistant</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
              <span>Powered by Groq & LLaMA 3</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;