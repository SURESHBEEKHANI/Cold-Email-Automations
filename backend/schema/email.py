from pydantic import BaseModel
from typing import Optional, List, Dict, Any

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

class EmailResponse(BaseModel):
    success: bool
    message: str
    emails: List[Dict[str, Any]]
    total_jobs: int 