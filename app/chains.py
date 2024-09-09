import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Chain:
    def __init__(self):
        # Initialize the language model with the API key and specified model
        self.llm = ChatGroq(
            temperature=0,  # Use deterministic responses
            groq_api_key=os.getenv("GROQ_API_KEY"),  # Get the API key from environment variables
            model_name="llama-3.1-70b-versatile"  # Specify the model to be used
        )

    def extract_jobs(self, cleaned_text):
        # Define the prompt template for extracting job information from the scraped text
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The provided text is scraped from the careers page of a website.
            Extract the job postings from this text and return them in JSON format with the following keys: 
            `role`, `experience`, `skills`, and `description`.
            Only return valid JSON.

            ### VALID JSON (NO PREAMBLE):
            If the data is not found in the Context, then return "N/A", otherwise return the precise Answer.
            """
        )
        # Create the extraction chain combining the prompt and the language model
        chain_extract = prompt_extract | self.llm
        # Invoke the chain with the input text
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        
        try:
            # Parse the result into JSON format
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            # Handle parsing errors
            raise OutputParserException("Context too large. Unable to parse job postings.")
        
        # Ensure the result is returned as a list of job postings
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        # Define the prompt template for writing a cold email
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Suresh Beekhani, a Business Development Executive at NexgenAI. NexgenAI is an AI and Software Consulting company, 
            dedicated to facilitating the seamless integration of business processes through automated tools. 
            With extensive experience, NexgenAI has empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency.

            Your task is to write a cold email to the client regarding the job mentioned above, describing how NexgenAI can address their needs.
            Also, include the most relevant examples from the following portfolio links to showcase NexgenAI's expertise: {link_list}.
            Remember, you are Suresh Beekhani, BDE at nexgenai, and the email should be concise and professional.
            Do not provide a preamble.

            ### EMAIL (NO PREAMBLE):
            If the Answer is not found in the Context, then return "N/A", otherwise return the precise Answer.
            """
        )
        
        # Create the email generation chain by combining the prompt and the language model
        chain_email = prompt_email | self.llm
        # Invoke the chain with the job description and portfolio links as input
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        # Return the generated email content
        return res.content

# Code to run if the script is executed directly (useful for debugging)
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
