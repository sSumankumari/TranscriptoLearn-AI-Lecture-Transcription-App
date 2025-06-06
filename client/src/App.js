import React, { useState } from 'react';
import VideoProcessor from './components/VideoProcessor';
import NotesDisplay from './components/NotesDisplay';
import ChatBot from './components/ChatBot';
import Header from './components/Header';
import LoadingSpinner from './components/LoadingSpinner';
import './App.css';

function App() {
  const [videoData, setVideoData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('notes');

  const handleVideoProcessed = (data) => {
    setVideoData(data);
    setError('');
    setActiveTab('notes');
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setVideoData(null);
  };

  const handleLoading = (isLoading) => {
    setLoading(isLoading);
  };

  return (
    <div className="App">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <VideoProcessor 
          onVideoProcessed={handleVideoProcessed}
          onError={handleError}
          onLoading={handleLoading}
        />

        {loading && <LoadingSpinner />}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

        {videoData && (
          <div className="mt-8">
            {/* Video Info */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {videoData.video_info.title}
              </h2>
              <div className="flex items-center text-gray-600 text-sm">
                <span className="mr-4">
                  <strong>Duration:</strong> {Math.floor(videoData.video_info.duration / 60)}:{(videoData.video_info.duration % 60).toString().padStart(2, '0')}
                </span>
                <span>
                  <strong>Uploader:</strong> {videoData.video_info.uploader}
                </span>
              </div>
            </div>

            {/* Tab Navigation */}
            <div className="bg-white rounded-lg shadow-md mb-6">
              <div className="flex border-b">
                <button
                  className={`flex-1 py-3 px-6 text-center font-medium transition-colors ${
                    activeTab === 'notes' 
                      ? 'bg-blue-500 text-white' 
                      : 'text-gray-600 hover:text-blue-500'
                  }`}
                  onClick={() => setActiveTab('notes')}
                >
                  Smart Notes
                </button>
                <button
                  className={`flex-1 py-3 px-6 text-center font-medium transition-colors ${
                    activeTab === 'summary' 
                      ? 'bg-blue-500 text-white' 
                      : 'text-gray-600 hover:text-blue-500'
                  }`}
                  onClick={() => setActiveTab('summary')}
                >
                  Summary
                </button>
                <button
                  className={`flex-1 py-3 px-6 text-center font-medium transition-colors ${
                    activeTab === 'chat' 
                      ? 'bg-blue-500 text-white' 
                      : 'text-gray-600 hover:text-blue-500'
                  }`}
                  onClick={() => setActiveTab('chat')}
                >
                  Q&A Chat
                </button>
                <button
                  className={`flex-1 py-3 px-6 text-center font-medium transition-colors ${
                    activeTab === 'transcript' 
                      ? 'bg-blue-500 text-white' 
                      : 'text-gray-600 hover:text-blue-500'
                  }`}
                  onClick={() => setActiveTab('transcript')}
                >
                  Transcript
                </button>
              </div>

              <div className="p-6">
                {activeTab === 'notes' && (
                  <NotesDisplay content={videoData.notes} title="Smart Notes" />
                )}
                {activeTab === 'summary' && (
                  <NotesDisplay content={videoData.summary} title="Summary" />
                )}
                {activeTab === 'chat' && (
                  <ChatBot videoId={videoData.video_id} />
                )}
                {activeTab === 'transcript' && (
                  <NotesDisplay content={videoData.transcript} title="Full Transcript" />
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;