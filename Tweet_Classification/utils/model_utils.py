from .helpers import clean_tweet_text

def predict_sentiment(tweet_text, vectorizer, model):
    """
    Predict sentiment of the given tweet text using the trained model
    
    Args:
        tweet_text (str): Text to analyze
        vectorizer: Trained CountVectorizer
        model: Trained MultinomialNB model
        
    Returns:
        str: 'Positive' or 'Negative'
    """
    try:
        # Clean text
        cleaned_text = clean_tweet_text(tweet_text)
        if not cleaned_text:
            return "Neutral"
            
        # Transform text
        features = vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = model.predict(features)[0]
        
        return "Positive" if prediction == 1 else "Negative"
    except Exception as e:
        print(f"Model prediction error: {str(e)}")
        return simple_sentiment_prediction(tweet_text)

def simple_sentiment_prediction(text):
    """
    Enhanced rule-based sentiment analysis
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: 'Positive', 'Negative', or 'Neutral'
    """
    if not isinstance(text, str) or not text.strip():
        return "Neutral"
        
    text = clean_tweet_text(text)
    if not text:
        return "Neutral"
    
    positive_words = {
        'good': 1, 'great': 2, 'excellent': 3, 'awesome': 2,
        'love': 3, 'like': 1, 'best': 2, 'amazing': 2,
        'happy': 2, 'joy': 2, 'wonderful': 2, 'perfect': 3
    }
    
    negative_words = {
        'bad': 1, 'worst': 3, 'hate': 3, 'terrible': 2,
        'awful': 2, 'poor': 1, 'sad': 2, 'angry': 2,
        'dislike': 1, 'horrible': 3, 'annoying': 2
    }
    
    # Calculate weighted scores
    pos_score = sum(positive_words.get(word, 0) for word in text.split())
    neg_score = sum(negative_words.get(word, 0) for word in text.split())
    
    # Determine sentiment with threshold
    if pos_score > neg_score + 1:
        return "Positive"
    elif neg_score > pos_score + 1:
        return "Negative"
    return "Neutral"