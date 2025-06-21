# Import the regular expression (re) module to work with regular expressions
import re

# Define a function named clean_text that takes a string (text) as input
def clean_text(text):
    # Remove HTML tags from the text using a regular expression
    text = re.sub(r'<[^>]*?>', '', text)
    
    # Remove URLs from the text using a regular expression that matches HTTP/HTTPS URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove excessive whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters but preserve punctuation and special characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Trim leading and trailing whitespace from the text
    text = text.strip()
    
    # Return the cleaned text
    return text
