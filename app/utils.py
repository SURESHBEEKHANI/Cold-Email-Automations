# Import the regular expression (re) module to work with regular expressions
import re

# Define a function named clean_text that takes a string (text) as input
def clean_text(text):
    # Remove HTML tags from the text using a regular expression
    text = re.sub(r'<[^>]*?>', '', text)
    
    # Remove URLs from the text using a regular expression that matches HTTP/HTTPS URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove special characters from the text, leaving only letters, numbers, and spaces
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    
    # Replace multiple consecutive spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Trim leading and trailing whitespace from the text
    text = text.strip()
    
    # Remove any remaining extra spaces within the text
    # This step splits the text by spaces and then joins it back together with a single space
    text = ' '.join(text.split())
    
    # Return the cleaned text
    return text
