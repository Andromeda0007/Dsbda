import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

def train_model(csv_file):
    """
    Train a sentiment analysis model using the provided CSV file
    
    Args:
        csv_file (str): Path to the CSV file containing tweets
        
    Returns:
        tuple: Model accuracy and stats
    """
    # Create directory for models if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Load dataset
    df = pd.read_csv(csv_file)
    print(f"Dataset loaded with {len(df)} tweets")
    
    # Create simple sentiment labels (positive/negative) based on common words
    positive_words = ['good', 'great', 'love', 'best', 'amazing', 'excellent']
    negative_words = ['bad', 'worst', 'hate', 'terrible', 'poor', 'useless']
    
    # Simple labeling function
    def label_sentiment(text):
        if not isinstance(text, str):
            return 0
        text = text.lower()
        pos_count = sum(word in text for word in positive_words)
        neg_count = sum(word in text for word in negative_words)
        return 1 if pos_count > neg_count else 0
    
    # Apply labels
    df['sentiment'] = df['tweet'].apply(label_sentiment)
    positive_count = df['sentiment'].sum()
    negative_count = len(df) - positive_count
    
    print(f"Positive tweets: {positive_count}")
    print(f"Negative tweets: {negative_count}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['tweet'], df['sentiment'], test_size=0.2, random_state=42
    )
    
    # Convert text to features
    vectorizer = CountVectorizer(max_features=3000)
    X_train_features = vectorizer.fit_transform(X_train)
    X_test_features = vectorizer.transform(X_test)
    
    # Train model
    model = MultinomialNB()
    model.fit(X_train_features, y_train)
    
    # Evaluate
    accuracy = model.score(X_test_features, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save model and vectorizer
    joblib.dump(model, os.path.join('models', 'sentiment_model.pkl'))
    joblib.dump(vectorizer, os.path.join('models', 'vectorizer.pkl'))
    print("Model saved successfully")
    
    # Return stats
    stats = {
        'totalTweets': len(df),
        'positiveTweets': positive_count,
        'negativeTweets': negative_count,
        'modelAccuracy': accuracy
    }
    
    return accuracy, stats

if __name__ == "__main__":
    # Check if CSV file is provided as an argument
    import sys
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = 'data_science.csv'  # Default file
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    
    train_model(csv_file)
