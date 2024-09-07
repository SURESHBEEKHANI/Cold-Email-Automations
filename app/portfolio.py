import pandas as pd  # type: ignore
import chromadb  # type: ignore
import uuid


class Portfolio:
    # Constructor method to initialize the Portfolio object
    def __init__(self, file_path='resource/my_portfolio.csv'):
        # Store the file path of the CSV file in an instance variable
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        
        # Initialize the Chroma client and create/get the collection
        self.chroma_client = chromadb.Client()  # Updated initialization method
        self.collection = self.chroma_client.create_collection(name="portfolio")

    def load_portfolio(self):
        # Check if the collection is empty; if it is, proceed to load data
        if self.collection.count() == 0:
            # Iterate over each row in the DataFrame
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        # Query the collection using the provided skills as the query text
        # Limit the number of results to 2
        # Extract and return the 'metadatas' (links) from the query results
        results = self.collection.query(query_texts=skills, n_results=2)
        return [result.get('metadatas') for result in results]

# Example usage
# portfolio = Portfolio()
# portfolio.load_portfolio()
# links = portfolio.query_links("Python")
# print(links)
