from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ColdEmailAgents:
    def __init__(self):
        # Set the API key as environment variable for CrewAI
        groq_api_key = os.getenv("GROQ_API_KEY", "")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        os.environ["GROQ_API_KEY"] = groq_api_key
        
        # Initialize the LLM properly with Groq - use a more compatible model
        try:
            self.llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama3-8b-8192"  # Use a more stable model
            )
            logger.info("LLM initialized successfully with Groq")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            # Fallback to string-based LLM for CrewAI compatibility
            self.llm = "llama3-8b-8192"
            logger.info("Using string-based LLM configuration as fallback")
        
        # Initialize agents
        self.job_analyst = self._create_job_analyst()
        self.portfolio_analyst = self._create_portfolio_analyst()
        self.email_writer = self._create_email_writer()
        self.team_coordinator = self._create_team_coordinator()

    def _create_job_analyst(self) -> Agent:
        """Creates an agent specialized in analyzing job postings and extracting key information."""
        return Agent(
            role='Job Analysis Specialist',
            goal='Extract and analyze job postings to identify key requirements, skills, and opportunities',
            backstory="""You are an expert job analyst with years of experience in talent acquisition and 
            recruitment. You excel at parsing through job descriptions, identifying key requirements, 
            and understanding what companies are truly looking for in candidates. You have a deep 
            understanding of various industries and can quickly identify the most important aspects 
            of any job posting.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,  # Limit iterations to prevent infinite loops
            max_rpm=10   # Rate limiting
        )

    def _create_portfolio_analyst(self) -> Agent:
        """Creates an agent specialized in analyzing portfolio data and matching skills."""
        return Agent(
            role='Portfolio & Skills Analyst',
            goal='Analyze portfolio data and match agent skills with job requirements',
            backstory="""You are a senior portfolio analyst who specializes in evaluating technical 
            skills, project portfolios, and team capabilities. You have extensive experience in 
            matching candidate skills with job requirements and can identify the best combinations 
            of team members for specific projects. You understand both technical and business 
            requirements and can assess collaboration potential between team members.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            max_rpm=10
        )

    def _create_email_writer(self) -> Agent:
        """Creates an agent specialized in writing compelling cold emails."""
        return Agent(
            role='Cold Email Specialist',
            goal='Write compelling, personalized cold emails that convert prospects into clients',
            backstory="""You are SURESH BEEKHANI, a seasoned business development executive at Nexgenai. 
            You have a proven track record of writing cold emails that generate high response rates. 
            You understand the psychology of persuasion and know how to craft messages that resonate 
            with potential clients. You excel at highlighting team capabilities, showcasing relevant 
            portfolio work, and demonstrating clear value propositions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            max_rpm=10
        )

    def _create_team_coordinator(self) -> Agent:
        """Creates an agent that coordinates the overall process and ensures quality output."""
        return Agent(
            role='Project Coordinator',
            goal='Coordinate the entire process and ensure high-quality, cohesive output',
            backstory="""You are a senior project coordinator with expertise in managing complex 
            workflows and ensuring deliverables meet the highest standards. You excel at 
            coordinating between different specialists, reviewing outputs for quality and 
            consistency, and ensuring that the final product exceeds client expectations. 
            You have a keen eye for detail and can spot opportunities for improvement.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            max_iter=3,
            max_rpm=10
        )

    def analyze_jobs(self, cleaned_text: str) -> List[Dict[str, Any]]:
        """Extract and analyze job postings from cleaned text."""
        try:
            task = Task(
                description=f"""
                Analyze the following scraped text from a careers page and extract job postings.
                
                TEXT TO ANALYZE:
                {cleaned_text}
                
                Your task is to:
                1. Identify all job postings in the text
                2. Extract key information for each job:
                   - Role/Position title
                   - Required experience level
                   - Required skills (technical and soft skills)
                   - Job description
                   - Company information (if available)
                3. Return the data in a structured JSON format
                4. Ensure all extracted information is accurate and complete
                
                Return only valid JSON with the following structure:
                [
                    {{
                        "role": "Job Title",
                        "experience": "Experience Level",
                        "skills": ["skill1", "skill2", "skill3"],
                        "description": "Detailed job description"
                    }}
                ]
                """,
                agent=self.job_analyst,
                expected_output="A JSON array containing structured job posting data"
            )

            crew = Crew(
                agents=[self.job_analyst],
                tasks=[task],
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            
            try:
                # Parse the result to extract JSON
                if isinstance(result, str):
                    # Try to find JSON in the result
                    start_idx = result.find('[')
                    end_idx = result.rfind(']') + 1
                    if start_idx != -1 and end_idx != 0:
                        json_str = result[start_idx:end_idx]
                        return json.loads(json_str)
                    else:
                        # If no JSON found, return empty list
                        return []
                else:
                    return result if isinstance(result, list) else [result]
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON from CrewAI result")
                return []
                
        except Exception as e:
            logger.error(f"CrewAI job analysis failed: {e}")
            # Fallback to direct LLM call
            return self._fallback_analyze_jobs(cleaned_text)

    def _fallback_analyze_jobs(self, cleaned_text: str) -> List[Dict[str, Any]]:
        """Fallback method using direct LLM calls when CrewAI fails."""
        try:
            if isinstance(self.llm, str):
                # If LLM is a string, we can't make direct calls
                logger.error("Cannot use fallback method with string-based LLM")
                return []
            
            prompt = f"""
            Analyze the following job posting text and extract key information in JSON format.
            
            TEXT: {cleaned_text}
            
            Return a JSON array with this structure:
            [
                {{
                    "role": "Job Title",
                    "experience": "Experience Level", 
                    "skills": ["skill1", "skill2", "skill3"],
                    "description": "Job description"
                }}
            ]
            
            Return only valid JSON.
            """
            
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Extract JSON from response
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                logger.error("No valid JSON found in LLM response")
                return []
                
        except Exception as e:
            logger.error(f"Fallback job analysis failed: {e}")
            return []

    def analyze_portfolio_match(self, job: Dict[str, Any], portfolio_links: List[str]) -> Dict[str, Any]:
        """Analyze portfolio data and match with job requirements."""
        task = Task(
            description=f"""
            Analyze the job requirements and portfolio data to create the best team match.
            
            JOB REQUIREMENTS:
            {json.dumps(job, indent=2)}
            
            PORTFOLIO LINKS:
            {portfolio_links}
            
            Your task is to:
            1. Analyze the job requirements and identify key skills needed
            2. Review the portfolio data and identify relevant projects/experience
            3. Determine if this is a single-agent or team opportunity
            4. If team opportunity, identify complementary skill sets
            5. Create a comprehensive analysis including:
               - Skill match percentage
               - Relevant portfolio projects
               - Team composition recommendations
               - Value proposition highlights
            
            Return a structured analysis that can be used for email generation.
            """,
            agent=self.portfolio_analyst,
            expected_output="A comprehensive analysis of portfolio-job match with team recommendations"
        )

        crew = Crew(
            agents=[self.portfolio_analyst],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )

        return crew.kickoff()

    def generate_cold_email(self, job: Dict[str, Any], portfolio_analysis: str) -> str:
        """Generate a compelling cold email based on job and portfolio analysis."""
        try:
            task = Task(
                description=f"""
                Write a compelling cold email as SURESH BEEKHANI, BDE at Nexgenai.
                
                JOB INFORMATION:
                {json.dumps(job, indent=2)}
                
                PORTFOLIO ANALYSIS:
                {portfolio_analysis}
                
                Your task is to write a professional cold email that:
                1. Introduces Nexgenai as an AI & Software Consulting company
                2. Addresses the specific job requirements
                3. Highlights relevant portfolio work and team capabilities
                4. Demonstrates clear value proposition
                5. Includes a compelling call-to-action
                6. Maintains professional tone while being engaging
                
                Key points to include:
                - Nexgenai's expertise in AI & Software Consulting
                - Relevant experience and portfolio projects
                - Team capabilities and collaboration benefits
                - Specific value propositions for the client
                - Clear next steps or call-to-action
                
                Write the email in a professional business format with proper greeting and closing.
                """,
                agent=self.email_writer,
                expected_output="A compelling cold email ready to send to the prospect"
            )

            crew = Crew(
                agents=[self.email_writer],
                tasks=[task],
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            return str(result) if result else "Email generation failed"
            
        except Exception as e:
            logger.error(f"CrewAI email generation failed: {e}")
            # Fallback to direct LLM call
            return self._fallback_generate_email(job, portfolio_analysis)

    def _fallback_generate_email(self, job: Dict[str, Any], portfolio_analysis: str) -> str:
        """Fallback method for email generation using direct LLM calls."""
        try:
            if isinstance(self.llm, str):
                logger.error("Cannot use fallback method with string-based LLM")
                return "Email generation failed - system error"
            
            prompt = f"""
            Write a professional cold email as SURESH BEEKHANI, BDE at Nexgenai.
            
            JOB: {json.dumps(job, indent=2)}
            PORTFOLIO: {portfolio_analysis}
            
            Write a compelling cold email that:
            1. Introduces Nexgenai as an AI & Software Consulting company
            2. Addresses the specific job requirements
            3. Highlights relevant portfolio work and team capabilities
            4. Demonstrates clear value proposition
            5. Includes a compelling call-to-action
            
            Write in professional business format with proper greeting and closing.
            """
            
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            return content
            
        except Exception as e:
            logger.error(f"Fallback email generation failed: {e}")
            return "Email generation failed - system error"

    def process_complete_workflow(self, cleaned_text: str, portfolio_links: List[str]) -> Dict[str, Any]:
        """Execute the complete workflow from job analysis to email generation."""
        try:
            # Task 1: Analyze jobs
            job_analysis_task = Task(
                description=f"Extract and analyze job postings from the provided text: {cleaned_text[:500]}...",
                agent=self.job_analyst,
                expected_output="Structured job posting data in JSON format"
            )

            # Task 2: Analyze portfolio matches
            portfolio_task = Task(
                description="Analyze portfolio data and match with job requirements",
                agent=self.portfolio_analyst,
                expected_output="Portfolio analysis with team recommendations",
                context=[job_analysis_task]
            )

            # Task 3: Generate cold email
            email_task = Task(
                description="Generate compelling cold email based on analysis",
                agent=self.email_writer,
                expected_output="Professional cold email ready for sending",
                context=[portfolio_task]
            )

            # Task 4: Coordinate and review
            coordination_task = Task(
                description="Review and coordinate the entire process to ensure quality output",
                agent=self.team_coordinator,
                expected_output="Final reviewed and polished cold email",
                context=[email_task]
            )

            crew = Crew(
                agents=[self.job_analyst, self.portfolio_analyst, self.email_writer, self.team_coordinator],
                tasks=[job_analysis_task, portfolio_task, email_task, coordination_task],
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            return result
            
        except Exception as e:
            logger.error(f"Complete workflow failed: {e}")
            # Fallback to simple workflow
            return self._simple_workflow_fallback(cleaned_text, portfolio_links)

    def _simple_workflow_fallback(self, cleaned_text: str, portfolio_links: List[str]) -> Dict[str, Any]:
        """Simple fallback workflow when complex CrewAI workflow fails."""
        try:
            # Step 1: Analyze jobs using fallback method
            jobs = self._fallback_analyze_jobs(cleaned_text)
            
            if not jobs:
                return {
                    "error": "No job postings found",
                    "email_content": "Unable to generate email - no job information found"
                }
            
            # Step 2: Generate email for the first job found
            job = jobs[0] if isinstance(jobs, list) else jobs
            
            # Step 3: Generate email using fallback method
            email_content = self._fallback_generate_email(job, str(portfolio_links))
            
            return {
                "job_title": job.get('role', 'Unknown Role'),
                "job_description": job.get('description', ''),
                "required_skills": job.get('skills', []),
                "experience_level": job.get('experience', 'Not specified'),
                "email_content": email_content,
                "portfolio_matches": portfolio_links,
                "workflow_type": "fallback"
            }
            
        except Exception as e:
            logger.error(f"Simple workflow fallback failed: {e}")
            return {
                "error": "Workflow failed",
                "email_content": "Unable to generate email due to system error"
            } 