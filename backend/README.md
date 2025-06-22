## Cold Email Automation API

## Overview

This project provides a FastAPI-based service that automates the extraction of job postings from websites and generates personalized cold emails to potential clients. It leverages AI agents powered by CrewAI and Groq to perform these tasks efficiently.

## Features

- **Job Extraction**: Extracts job postings from scraped text, focusing on fields like role, experience, skills, and job description.
- **Cold Email Generation**: Automatically writes personalized cold emails to potential clients based on the extracted job information and company portfolio links.
- **RESTful API**: FastAPI-based endpoints for easy integration with frontend applications.
- **Portfolio Matching**: Intelligent matching of portfolio items to job requirements.

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **CrewAI**: Framework for orchestrating role-playing autonomous AI agents
- **LangChain**: Framework for developing applications with LLMs
- **Groq**: High-performance LLM inference platform
- **ChromaDB**: Vector database for portfolio matching
- **Pandas**: Data manipulation and analysis
- **Python-dotenv**: Environment variable management

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/SURESHBEEKHANI/Job-Extraction-and-Cold-Email-Automation.git
    cd Job-Extraction-and-Cold-Email-Automation/backend
    ```

2. **Install Dependencies**:
    ```bash
    pip install -e .
    ```

3. **Set Up Environment Variables**:
    Create a `.env` file in the backend directory and add your `GROQ_API_KEY`:
    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

## Usage

### Running the API Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

#### 2. Generate Emails
```bash
POST /generate-emails
```

**Request Body:**
```json
{
    "url": "https://example.com/careers",
    "job_description": "We are looking for a Python developer with 3+ years of experience in machine learning and data analysis."
}
```

**Response:**
```json
{
    "success": true,
    "message": "Successfully generated 1 emails",
    "emails": [
        {
            "job_title": "Python Developer",
            "job_description": "We are looking for a Python developer...",
            "required_skills": ["Python", "Machine Learning"],
            "experience_level": "3+ years",
            "email_content": "Dear Hiring Manager...",
            "portfolio_matches": ["project1", "project2"],
            "location": "Remote",
            "work_type": "Full-time"
        }
    ],
    "total_jobs": 1
}
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── src/
│   ├── agents.py        # CrewAI agents for job analysis and email generation
│   ├── portfolio.py     # Portfolio management and matching
│   └── utils.py         # Utility functions
├── resource/            # Portfolio data and resources
└── pyproject.toml       # Project dependencies and metadata
```

## Customization

- **Prompt Templates**: Modify the prompt templates in `src/agents.py` to adjust the AI behavior
- **Portfolio Data**: Update the portfolio data in the `resource/` directory
- **Model Configuration**: Adjust model settings in the agent initialization

## Error Handling

The API includes comprehensive error handling for:
- Invalid input validation
- Network errors when scraping URLs
- AI model failures
- Portfolio loading issues

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides an overview of the project's purpose, setup instructions, and usage examples. For further information or support, please contact the project maintainer.
