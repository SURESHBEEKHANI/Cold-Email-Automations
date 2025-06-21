# 🚀 Cold Email Automations

A full-stack web application that automates the extraction of job postings from career websites and generates personalized cold emails using AI agents. Built with React frontend and FastAPI backend powered by CrewAI and LangChain.

![Cold Email Automation](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-Latest-orange.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project combines web scraping, AI-powered job analysis, and automated email generation to streamline the process of reaching out to potential clients. The system uses multiple AI agents working together to:

1. **Extract job postings** from career websites
2. **Analyze job requirements** and match them with portfolio data
3. **Generate personalized cold emails** using AI agents
4. **Provide a modern web interface** for easy interaction

## ✨ Features

### 🔍 Job Extraction
- **Web Scraping**: Extract job postings from any career website URL
- **Text Processing**: Clean and structure raw web content
- **Job Analysis**: Identify roles, skills, experience requirements, and work types
- **JSON Output**: Structured data extraction for further processing

### 🤖 AI-Powered Email Generation
- **Multi-Agent System**: Uses CrewAI with specialized agents for different tasks
- **Portfolio Matching**: Automatically matches relevant portfolio projects with job requirements
- **Personalized Content**: Generates context-aware, professional cold emails
- **Skill-Based Recommendations**: Suggests relevant team compositions and experience

### 🌐 Modern Web Interface
- **React Frontend**: Clean, responsive UI built with React 18
- **Tailwind CSS**: Modern styling with utility-first approach
- **Real-time Processing**: Live email generation with progress indicators
- **History Tracking**: Save and review previously generated emails

### 🔧 Backend API
- **FastAPI**: High-performance, async API with automatic documentation
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling and logging
- **Health Checks**: API health monitoring endpoints

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI       │    │   CrewAI        │
│   Frontend      │◄──►│   Backend       │◄──►│   Agents        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Tailwind CSS  │    │   Web Scraping  │    │   ChromaDB      │
│   UI Components │    │   & Cleaning    │    │   Vector Store  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Agent Roles

1. **Job Analyst Agent**: Extracts and structures job postings
2. **Portfolio Analyst Agent**: Matches portfolio data with requirements
3. **Email Writer Agent**: Generates personalized cold emails
4. **Team Coordinator Agent**: Orchestrates the entire workflow

## 🛠️ Tech Stack

### Frontend
- **React 18.2.0** - Modern UI framework
- **React Router DOM** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Icon library

### Backend
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **CrewAI** - Multi-agent orchestration
- **LangChain** - LLM framework
- **ChatGroq** - Language model service
- **ChromaDB** - Vector database
- **Pandas** - Data manipulation
- **Selenium** - Web scraping

### AI/ML
- **Groq API** - High-performance LLM inference
- **Vector Embeddings** - Semantic search and matching
- **Prompt Engineering** - Structured AI interactions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Cold-Email-Automations.git
cd Cold-Email-Automations
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Start the backend server
python main.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📦 Installation

### Detailed Backend Installation

1. **Environment Setup**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Variables**
Create a `.env` file in the backend directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run Tests**
```bash
python test.py
```

### Detailed Frontend Installation

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configuration**
The frontend is configured to proxy API calls to `http://localhost:8000` (see `package.json`).

3. **Start Development Server**
```bash
npm start
```

## 💻 Usage

### Web Interface

1. **Navigate to the Application**
   - Open http://localhost:3000 in your browser

2. **Generate Emails**
   - Go to the "Generate Emails" page
   - Enter a career website URL or paste a job description
   - Click "Generate Emails"
   - View the generated personalized cold emails

3. **Review History**
   - Check the "History" page to see previously generated emails

### API Usage

#### Generate Emails from URL
```bash
curl -X POST "http://localhost:8000/generate-emails" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/careers"
  }'
```

#### Generate Emails from Job Description
```bash
curl -X POST "http://localhost:8000/generate-emails" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We are looking for a Python developer with 3+ years of experience in machine learning and data analysis."
  }'
```

#### Health Check
```bash
curl "http://localhost:8000/health"
```

## 📚 API Documentation

### Endpoints

#### `POST /generate-emails`
Generate cold emails from job URLs or descriptions.

**Request Body:**
```json
{
  "url": "https://example.com/careers",
  "job_description": "Optional job description text"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully generated 2 emails",
  "emails": [
    {
      "job_title": "Senior Python Developer",
      "job_description": "We are looking for...",
      "required_skills": ["Python", "Django", "Machine Learning"],
      "experience_level": "3+ years",
      "email_content": "Dear Hiring Manager...",
      "portfolio_matches": ["project1", "project2"],
      "location": "Remote",
      "work_type": "Full-time"
    }
  ],
  "total_jobs": 2
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### `GET /`
API information endpoint.

**Response:**
```json
{
  "message": "Cold Email Generator API",
  "version": "1.0.0",
  "usage": "POST /generate-emails with URL or job_description"
}
```

## 🔧 Development

### Project Structure
```
Cold-Email-Automations/
├── backend/
│   ├── src/
│   │   ├── agents.py          # CrewAI agents implementation
│   │   ├── portfolio.py       # Portfolio management
│   │   ├── prompt.py          # Prompt templates
│   │   └── utils.py           # Utility functions
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── test.py                # Test suite
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   └── App.js            # Main app component
│   ├── package.json          # Node.js dependencies
│   └── tailwind.config.js    # Tailwind configuration
└── README.md                 # This file
```

### Running Tests
```bash
# Backend tests
cd backend
python test.py

# Frontend tests
cd frontend
npm test
```

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **React**: Follow React best practices

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Follow the existing code style

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](backend/LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Architecture Fixes](backend/ARCHITECTURE_FIXES.md) document for known issues
2. Review the API documentation at http://localhost:8000/docs
3. Check the logs for detailed error messages
4. Open an issue on GitHub with detailed information

## 🙏 Acknowledgments

- **CrewAI** for the multi-agent orchestration framework
- **LangChain** for the LLM integration tools
- **Groq** for high-performance language model inference
- **FastAPI** for the modern Python web framework
- **React** for the frontend framework

---

**Made with ❤️ for automating cold email outreach** 