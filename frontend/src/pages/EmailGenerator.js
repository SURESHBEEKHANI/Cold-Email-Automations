import React, { useState } from 'react';
import { Mail, Link as LinkIcon, FileText, Loader2, Copy, Download, Eye, EyeOff } from 'lucide-react';
import EmailForm from '../components/EmailForm';
import EmailResults from '../components/EmailResults';
import LoadingSpinner from '../components/LoadingSpinner';

const EmailGenerator = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('url');

  const handleGenerateEmails = async (formData) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('/generate-emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate emails');
      }

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Generate Cold Emails
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Paste a job URL or description to automatically extract job details and generate 
          personalized cold emails using AI-powered agents.
        </p>
      </div>

      {/* Main Content */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center mb-6">
            <Mail className="h-6 w-6 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Input Job Information</h2>
          </div>

          {/* Tab Navigation */}
          <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setActiveTab('url')}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'url'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <LinkIcon className="h-4 w-4 mr-2" />
              Job URL
            </button>
            <button
              onClick={() => setActiveTab('description')}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'description'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <FileText className="h-4 w-4 mr-2" />
              Job Description
            </button>
          </div>

          <EmailForm
            activeTab={activeTab}
            onSubmit={handleGenerateEmails}
            isLoading={isLoading}
            onReset={handleReset}
          />
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center mb-6">
            <Mail className="h-6 w-6 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Generated Emails</h2>
          </div>

          {isLoading && (
            <div className="flex items-center justify-center py-12">
              <LoadingSpinner />
              <span className="ml-3 text-gray-600">Generating emails...</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <p className="mt-1 text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}

          {results && !isLoading && (
            <EmailResults results={results} />
          )}

          {!results && !isLoading && !error && (
            <div className="text-center py-12 text-gray-500">
              <Mail className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Generated emails will appear here</p>
            </div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">How it works</h3>
        <div className="grid md:grid-cols-3 gap-4 text-sm text-blue-800">
          <div className="flex items-start">
            <span className="flex items-center justify-center w-6 h-6 bg-blue-600 text-white text-xs rounded-full mr-3 mt-0.5">1</span>
            <span>AI analyzes the job posting and extracts key requirements</span>
          </div>
          <div className="flex items-start">
            <span className="flex items-center justify-center w-6 h-6 bg-blue-600 text-white text-xs rounded-full mr-3 mt-0.5">2</span>
            <span>Matches your portfolio projects with job requirements</span>
          </div>
          <div className="flex items-start">
            <span className="flex items-center justify-center w-6 h-6 bg-blue-600 text-white text-xs rounded-full mr-3 mt-0.5">3</span>
            <span>Generates personalized cold emails with relevant examples</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailGenerator; 