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

  const formatTime = (seconds) => {
    if (!seconds) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
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
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 fade-in">
            <strong>Error:</strong> {error}
          </div>
        )}

        {videoData && (
          <div className="mt-8 fade-in">
            {/* Video Info */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {videoData.video_info?.title || 'Video Title'}
              </h2>
              <div className="flex items-center text-gray-600 text-sm space-x-4">
                <span>
                  <strong>Duration:</strong> {formatTime(videoData.video_info?.duration)}
                </span>
                <span>
                  <strong>Channel:</strong> {videoData.video_info?.uploader || 'Unknown'}
                </span>
              </div>
            </div>

            {/* Tab Navigation */}
            <div className="bg-white rounded-lg shadow-md mb-6">
              <div className="flex border-b">
                {[
                  { key: 'notes', label: 'Smart Notes', icon: '📝' },
                  { key: 'summary', label: 'Summary', icon: '📋' },
                  { key: 'chat', label: 'Q&A Chat', icon: '💬' },
                  { key: 'transcript', label: 'Transcript', icon: '📄' }
                ].map((tab) => (
                  <button
                    key={tab.key}
                    className={`flex-1 py-3 px-6 text-center font-medium transition-all duration-200 ${
                      activeTab === tab.key 
                        ? 'bg-blue-500 text-white border-b-2 border-blue-600' 
                        : 'text-gray-600 hover:text-blue-500 hover:bg-gray-50'
                    }`}
                    onClick={() => setActiveTab(tab.key)}
                  >
                    <span className="mr-2">{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </div>

              <div className="p-6">
                <div className="tab-content">
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
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">
            Powered by <span className="text-blue-400">Groq API</span> & <span className="text-purple-400">LLaMA 3</span>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;