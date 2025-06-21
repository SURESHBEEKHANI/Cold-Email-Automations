import React, { useState } from 'react';
import { Copy, Download, Eye, EyeOff, CheckCircle, ExternalLink, Tag, MapPin, Clock } from 'lucide-react';

const EmailResults = ({ results }) => {
  const [expandedEmails, setExpandedEmails] = useState(new Set());
  const [copiedEmail, setCopiedEmail] = useState(null);

  const toggleEmailExpansion = (emailIndex) => {
    const newExpanded = new Set(expandedEmails);
    if (newExpanded.has(emailIndex)) {
      newExpanded.delete(emailIndex);
    } else {
      newExpanded.add(emailIndex);
    }
    setExpandedEmails(newExpanded);
  };

  const copyToClipboard = async (text, emailIndex) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedEmail(emailIndex);
      setTimeout(() => setCopiedEmail(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const downloadEmail = (email, index) => {
    const blob = new Blob([email.email_content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cold-email-${email.job_title.replace(/\s+/g, '-').toLowerCase()}-${index + 1}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadAllEmails = () => {
    const allEmails = results.emails.map((email, index) => 
      `=== Email ${index + 1} ===\n\nJob: ${email.job_title}\n\n${email.email_content}\n\n`
    ).join('\n');
    
    const blob = new Blob([allEmails], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cold-emails-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!results || !results.emails || results.emails.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No emails generated</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center">
          <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
          <div>
            <h3 className="text-sm font-medium text-green-800">
              Successfully generated {results.total_jobs} email{results.total_jobs !== 1 ? 's' : ''}
            </h3>
            <p className="text-sm text-green-700 mt-1">{results.message}</p>
          </div>
        </div>
      </div>

      {/* Download All Button */}
      <div className="flex justify-end">
        <button
          onClick={downloadAllEmails}
          className="inline-flex items-center px-4 py-2 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Download className="h-4 w-4 mr-2" />
          Download All
        </button>
      </div>

      {/* Email List */}
      <div className="space-y-4">
        {results.emails.map((email, index) => (
          <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
            {/* Email Header */}
            <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900">{email.job_title}</h3>
                  <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600">
                    {email.location && email.location !== 'Not specified' && (
                      <div className="flex items-center">
                        <MapPin className="h-3 w-3 mr-1" />
                        {email.location}
                      </div>
                    )}
                    {email.experience_level && email.experience_level !== 'Not specified' && (
                      <div className="flex items-center">
                        <Clock className="h-3 w-3 mr-1" />
                        {email.experience_level}
                      </div>
                    )}
                    {email.work_type && email.work_type !== 'Not specified' && (
                      <div className="flex items-center">
                        <Tag className="h-3 w-3 mr-1" />
                        {email.work_type}
                      </div>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => toggleEmailExpansion(index)}
                    className="text-gray-600 hover:text-gray-900 p-1"
                    title={expandedEmails.has(index) ? 'Collapse' : 'Expand'}
                  >
                    {expandedEmails.has(index) ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                  <button
                    onClick={() => copyToClipboard(email.email_content, index)}
                    className="text-gray-600 hover:text-gray-900 p-1"
                    title="Copy email"
                  >
                    {copiedEmail === index ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </button>
                  <button
                    onClick={() => downloadEmail(email, index)}
                    className="text-gray-600 hover:text-gray-900 p-1"
                    title="Download email"
                  >
                    <Download className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Email Content */}
            {expandedEmails.has(index) && (
              <div className="p-4">
                {/* Job Description Preview */}
                {email.job_description && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Job Description</h4>
                    <p className="text-sm text-gray-600 line-clamp-3">
                      {email.job_description.length > 200 
                        ? `${email.job_description.substring(0, 200)}...`
                        : email.job_description
                      }
                    </p>
                  </div>
                )}

                {/* Required Skills */}
                {email.required_skills && email.required_skills.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Required Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {email.required_skills.map((skill, skillIndex) => (
                        <span
                          key={skillIndex}
                          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Portfolio Matches */}
                {email.portfolio_matches && email.portfolio_matches.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Portfolio Matches</h4>
                    <div className="space-y-2">
                      {email.portfolio_matches.slice(0, 3).map((match, matchIndex) => (
                        <div key={matchIndex} className="flex items-center text-sm text-gray-600">
                          <ExternalLink className="h-3 w-3 mr-2 text-gray-400" />
                          <span className="truncate">{match}</span>
                        </div>
                      ))}
                      {email.portfolio_matches.length > 3 && (
                        <p className="text-xs text-gray-500">
                          +{email.portfolio_matches.length - 3} more matches
                        </p>
                      )}
                    </div>
                  </div>
                )}

                {/* Email Content */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Generated Email</h4>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans">
                      {email.email_content}
                    </pre>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmailResults; 