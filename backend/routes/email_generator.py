from fastapi import APIRouter, Depends, HTTPException, Request
from schema.email import EmailRequest, EmailResponse
from typing import List, Dict, Any
import logging

from src.utils import clean_text
from langchain_community.document_loaders import WebBaseLoader
from src.agents import ColdEmailAgents
from src.portfolio import Portfolio

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Dependencies ---
def get_agents(request: Request) -> ColdEmailAgents:
    if not hasattr(request.app.state, 'agents') or request.app.state.agents is None:
        raise HTTPException(status_code=500, detail="System components (agents) not initialized properly")
    return request.app.state.agents

def get_portfolio(request: Request) -> Portfolio:
    if not hasattr(request.app.state, 'portfolio') or request.app.state.portfolio is None:
        raise HTTPException(status_code=500, detail="System components (portfolio) not initialized properly")
    return request.app.state.portfolio

@router.post("/generate-emails", response_model=EmailResponse)
async def generate_emails(
    request: EmailRequest,
    agents: ColdEmailAgents = Depends(get_agents),
    portfolio: Portfolio = Depends(get_portfolio)
):
    """
    Generate cold emails from job URL or description.
    
    Args:
        request: EmailRequest containing either URL or job description
        
    Returns:
        Generated cold emails for all found jobs
    """
    try:
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
            
            generated_emails = []
            for job in jobs:
                try:
                    skills = job.get('skills', [])
                    if isinstance(skills, str):
                        skills = [s.strip() for s in skills.split(',') if s.strip()]
                    portfolio_matches = portfolio.query_links(skills)
                    
                    email_content = agents.generate_cold_email(job, str(portfolio_matches))
                    
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

@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Cold Email Generator API",
        "version": "1.0.0",
        "usage": "POST /api/generate-emails with URL or job_description"
    }

@router.get("/health")
async def health_check():
    return {"status": "ok"} 