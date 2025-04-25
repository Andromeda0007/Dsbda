import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

def preprocess_data():
    # Load the dataset from the URL
    url = 'https://raw.githubusercontent.com/rashida048/Some-NLP-Projects/master/movie_dataset.csv'
    df = pd.read_csv(url)
    
    # Data Preprocessing: Drop rows with missing movie titles or descriptions
    df = df.dropna(subset=['title', 'description'])
    print(f"Number of movies after cleaning: {len(df)}")
    
    # Feature Extraction: Convert movie descriptions into TF-IDF features
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Transform the 'description' column to tf-idf features
    tfidf_matrix = tfidf.fit_transform(df['description'])
    print(f"Shape of the tf-idf matrix: {tfidf_matrix.shape}")
    
    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print(f"Cosine similarity matrix shape: {cosine_sim.shape}")
    
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Save the preprocessed data and model artifacts
    with open('./data/movies_df.pkl', 'wb') as f:
        pickle.dump(df, f)
        
    with open('./data/cosine_sim.pkl', 'wb') as f:
        pickle.dump(cosine_sim, f)
        
    with open('./data/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    
    print("Preprocessing complete. Data and model artifacts saved.")
    return df, cosine_sim, tfidf

if __name__ == "__main__":
    preprocess_data()