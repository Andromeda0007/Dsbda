import re
from datetime import datetime

def clean_tweet_text(text):
    """Clean tweet text before analysis"""
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user mentions
    text = re.sub(r'@\w+', '', text)
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Convert to lowercase
    text = text.lower().strip()
    
    return text

def format_timestamp(iso_string):
    """Format ISO timestamp for display"""
    return datetime.fromisoformat(iso_string).strftime('%b %d, %Y %I:%M %p')