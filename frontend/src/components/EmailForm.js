import React, { useState } from 'react';
import { Link as LinkIcon, FileText, Send, RotateCcw } from 'lucide-react';

const EmailForm = ({ activeTab, onSubmit, isLoading, onReset }) => {
  const [formData, setFormData] = useState({
    url: '',
    job_description: ''
  });

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const data = activeTab === 'url' 
      ? { url: formData.url }
      : { job_description: formData.job_description };
    
    onSubmit(data);
  };

  const handleReset = () => {
    setFormData({
      url: '',
      job_description: ''
    });
    onReset();
  };

  const isFormValid = () => {
    if (activeTab === 'url') {
      return formData.url.trim() !== '';
    } else {
      return formData.job_description.trim() !== '';
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* URL Input */}
      {activeTab === 'url' && (
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
            Job Posting URL
          </label>
          <div className="relative">
            <LinkIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="url"
              id="url"
              value={formData.url}
              onChange={(e) => handleInputChange('url', e.target.value)}
              placeholder="https://example.com/careers/job-posting"
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            />
          </div>
          <p className="mt-2 text-sm text-gray-500">
            Paste the URL of a job posting or careers page
          </p>
        </div>
      )}

      {/* Job Description Input */}
      {activeTab === 'description' && (
        <div>
          <label htmlFor="job_description" className="block text-sm font-medium text-gray-700 mb-2">
            Job Description
          </label>
          <div className="relative">
            <FileText className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <textarea
              id="job_description"
              value={formData.job_description}
              onChange={(e) => handleInputChange('job_description', e.target.value)}
              placeholder="Paste the job description here..."
              rows={8}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              required
            />
          </div>
          <p className="mt-2 text-sm text-gray-500">
            Copy and paste the job description text
          </p>
        </div>
      )}

      {/* Example Section */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-900 mb-2">Example Input</h3>
        {activeTab === 'url' ? (
          <div className="text-sm text-gray-600">
            <p className="mb-2">Valid URL formats:</p>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>https://company.com/careers/senior-developer</li>
              <li>https://linkedin.com/jobs/view/123456789</li>
              <li>https://indeed.com/viewjob?jk=abc123</li>
            </ul>
          </div>
        ) : (
          <div className="text-sm text-gray-600">
            <p className="mb-2">Include key information like:</p>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>Job title and company name</li>
              <li>Required skills and experience</li>
              <li>Job responsibilities</li>
              <li>Company description</li>
            </ul>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-3">
        <button
          type="submit"
          disabled={!isFormValid() || isLoading}
          className="flex-1 flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Generating...
            </>
          ) : (
            <>
              <Send className="h-4 w-4 mr-2" />
              Generate Emails
            </>
          )}
        </button>
        
        <button
          type="button"
          onClick={handleReset}
          disabled={isLoading}
          className="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <RotateCcw className="h-4 w-4" />
        </button>
      </div>

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-900 mb-2">💡 Tips for Better Results</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Use detailed job descriptions for more personalized emails</li>
          <li>• Include company information when available</li>
          <li>• The AI will automatically match your portfolio projects</li>
        </ul>
      </div>
    </form>
  );
};

export default EmailForm; 