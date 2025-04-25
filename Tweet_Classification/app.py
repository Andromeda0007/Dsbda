from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os
from utils.model_utils import predict_sentiment, simple_sentiment_prediction

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load the trained model and vectorizer
model_path = os.path.join('models', 'sentiment_model.pkl')
vectorizer_path = os.path.join('models', 'vectorizer.pkl')

models_loaded = False
model = None
vectorizer = None

try:
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        models_loaded = True
    else:
        print("Warning: Model or vectorizer not found. Using fallback sentiment analysis.")
except Exception as e:
    print(f"Error loading models: {str(e)}. Using fallback sentiment analysis.")

# Stats (in a real app, these would come from a database)
stats = {
    'totalTweets': 2000,
    'positiveTweets': 1200,
    'negativeTweets': 800,
    'modelAccuracy': 0.85
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json(silent=True) or {}
    tweet_text = data.get('tweet', '').strip()
    
    if not tweet_text:
        return jsonify({'error': 'Tweet text is required'}), 400
    
    try:
        if models_loaded:
            result = predict_sentiment(tweet_text, vectorizer, model)
        else:
            result = simple_sentiment_prediction(tweet_text)
            
        return jsonify({
            'tweet': tweet_text,
            'sentiment': result,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)