import React from 'react';
import { Brain, BookOpen } from 'lucide-react';

const LoadingSpinner = () => {
  return (
    <div className="bg-white rounded-lg shadow-md p-8 text-center">
      <div className="flex items-center justify-center space-x-4 mb-4">
        <div className="relative">
          <Brain className="text-blue-500 animate-pulse" size={40} />
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
        </div>
        <BookOpen className="text-purple-500 animate-bounce" size={40} />
      </div>
      
      <h3 className="text-xl font-semibold text-gray-800 mb-2">
        Processing Your Video
      </h3>
      
      <div className="space-y-2 text-sm text-gray-600 mb-6">
        <p>🎬 Extracting transcript from YouTube</p>
        <p>🧠 Analyzing content with AI</p>
        <p>📝 Generating smart notes and summary</p>
        <p>💡 Preparing Q&A capabilities</p>
      </div>

      {/* Progress Animation */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
        <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full animate-pulse" style={{width: '75%'}}></div>
      </div>

      <p className="text-xs text-gray-500">
        This may take 30-60 seconds depending on video length...
      </p>
    </div>
  );
};

export default LoadingSpinner;