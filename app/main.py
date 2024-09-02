import streamlit as st  # Import Streamlit
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Configure the Streamlit page
st.set_page_config(
    layout="wide",
    page_title="Cloud Email Generator",
    page_icon="📧"
)

def sidebar():
    """
    Sets up the sidebar with a logo and a centered title using custom HTML and CSS.
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
                    
                  
                    st.code(email.title().strip(), language="Markdown")
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
