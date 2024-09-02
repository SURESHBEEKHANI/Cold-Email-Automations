# Import necessary modules
import os  # Provides a way to use operating system-dependent functionality like accessing environment variables
from langchain_groq import ChatGroq  # Imports the ChatGroq class for interacting with a language model
from langchain_core.prompts import PromptTemplate  # Imports PromptTemplate for creating prompt templates
from langchain_core.output_parsers import JsonOutputParser  # Imports JsonOutputParser for parsing output into JSON
from langchain_core.exceptions import OutputParserException  # Imports OutputParserException for handling parsing errors
from dotenv import load_dotenv  # Imports load_dotenv to load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Define the Chain class
class Chain:
    def __init__(self):
        # Initialize the ChatGroq language model with a specific API key and model name
        self.llm = ChatGroq(
            temperature=0,  # Set temperature for model responses (0 for deterministic responses)
            groq_api_key=os.getenv("GROQ_API_KEY"),  # Retrieve the API key from environment variables
            model_name="llama-3.1-70b-versatile"  # Specify the model name to use
        )

    def extract_jobs(self, cleaned_text):
        # Create a prompt template for extracting job postings from text
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.or input text
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        # Create a processing chain that combines the prompt template with the language model
        chain_extract = prompt_extract | self.llm
        # Invoke the chain with the cleaned text as input
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            # Create a JSON output parser to parse the result
            json_parser = JsonOutputParser()
            # Parse the result into JSON format
            res = json_parser.parse(res.content)
        except OutputParserException:
            # Handle parsing errors, e.g., if the context is too large
            raise OutputParserException("provode Context `role`, `experience`, `skills` and `description`. . Unable to write colud email for provode contect")
        # Return the result as a list of job postings
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        # Create a prompt template for writing a cold email
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are SURESH Beekhani, a business development executive at NexGenai. NexGeani is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of NexGenai
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase NexGenai portfolio: {link_list}
            Remember you are SURESH Beekhani, BDE at NexGeani. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        # Create a processing chain that combines the email prompt template with the language model
        chain_email = prompt_email | self.llm
        # Invoke the chain with the job description and links as input
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        # Return the content of the generated email
        return res.content

# Code to run if this script is executed directly (not imported)
if __name__ == "__main__":
    # Print the value of the GROQ_API_KEY environment variable (useful for debugging)
    print(os.getenv("GROQ_API_KEY"))