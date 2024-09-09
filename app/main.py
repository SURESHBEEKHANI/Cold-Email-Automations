__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st  # Import Streamlit for creating the web app
from langchain_community.document_loaders import WebBaseLoader  # Import WebBaseLoader for processing web content
from chains import Chain  # Import Chain for processing or handling data
from portfolio import Portfolio  # Import Portfolio for managing or querying portfolio data
from utils import clean_text  # Import clean_text for preprocessing text data

# Configure the Streamlit page
st.set_page_config(
    layout="wide",  # Use a wide layout
    page_title="Cloud Email Generator",  # Set the page title
    page_icon="📧"  # Set the page icon
)
st.title('Cloud Email')

def sidebar():
    """
    Sets up the sidebar with a logo, caption, title, and description using custom HTML and CSS.
    """
    # Display the logo in the sidebar
    st.sidebar.image(
        r'C:\Users\SURESH BEEKHANI\Desktop\project-genai-cold-email-generator\imgs\img.png', 
        use_column_width=True
    )
    
    
    # Center the title in the sidebar with custom HTML and CSS
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
    
    # Add a description below the title
    st.sidebar.markdown("""
        <style>
        .sidebar-description {
            text-align: center;
            font-size: 20px;
            margin-top: 20px;
        }
        </style>
        <div class="sidebar-description">
            This tool helps you generate personalized cold emails quickly and effectively. 
            Input your details, and let the AI do the rest, crafting compelling messages 
            tailored to your needs.
        </div>
        """, unsafe_allow_html=True)


def create_streamlit_app(llm, portfolio, clean_text):
    """
    Sets up the main functionality of the Streamlit app.
    
    Parameters:
    - llm: Language model instance (e.g., Chain object).
    - portfolio: Instance of the Portfolio class.
    - clean_text: Function for cleaning up text.
    """
    # Input field for URL or plain text
    user_input = st.chat_input("Please provide a valid URL or job description:")

    if user_input:
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
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            if jobs:
                for job in jobs:
                    # Extract required skills and query portfolio
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    
                    # Generate email draft
                    email = llm.write_mail(job, links)
                    # Display the email draft with a title
                    st.write("### Generated Email Draft:")
                    st.write(f"```markdown\n{email}\n```")

                    # Display the user input with a title
                    st.write("### User Input:")
                    st.write(f"```markdown\n{user_input}\n```")
            else:
                st.warning("Warning: No job postings were found in the content you provided. Please ensure that your submission includes valid information and includes the following details: role, experience, skills, and description.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Initialize components
    chain = Chain()
    portfolio = Portfolio()
    
    # Display sidebar
    sidebar()
    
    # Run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)

