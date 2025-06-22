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

  // Pluralization helper
  const pluralize = (word, count) => count === 1 ? word : word + 's';

  return (
    <div className="space-y-8">
      {/* Summary */}
      <div className="bg-gradient-to-r from-primary-100 to-blue-50 border border-primary-200 rounded-xl p-6 flex items-center gap-4 shadow-sm">
        <div className="flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
          <CheckCircle className="h-7 w-7 text-green-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-green-900">
            Successfully generated {results.total_jobs} {pluralize('email', results.total_jobs)}
          </h3>
          <p className="text-sm text-green-800 mt-1">{results.message}</p>
        </div>
      </div>

      {/* Download All Button */}
      <div className="flex justify-end">
        <button
          onClick={downloadAllEmails}
          className="inline-flex items-center px-5 py-2.5 bg-primary-600 text-white font-semibold rounded-lg shadow hover:bg-primary-700 transition-all gap-2"
        >
          <Download className="h-5 w-5" />
          Download All
        </button>
      </div>

      {/* Email List */}
      <div className="space-y-6">
        {results.emails.map((email, index) => (
          <div key={index} className="border border-gray-200 rounded-2xl shadow bg-white overflow-hidden transition hover:shadow-lg">
            {/* Email Header */}
            <div className="bg-gradient-to-r from-gray-50 to-blue-50 px-6 py-4 border-b border-gray-100 flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-lg text-gray-900 truncate">{email.job_title}</h3>
                <div className="flex flex-wrap items-center gap-4 mt-1 text-sm text-gray-600">
                  {email.location && email.location !== 'Not specified' && (
                    <span className="flex items-center gap-1"><MapPin className="h-4 w-4" />{email.location}</span>
                  )}
                  {email.experience_level && email.experience_level !== 'Not specified' && (
                    <span className="flex items-center gap-1"><Clock className="h-4 w-4" />{email.experience_level}</span>
                  )}
                  {email.work_type && email.work_type !== 'Not specified' && (
                    <span className="flex items-center gap-1"><Tag className="h-4 w-4" />{email.work_type}</span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2 ml-4">
                <button
                  onClick={() => toggleEmailExpansion(index)}
                  className="text-gray-500 hover:text-primary-700 p-2 rounded-full transition"
                  title={expandedEmails.has(index) ? 'Collapse' : 'Expand'}
                >
                  {expandedEmails.has(index) ? (
                    <EyeOff className="h-5 w-5" />
                  ) : (
                    <Eye className="h-5 w-5" />
                  )}
                </button>
                <button
                  onClick={() => copyToClipboard(email.email_content, index)}
                  className="text-gray-500 hover:text-green-600 p-2 rounded-full transition"
                  title="Copy email"
                >
                  {copiedEmail === index ? (
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  ) : (
                    <Copy className="h-5 w-5" />
                  )}
                </button>
                <button
                  onClick={() => downloadEmail(email, index)}
                  className="text-gray-500 hover:text-blue-600 p-2 rounded-full transition"
                  title="Download email"
                >
                  <Download className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Email Content */}
            {expandedEmails.has(index) && (
              <div className="p-6 space-y-6">
                {/* Job Description Preview */}
                {email.job_description && (
                  <div>
                    <h4 className="text-base font-semibold text-gray-900 mb-1">Job Description</h4>
                    <p className="text-sm text-gray-700 line-clamp-3">
                      {email.job_description.length > 200 
                        ? `${email.job_description.substring(0, 200)}...`
                        : email.job_description
                      }
                    </p>
                  </div>
                )}

                {/* Required Skills */}
                {email.required_skills && email.required_skills.length > 0 && (
                  <div>
                    <h4 className="text-base font-semibold text-gray-900 mb-1">Required Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {email.required_skills.map((skill, skillIndex) => (
                        <span
                          key={skillIndex}
                          className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 shadow-sm"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Portfolio Matches */}
                {email.portfolio_matches && email.portfolio_matches.length > 0 && (
                  <div>
                    <h4 className="text-base font-semibold text-gray-900 mb-1">Portfolio Matches</h4>
                    <div className="space-y-2">
                      {email.portfolio_matches.slice(0, 3).map((match, matchIndex) => (
                        <div key={matchIndex} className="flex items-center text-sm text-gray-600">
                          <ExternalLink className="h-4 w-4 mr-2 text-gray-400" />
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
                  <h4 className="text-base font-semibold text-gray-900 mb-1">Generated Email</h4>
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
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