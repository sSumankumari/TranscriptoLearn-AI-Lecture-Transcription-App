import React, { useState } from 'react';
import axios from 'axios';
import { Youtube, Send, AlertCircle } from 'lucide-react';

const VideoProcessor = ({ onVideoProcessed, onError, onLoading }) => {
  const [url, setUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const validateYouTubeUrl = (url) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    return youtubeRegex.test(url);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      onError('Please enter a YouTube URL');
      return;
    }

    if (!validateYouTubeUrl(url)) {
      onError('Please enter a valid YouTube URL');
      return;
    }

    setIsProcessing(true);
    onLoading(true);
    onError('');

    try {
      const response = await axios.post('http://localhost:5000/api/process-video', {
        url: url.trim()
      });

      if (response.data.success) {
        onVideoProcessed(response.data);
        setUrl(''); // Clear the input after successful processing
      } else {
        onError('Failed to process video');
      }
    } catch (error) {
      if (error.response) {
        onError(error.response.data.error || 'Server error occurred');
      } else if (error.request) {
        onError('Unable to connect to server. Please make sure the backend is running.');
      } else {
        onError('An unexpected error occurred');
      }
    } finally {
      setIsProcessing(false);
      onLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center space-x-3 mb-4">
        <Youtube className="text-red-500" size={28} />
        <h2 className="text-2xl font-bold text-gray-800">Process YouTube Video</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="video-url" className="block text-sm font-medium text-gray-700 mb-2">
            YouTube Video URL
          </label>
          <div className="relative">
            <input
              id="video-url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
              disabled={isProcessing}
            />
            <Youtube className="absolute right-3 top-3 text-gray-400" size={20} />
          </div>
        </div>

        <button
          type="submit"
          disabled={isProcessing || !url.trim()}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
        >
          {isProcessing ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Processing Video...</span>
            </>
          ) : (
            <>
              <Send size={20} />
              <span>Generate Notes & Summary</span>
            </>
          )}
        </button>
      </form>

      <div className="mt-4 p-4 bg-blue-50 rounded-md">
        <div className="flex items-start space-x-2">
          <AlertCircle className="text-blue-500 mt-0.5" size={16} />
          <div className="text-sm text-blue-700">
            <p className="font-medium mb-1">How it works:</p>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>Paste any YouTube lecture video URL</li>
              <li>AI extracts and processes the transcript</li>
              <li>Get structured notes, summary, and interactive Q&A</li>
              <li>Ask questions about the video content</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoProcessor;