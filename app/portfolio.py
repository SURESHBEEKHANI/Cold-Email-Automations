# Import the pandas library and alias it as pd for easier usage
import pandas as pd

# Import the chromadb library for managing the vector store
import chromadb

# Import the uuid module to generate unique identifiers
import uuid

# Define a class named Portfolio to manage portfolio data and interactions with the vector store
class Portfolio:
    # Constructor method to initialize the Portfolio object
    def __init__(self, file_path=r"C:\Users\SURESH BEEKHANI\Desktop\project-genai-cold-email-generator\app\resource\my_portfolio.csv"):
        # Store the file path of the CSV file in an instance variable
        self.file_path = file_path
        
        # Read the CSV file into a pandas DataFrame and store it in an instance variable
        self.data = pd.read_csv(file_path)
        
        # Create a PersistentClient for the vector store named 'vectorstore'
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        
        # Get or create a collection named 'portfolio' in the vector store
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    # Method to load portfolio data from the CSV file into the vector store
    def load_portfolio(self):
        # Check if the collection is empty; if it is, proceed to load data
        if not self.collection.count():
            # Iterate over each row in the DataFrame
            for _, row in self.data.iterrows():
                # Add the current row's data to the vector store collection
                # The 'Techstack' column is added as the document
                # The 'Links' column is added as metadata with the key 'links'
                # A unique ID is generated for each entry using uuid.uuid4()
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    # Method to query the vector store for links based on provided skills
    def query_links(self, skills):
        # Query the collection using the provided skills as the query text
        # Limit the number of results to 2
        # Extract and return the 'metadatas' (links) from the query results
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
