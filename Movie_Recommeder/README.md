# Movie Recommender System

A content-based movie recommendation system that suggests similar movies based on movie descriptions using TF-IDF vectorization and cosine similarity.

## Features

- Content-based movie recommendation engine
- Clean and responsive web interface
- Automatic data preprocessing
- Displays movie overview and similarity percentage
- Responsive design for mobile and desktop

## Installation

1. Clone this repository
   ```
   git clone https://github.com/yourusername/movie-recommender.git
   cd movie-recommender
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the application
   ```
   python app.py
   ```

4. Open your browser and go to `http://localhost:5000`

## How It Works

1. The system uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert movie descriptions into vectors.
2. Cosine similarity is calculated between these vectors to determine how similar two movies are.
3. When a user searches for a movie, the system finds the most similar movies based on their descriptions.

## Dataset

The movie dataset is sourced from [GitHub](https://raw.githubusercontent.com/rashida048/Some-NLP-Projects/master/movie_dataset.csv) and contains movie titles and descriptions.

## Project Structure

```
movie-recommender/
│
├── data/                  # Data related files
│   └── preprocess.py      # Script to preprocess the dataset
│
├── models/                # Model related files
│   └── recommender.py     # Movie recommendation engine
│
├── static/                # Static files for the web interface
│   ├── css/
│   │   └── style.css      # CSS styling
│   └── js/
│       └── script.js      # Frontend JavaScript
│
├── templates/             # HTML templates
│   └── index.html         # Main page
│
├── app.py                 # Flask application
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Technologies Used

- Python
- Flask
- Pandas
- scikit-learn
- HTML/CSS/JavaScript
- Animate.css
- Font Awesome

## Future Enhancements

- Add movie posters and additional metadata
- Implement user accounts to track recommendations
- Add collaborative filtering for personalized recommendations
- Deploy to a cloud platform for public access