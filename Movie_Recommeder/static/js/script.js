document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM elements
    const movieInput = document.getElementById('movie-input');
    const searchBtn = document.getElementById('search-btn');
    const loadingEl = document.getElementById('loading');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    const selectedMovieContainer = document.getElementById('selected-movie');
    const selectedTitle = document.getElementById('selected-title');
    const selectedOverview = document.getElementById('selected-overview');
    const resultsContainer = document.getElementById('results-container');
    const recommendationsList = document.getElementById('recommendations-list');
    
    // Add event listeners
    searchBtn.addEventListener('click', getRecommendations);
    movieInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            getRecommendations();
        }
    });
    
    // Function to get movie recommendations
    function getRecommendations() {
        const movieTitle = movieInput.value.trim();
        
        if (!movieTitle) {
            showError('Please enter a movie title');
            return;
        }
        
        // Show loading spinner, hide other containers
        loadingEl.style.display = 'flex';
        errorContainer.style.display = 'none';
        selectedMovieContainer.style.display = 'none';
        resultsContainer.style.display = 'none';
        
        // Make API request
        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie: movieTitle })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            loadingEl.style.display = 'none';
            
            if (data.error) {
                showError(data.error);
                return;
            }
            
            // Display the selected movie
            selectedTitle.textContent = data.selected_movie.title;
            selectedOverview.textContent = data.selected_movie.overview;
            selectedMovieContainer.style.display = 'block';
            
            // Display the recommendations
            displayRecommendations(data.recommendations);
        })
        .catch(error => {
            loadingEl.style.display = 'none';
            showError('An error occurred. Please try again later.');
            console.error('Error:', error);
        });
    }
    
    // Function to display recommendations
    function displayRecommendations(recommendations) {
        // Clear previous recommendations
        recommendationsList.innerHTML = '';
        
        if (recommendations.length === 0) {
            showError('No recommendations found');
            return;
        }
        
        // Create a card for each recommendation
        recommendations.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.className = 'movie-card animate__animated animate__fadeIn';
            
            const title = document.createElement('h3');
            title.textContent = movie.title;
            
            const overview = document.createElement('p');
            overview.textContent = movie.overview;
            
            const similarity = document.createElement('div');
            similarity.className = 'similarity';
            similarity.textContent = `Similarity: ${movie.similarity.toFixed(1)}%`;
            
            movieCard.appendChild(title);
            movieCard.appendChild(overview);
            movieCard.appendChild(similarity);
            
            recommendationsList.appendChild(movieCard);
        });
        
        // Show results container
        resultsContainer.style.display = 'block';
        
        // Apply staggered animation to cards
        const cards = document.querySelectorAll('.movie-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    // Function to show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.style.display = 'block';
    }
});