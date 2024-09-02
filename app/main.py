import streamlit as st  # Import Streamlit at the top
# Continue with the rest of your imports
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Set the Streamlit page configuration first, before any other Streamlit commands
st.set_page_config(
    layout="wide", 
    page_title="Cloud Email Generator", 
    page_icon="📧"
)



def sidebar():
    """
    This function sets up the sidebar for the Streamlit app. 
    It displays a logo and a centered title using custom HTML and CSS.
    """
    
    # Display the logo in the sidebar using an image file
    st.sidebar.image(r'C:\Users\SURESH BEEKHANI\Desktop\project-genai-cold-email-generator\imgs\img.png', use_column_width=True)
    
    # Inject custom HTML and CSS to create a centered title in the sidebar
    st.sidebar.markdown("""
        <style>
        .sidebar-title {
            text-align: center;
            font-size: 34px;
            font-weight: bold;
        }
        </style>
        <div class="sidebar-title">
            Cloud Email Generator
        </div>
        """, unsafe_allow_html=True)

def create_streamlit_app(llm, portfolio, clean_text):
    """
    This function sets up the main functionality of the Streamlit app. 
    It takes user input, processes web content or plain text, extracts job details, and generates emails.
    
    Parameters:
    - llm: A language model instance (likely the Chain object).
    - portfolio: An instance of the Portfolio class.
    - clean_text: A function for cleaning up text.
    """
    # Create a single input field for URL or plain text
    user_input = st.chat_input("Could you Please Provide a Valid URL or The Job Description")

    if user_input:
        try:
            # Check if the user input is a URL
            if user_input.startswith(('http://', 'https://')):
                # Load and process data from the URL entered by the user
                loader = WebBaseLoader([user_input])
                page_content = loader.load().pop().page_content
                data = clean_text(page_content)
            else:
                # Use the plain text input provided by the user
                data = clean_text(user_input)
            
            # Load portfolio data and extract job details using the language model
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            # Generate and display email content if jobs are found
            if jobs:
                for job in jobs:
                    # Extract skills required for the job
                    skills = job.get('skills', [])
                    
                    # Query portfolio for relevant links based on the skills
                    links = portfolio.query_links(skills)
                    
                    # Generate an email draft based on job details and relevant links
                    email = llm.write_mail(job, links)
                    
                    # Display the generated email content in the app, formatted as Markdown
                    st.code(email, language='markdown')
            else:
                # Display a warning message if no jobs are found in the provided content
                st.warning("No jobs found in the provided URL or text.")
                
        except Exception as e:
            # Display an error message if an exception occurs during processing
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    
    # Initialize components for the app
    chain = Chain()
    portfolio = Portfolio()
    
    # Display the sidebar with the logo and title
    sidebar()
    
    # Create and run the Streamlit app with the initialized components
    create_streamlit_app(chain, portfolio, clean_text)
