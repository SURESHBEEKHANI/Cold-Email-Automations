__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.document_loaders import WebBaseLoader  # Import WebBaseLoader for processing web content
from chains import Chain  # Import Chain for processing or handling data
from portfolio import Portfolio  # Import Portfolio for managing or querying portfolio data
from utils import clean_text  # Import clean_text for preprocessing text data

class ChatBotApp:
    """
    A chatbot for generating personalized cold emails based on job descriptions or URLs.
    """

    def __init__(self):
        # Initialize components like language model and portfolio
        self.llm = Chain()  # Language model instance
        self.portfolio = Portfolio()  # Portfolio instance

    def get_user_input(self, conversation_history):
        """
        Simulates user input in a chatbot conversation.
        Extracts the latest message from the conversation history.

        Parameters:
        - conversation_history: The history of conversation with the chatbot.

        Returns:
        - user_input: The latest user input.
        """
        # Assuming conversation_history is a list of message dictionaries
        if conversation_history:
            # Get the latest message from the user in the conversation
            return conversation_history[-1]['message']
        return None

    def handle_input(self, user_input):
        """
        Processes the user input, either as a URL or plain text.

        Parameters:
        - user_input: The input provided by the user.

        Returns:
        - A response message with the generated email draft or an error/warning message.
        """
        try:
            if user_input.startswith(('http://', 'https://')):
                # Load and process data from URL
                loader = WebBaseLoader([user_input])
                page_content = loader.load().pop().page_content
                data = clean_text(page_content)
            else:
                # Use the provided plain text
                data = clean_text(user_input)

            # Load portfolio and extract job details
            self.portfolio.load_portfolio()
            jobs = self.llm.extract_jobs(data)

            if jobs:
                response = ""
                for job in jobs:
                    # Extract required skills and query portfolio
                    skills = job.get('skills', [])
                    links = self.portfolio.query_links(skills)

                    # Generate email draft
                    email = self.llm.write_mail(job, links)

                    # Append the email draft to the response
                    response += f"Generated Email Draft:\n{email}\n\n"

                return response
            else:
                return "Warning: No job postings were found in the content you provided. Please ensure that your submission includes valid information such as role, experience, skills, and description."

        except Exception as e:
            return f"Error: {e}"

    def chat(self, conversation_history):
        """
        Main function to handle the chatbot conversation flow.

        Parameters:
        - conversation_history: The history of conversation with the chatbot.
        """
        user_input = self.get_user_input(conversation_history)

        if user_input:
            # Process the user input and generate a response
            response = self.handle_input(user_input)
            return response
        else:
            return "Please provide a valid URL or job description to proceed."

# Example usage of the chatbot application
if __name__ == "__main__":
    # Simulating conversation history (list of messages between user and chatbot)
    conversation_history = [
        {"role": "user", "message": "https://example.com/job-description"},
        # Additional chat history can be appended here...
    ]

    chatbot = ChatBotApp()
    # Generate response based on the latest conversation input
    response = chatbot.chat(conversation_history)
    print(response)
