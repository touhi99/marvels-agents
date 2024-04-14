import os 
import re 

def check_data_exists(directory="data"):
    """Check if there is any data file in the specified directory."""
    return any(os.path.isfile(os.path.join(directory, f)) for f in os.listdir(directory))

def clean_html(raw_html):
    """Utility function to remove HTML tags from descriptions."""
    clean_text = re.sub(r'<.*?>', '', raw_html)
    return clean_text