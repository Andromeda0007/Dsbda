import pickle
import os
import pandas as pd

class MovieRecommender:
    def __init__(self):
        self.df = None
        self.cosine_sim = None
        self.load_model()
        
    def load_model(self):
        """Load preprocessed data and similarity matrix"""
        try:
            with open('./data/movies_df.pkl', 'rb') as f:
                self.df = pickle.load(f)
                
            with open('./data/cosine_sim.pkl', 'rb') as f:
                self.cosine_sim = pickle.load(f)
                
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("Model files not found. Please run preprocess.py first.")
            
    def get_recommendations(self, title, top_n=5):
        """
        Get movie recommendations based on the input title
        
        Args:
            title (str): The title of the movie
            top_n (int): Number of recommendations to return
            
        Returns:
            list: List of recommended movie titles and details
        """
        if self.df is None or self.cosine_sim is None:
            return {"error": "Model not loaded. Please preprocess the data first."}
        
        # Check if the movie exists in our dataset
        movie_matches = self.df[self.df['title'].str.lower() == title.lower()]
        
        if movie_matches.empty:
            # Try partial matching if exact match fails
            movie_matches = self.df[self.df['title'].str.lower().str.contains(title.lower())]
            
            if movie_matches.empty:
                return {"error": f"Movie '{title}' not found in the dataset."}
            else:
                # Return the first match and recommendations
                movie = movie_matches.iloc[0]
                idx = movie.name
        else:
            # Use the first exact match
            idx = movie_matches.index[0]
        
        # Get the similarity scores for this movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort the movies based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the indices of the top_n most similar movies (excluding the movie itself)
        movie_indices = [i[0] for i in sim_scores[1:top_n+1]]
        
        # Get the recommended movies with some additional details
        recommended_movies = []
        for i in movie_indices:
            movie_data = self.df.iloc[i]
            recommended_movies.append({
                'title': movie_data['title'],
                'overview': movie_data['description'][:200] + "..." if len(movie_data['description']) > 200 else movie_data['description'],
                'similarity': sim_scores[movie_indices.index(i) + 1][1] * 100  # Convert to percentage
            })
            
        movie_data = movie_matches.iloc[0]
        selected_movie = {
            'title': movie_data['title'],
            'overview': movie_data['description'][:200] + "..." if len(movie_data['description']) > 200 else movie_data['description']
        }
            
        return {
            "selected_movie": selected_movie,
            "recommendations": recommended_movies
        }