import os
import sys
from flask import Flask, render_template, request, jsonify

# Add the project directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import the modules
from models.recommender import MovieRecommender
from data.preprocess import preprocess_data

app = Flask(__name__)

# Initialize the recommender model
recommender = MovieRecommender()

# Check if model data exists, if not, preprocess the data
if not os.path.exists('./data/movies_df.pkl') or not os.path.exists('./data/cosine_sim.pkl'):
    print("Preprocessing data for the first time...")
    preprocess_data()
    # Reload the model
    recommender = MovieRecommender()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint to get movie recommendations"""
    data = request.get_json()
    
    if not data or 'movie' not in data:
        return jsonify({"error": "Please provide a movie title"}), 400
    
    movie_title = data['movie']
    recommendations = recommender.get_recommendations(movie_title)
    
    return jsonify(recommendations)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True)