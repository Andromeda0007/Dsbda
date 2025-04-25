# Tweet Sentiment Analyzer

A web application that analyzes the sentiment of tweets using a machine learning model.

## Features

- Real-time sentiment analysis of text
- Clean and responsive user interface
- Analysis history tracking
- Statistics dashboard

## Project Structure

```
sentiment_analyzer/
├── app.py                  # Main Flask application
├── models/                 # Directory for trained models
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── utils/                  # Utility functions
├── train.py                # Script to train the model
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sentiment_analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Train the model (if you have a dataset):
   ```
   python train.py data_science.csv
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Enter a tweet in the text area
2. Click the "Analyze Sentiment" button
3. View the sentiment analysis result
4. Check the analysis history at the bottom of the page

## Model Training

The sentiment analysis model is trained using a Multinomial Naive Bayes classifier on a dataset of labeled tweets. The model works by:

1. Converting text to numerical features using CountVectorizer
2. Training a Naive Bayes classifier on these features
3. Predicting sentiment based on the learned patterns

## License

[MIT License](LICENSE)