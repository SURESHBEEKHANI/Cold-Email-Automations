from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.agents import ColdEmailAgents
from src.portfolio import Portfolio
import logging
from routes import email_generator

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

# Initialize components and attach to app state
try:
    app.state.agents = ColdEmailAgents()
    app.state.portfolio = Portfolio()
    logger.info("Components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    app.state.agents = None
    app.state.portfolio = None

# Include the new router
app.include_router(email_generator.router, prefix="/api")
app.include_router(email_generator.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# To run the app, use the command: uvicorn app:app --reload