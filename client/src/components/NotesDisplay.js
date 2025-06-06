import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Check, Download, FileText } from 'lucide-react';

const NotesDisplay = ({ content, title }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `${title.toLowerCase().replace(/\s+/g, '_')}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (!content) return null;

  return (
    <div className="space-y-4">
      {/* Header with actions */}
      <div className="flex items-center justify-between border-b border-gray-200 pb-3">
        <div className="flex items-center space-x-2">
          <FileText className="text-blue-500" size={20} />
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
          >
            {copied ? (
              <>
                <Check size={16} className="text-green-500" />
                <span className="text-green-500">Copied!</span>
              </>
            ) : (
              <>
                <Copy size={16} />
                <span>Copy</span>
              </>
            )}
          </button>
          
          <button
            onClick={handleDownload}
            className="flex items-center space-x-1 px-3 py-1.5 text-sm bg-blue-100 hover:bg-blue-200 rounded-md transition-colors"
          >
            <Download size={16} />
            <span>Download</span>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="prose prose-sm max-w-none">
        {title === 'Full Transcript' ? (
          <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
            {content}
          </div>
        ) : (
          <ReactMarkdown 
            className="markdown-content"
            components={{
              h1: ({children}) => <h1 className="text-2xl font-bold text-gray-900 mb-4">{children}</h1>,
              h2: ({children}) => <h2 className="text-xl font-semibold text-gray-800 mb-3 mt-6">{children}</h2>,
              h3: ({children}) => <h3 className="text-lg font-semibold text-gray-800 mb-2 mt-4">{children}</h3>,
              p: ({children}) => <p className="text-gray-700 mb-3 leading-relaxed">{children}</p>,
              ul: ({children}) => <ul className="list-disc list-inside mb-4 space-y-1 text-gray-700">{children}</ul>,
              ol: ({children}) => <ol className="list-decimal list-inside mb-4 space-y-1 text-gray-700">{children}</ol>,
              li: ({children}) => <li className="ml-2">{children}</li>,
              strong: ({children}) => <strong className="font-semibold text-gray-900">{children}</strong>,
              em: ({children}) => <em className="italic text-gray-800">{children}</em>,
              code: ({children}) => <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-gray-800">{children}</code>,
              blockquote: ({children}) => (
                <blockquote className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50 my-4 italic text-gray-700">
                  {children}
                </blockquote>
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        )}
      </div>

      {/* Word count */}
      <div className="text-xs text-gray-500 pt-3 border-t border-gray-100">
        Word count: {content.split(/\s+/).length} words
      </div>
    </div>
  );
};

export default NotesDisplay;