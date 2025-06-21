import pandas as pd
import chromadb
import uuid
import sqlite3
from typing import List, Dict, Any
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Portfolio:
    def __init__(self, file_path="resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = self._load_portfolio_data()
        
        # Initialize ChromaDB with error handling
        try:
            self.chroma_client = chromadb.PersistentClient('src/vectorstore')
            self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def _load_portfolio_data(self) -> pd.DataFrame:
        """Load portfolio data with comprehensive error handling."""
        try:
            if os.path.exists(self.file_path):
                data = pd.read_csv(self.file_path)
                logger.info(f"Portfolio loaded from {self.file_path}")
                return data
            else:
                logger.warning(f"Portfolio file not found at {self.file_path}, creating sample data")
                return self._create_sample_portfolio()
        except pd.errors.EmptyDataError:
            logger.error("Portfolio file is empty, creating sample data")
            return self._create_sample_portfolio()
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing portfolio file: {e}, creating sample data")
            return self._create_sample_portfolio()
        except Exception as e:
            logger.error(f"Unexpected error loading portfolio: {e}, creating sample data")
            return self._create_sample_portfolio()

    def _create_sample_portfolio(self) -> pd.DataFrame:
        """Create a sample portfolio with diverse skills and projects."""
        sample_data = {
            'Techstack': [
                'Python, Machine Learning, Data Analysis, Pandas, Scikit-learn',
                'JavaScript, React, Node.js, Full-stack Development, API Development',
                'Python, Django, PostgreSQL, AWS, DevOps, CI/CD',
                'Python, AI, Natural Language Processing, TensorFlow, PyTorch',
                'JavaScript, Vue.js, TypeScript, UI/UX Design, Frontend Development',
                'Python, Data Science, SQL, Tableau, Business Intelligence',
                'Java, Spring Boot, Microservices, Docker, Kubernetes',
                'Python, Automation, Selenium, Testing, Quality Assurance'
            ],
            'Links': [
                'https://github.com/portfolio/ml-project-1',
                'https://github.com/portfolio/fullstack-app',
                'https://github.com/portfolio/django-ecommerce',
                'https://github.com/portfolio/nlp-chatbot',
                'https://github.com/portfolio/vue-dashboard',
                'https://github.com/portfolio/data-analytics',
                'https://github.com/portfolio/microservices-app',
                'https://github.com/portfolio/automation-framework'
            ],
            'Experience': [
                '3 years',
                '5 years', 
                '4 years',
                '2 years',
                '3 years',
                '6 years',
                '4 years',
                '3 years'
            ],
            'Specialization': [
                'Machine Learning Engineer',
                'Full-stack Developer',
                'Backend Developer',
                'AI/ML Specialist',
                'Frontend Developer',
                'Data Scientist',
                'Backend Engineer',
                'QA Engineer'
            ]
        }
        return pd.DataFrame(sample_data)

    def load_portfolio(self):
        """Load portfolio data into the vector database."""
        if not self.collection.count():
            for _, row in self.data.iterrows():
                # Create a comprehensive document combining all portfolio information
                portfolio_text = f"{row['Techstack']} {row.get('Specialization', '')} {row.get('Experience', '')}"
                
                self.collection.add(
                    documents=[portfolio_text],
                    metadatas=[{
                        "links": row["Links"],
                        "experience": row.get("Experience", ""),
                        "specialization": row.get("Specialization", ""),
                        "techstack": row["Techstack"]
                    }],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Query portfolio for relevant skills and return matching projects."""
        if not skills:
            return []
        
        # Convert skills list to a single query string
        query_text = " ".join(skills) if isinstance(skills, list) else str(skills)
        
        try:
            results = self.collection.query(
                query_texts=[query_text], 
                n_results=3,
                include=['metadatas', 'documents']
            )
            
            # Format the results for better use in email generation
            formatted_results = []
            for i, metadata in enumerate(results.get('metadatas', [[]])[0]):
                formatted_results.append({
                    'link': metadata.get('links', ''),
                    'experience': metadata.get('experience', ''),
                    'specialization': metadata.get('specialization', ''),
                    'techstack': metadata.get('techstack', ''),
                    'relevance_score': i + 1  # Simple relevance scoring
                })
            
            return formatted_results
        except Exception as e:
            print(f"Error querying portfolio: {e}")
            return []

    def get_agent_profiles(self) -> List[Dict[str, Any]]:
        """Get all agent profiles for team composition analysis."""
        profiles = []
        for _, row in self.data.iterrows():
            profiles.append({
                'specialization': row.get('Specialization', ''),
                'experience': row.get('Experience', ''),
                'techstack': row['Techstack'],
                'portfolio_link': row['Links']
            })
        return profiles

    def find_team_matches(self, job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Find the best team composition for a given job."""
        required_skills = job_requirements.get('skills', [])
        if isinstance(required_skills, str):
            required_skills = [required_skills]
        
        # Query for individual matches
        individual_matches = self.query_links(required_skills)
        
        # Analyze team composition possibilities
        all_profiles = self.get_agent_profiles()
        
        # Simple team matching logic - can be enhanced
        team_analysis = {
            'individual_matches': individual_matches,
            'team_recommendations': [],
            'skill_coverage': {},
            'collaboration_score': 0
        }
        
        # Create team recommendations based on skill coverage
        if len(individual_matches) >= 2:
            team_analysis['team_recommendations'] = [
                {
                    'agents': individual_matches[:2],
                    'combined_skills': required_skills,
                    'collaboration_potential': 'High'
                }
            ]
            team_analysis['collaboration_score'] = 85
        
        return team_analysis