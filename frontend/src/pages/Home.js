import React from 'react';
import { Link } from 'react-router-dom';
import { Mail, Zap, Target, Users, ArrowRight, CheckCircle } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Target,
      title: 'Job Extraction',
      description: 'Automatically extract job postings from career pages and job descriptions'
    },
    {
      icon: Mail,
      title: 'Cold Email Generation',
      description: 'Generate personalized cold emails using AI-powered agents'
    },
    {
      icon: Users,
      title: 'Portfolio Matching',
      description: 'Match your portfolio projects with job requirements for better relevance'
    },
    {
      icon: Zap,
      title: 'Fast & Efficient',
      description: 'Process multiple jobs and generate emails in seconds'
    }
  ];

  const benefits = [
    'Save hours of manual research and writing',
    'Increase response rates with personalized content',
    'Scale your outreach efforts efficiently',
    'Focus on high-quality opportunities'
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Automate Your
          <span className="text-primary-600"> Cold Email</span>
          <br />
          Outreach
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Generate personalized cold emails from job postings using AI. Extract job details, 
          match with your portfolio, and create compelling outreach messages automatically.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/generate"
            className="inline-flex items-center px-8 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
          >
            Start Generating Emails
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
          <button className="inline-flex items-center px-8 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors">
            Learn More
          </button>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Powerful Features
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="text-center p-6 bg-white rounded-lg shadow-sm border">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 text-primary-600 rounded-lg mb-4">
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-16 bg-white rounded-lg shadow-sm border">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Why Choose Cold Email Automations?
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Boost Your Outreach Success
              </h3>
              <ul className="space-y-3">
                {benefits.map((benefit, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">How It Works</h3>
              <ol className="space-y-3 text-gray-700">
                <li className="flex items-start">
                  <span className="flex items-center justify-center w-6 h-6 bg-primary-600 text-white text-sm rounded-full mr-3 mt-0.5">1</span>
                  <span>Paste a job URL or description</span>
                </li>
                <li className="flex items-start">
                  <span className="flex items-center justify-center w-6 h-6 bg-primary-600 text-white text-sm rounded-full mr-3 mt-0.5">2</span>
                  <span>AI extracts job details and requirements</span>
                </li>
                <li className="flex items-start">
                  <span className="flex items-center justify-center w-6 h-6 bg-primary-600 text-white text-sm rounded-full mr-3 mt-0.5">3</span>
                  <span>Matches with your portfolio projects</span>
                </li>
                <li className="flex items-start">
                  <span className="flex items-center justify-center w-6 h-6 bg-primary-600 text-white text-sm rounded-full mr-3 mt-0.5">4</span>
                  <span>Generates personalized cold emails</span>
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Ready to Transform Your Outreach?
        </h2>
        <p className="text-xl text-gray-600 mb-8">
          Start generating personalized cold emails in minutes
        </p>
        <Link
          to="/generate"
          className="inline-flex items-center px-8 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
        >
          Get Started Now
          <ArrowRight className="ml-2 h-5 w-5" />
        </Link>
      </div>
    </div>
  );
};

export default Home; 