from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from src.agents import ColdEmailAgents
from src.portfolio import Portfolio
from src.utils import clean_text
from langchain_community.document_loaders import WebBaseLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cold Email Generator API",
    description="Generate cold emails from job URLs or descriptions using AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components with error handling
try:
    agents = ColdEmailAgents()
    portfolio = Portfolio()
    logger.info("Components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    agents = None
    portfolio = None

# Request model
class EmailRequest(BaseModel):
    url: Optional[str] = None
    job_description: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/careers",
                "job_description": "We are looking for a Python developer with 3+ years of experience in machine learning and data analysis."
            }
        }

# Response model
class EmailResponse(BaseModel):
    success: bool
    message: str
    emails: List[Dict[str, Any]]
    total_jobs: int

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Cold Email Generator API",
        "version": "1.0.0",
        "usage": "POST /generate-emails with URL or job_description"
    }

@app.post("/generate-emails", response_model=EmailResponse)
async def generate_emails(request: EmailRequest):
    """
    Generate cold emails from job URL or description.
    
    Args:
        request: EmailRequest containing either URL or job description
        
    Returns:
        Generated cold emails for all found jobs
    """
    try:
        # Check if components are initialized
        if agents is None or portfolio is None:
            raise HTTPException(status_code=500, detail="System components not initialized properly")
        
        # Validate input
        if not request.url and not request.job_description:
            raise HTTPException(status_code=400, detail="Either URL or job_description must be provided")
        
        # Process input
        if request.url:
            try:
                # Load and process data from URL
                loader = WebBaseLoader([request.url])
                page_content = loader.load().pop().page_content
                data = clean_text(page_content)
                logger.info(f"Successfully loaded content from URL: {request.url}")
            except Exception as e:
                logger.error(f"Failed to load content from URL: {e}")
                raise HTTPException(status_code=400, detail=f"Failed to load content from URL: {str(e)}")
        else:
            # Use the provided job description
            data = clean_text(request.job_description)
            logger.info("Using provided job description")
        
        # Load portfolio
        try:
            portfolio.load_portfolio()
            logger.info("Portfolio loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load portfolio: {e}")
            raise HTTPException(status_code=500, detail="Failed to load portfolio data")
        
        # Use the complete workflow method for better coordination
        try:
            workflow_result = agents.process_complete_workflow(data, [])
            logger.info("Complete workflow executed successfully")
            
            # Parse the workflow result
            if isinstance(workflow_result, str):
                # If it's a string, treat it as a single email
                generated_emails = [{
                    "job_title": "Extracted Role",
                    "job_description": data[:200] + "..." if len(data) > 200 else data,
                    "required_skills": [],
                    "experience_level": "Not specified",
                    "email_content": workflow_result,
                    "portfolio_matches": [],
                    "location": "Not specified",
                    "work_type": "Not specified"
                }]
            else:
                # If it's a structured result, format it properly
                generated_emails = [workflow_result] if not isinstance(workflow_result, list) else workflow_result
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            # Fallback to individual methods
            jobs = agents.analyze_jobs(data)
            
            if not jobs:
                return EmailResponse(
                    success=False,
                    message="No job postings found in the provided content",
                    emails=[],
                    total_jobs=0
                )
            
            # Generate emails for each job
            generated_emails = []
            for job in jobs:
                try:
                    # Extract skills and query portfolio
                    skills = job.get('skills', [])
                    if isinstance(skills, str):
                        skills = [skills]
                    portfolio_matches = portfolio.query_links(skills)
                    
                    # Generate email using Crew AI agents
                    email_content = agents.generate_cold_email(job, str(portfolio_matches))
                    
                    # Create email response
                    email_data = {
                        "job_title": job.get('role', 'Unknown Role'),
                        "job_description": job.get('description', ''),
                        "required_skills": skills,
                        "experience_level": job.get('experience', 'Not specified'),
                        "email_content": email_content,
                        "portfolio_matches": portfolio_matches,
                        "location": job.get('location', 'Not specified'),
                        "work_type": job.get('work_type', 'Not specified')
                    }
                    
                    generated_emails.append(email_data)
                    
                except Exception as e:
                    # Continue with other jobs if one fails
                    logger.error(f"Error processing job {job.get('role', 'Unknown')}: {str(e)}")
                    continue
        
        return EmailResponse(
            success=True,
            message=f"Successfully generated {len(generated_emails)} emails",
            emails=generated_emails,
            total_jobs=len(generated_emails)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_emails: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating emails: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 