// Analysis history
let analysisHistory = JSON.parse(localStorage.getItem('analysisHistory')) || [];

// DOM Elements
const tweetInput = document.getElementById('tweet-input');
const analyzeBtn = document.getElementById('analyze-btn');
const resultContainer = document.getElementById('result-container');
const loadingOverlay = document.getElementById('loading');
const themeToggle = document.getElementById('theme-toggle');
const charCount = document.getElementById('char-count');
const clearHistoryBtn = document.getElementById('clear-history');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // Load stats
    fetchStats();
    
    // Load history
    updateHistoryUI();
    
    // Set up event listeners
    analyzeBtn.addEventListener('click', analyzeTweet);
    tweetInput.addEventListener('input', updateCharCount);
    tweetInput.addEventListener('keydown', handleTextareaKeydown);
    themeToggle.addEventListener('click', toggleTheme);
    clearHistoryBtn.addEventListener('click', clearHistory);
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.className = `${savedTheme}-mode`;
    updateThemeToggleIcon(savedTheme);
    
    // Initialize character count
    updateCharCount();
});

// Fetch stats from the API
async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        updateStatsUI(data);
    } catch (error) {
        console.error('Error fetching stats:', error);
        showToast('Failed to load statistics', 'error');
    }
}

// Update stats UI
function updateStatsUI(data) {
    document.getElementById('total-tweets').textContent = data.totalTweets.toLocaleString();
    document.getElementById('positive-tweets').textContent = data.positiveTweets.toLocaleString();
    document.getElementById('negative-tweets').textContent = data.negativeTweets.toLocaleString();
    document.getElementById('model-accuracy').textContent = `${(data.modelAccuracy * 100).toFixed(0)}%`;
}

// Analyze tweet
async function analyzeTweet() {
    const tweetText = tweetInput.value.trim();
    
    if (!tweetText) {
        showToast('Please enter some text to analyze', 'warning');
        tweetInput.focus();
        return;
    }
    
    if (tweetText.length > 280) {
        showToast('Tweet exceeds maximum length of 280 characters', 'warning');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ tweet: tweetText }),
        });
        
        if (!response.ok) {
            throw new Error(await response.text());
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        updateResultUI(data);
        addToHistory(data.tweet, data.sentiment);
        
        if (data.sentiment === 'Positive') {
            triggerConfetti();
        }
    } catch (error) {
        console.error('Error:', error);
        showToast(error.message || 'Failed to analyze tweet', 'error');
    } finally {
        showLoading(false);
    }
}

// Update result UI
function updateResultUI(data) {
    const resultTweet = document.getElementById('result-tweet');
    const sentimentBadge = document.getElementById('sentiment-badge');
    
    resultTweet.textContent = data.tweet;
    sentimentBadge.textContent = data.sentiment;
    sentimentBadge.className = `sentiment-badge ${data.sentiment.toLowerCase()}`;
    
    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

// Add analysis to history
function addToHistory(tweet, sentiment) {
    // Add to beginning of array
    analysisHistory.unshift({ 
        tweet, 
        sentiment,
        timestamp: new Date().toISOString()
    });
    
    // Keep only the last 50 items
    if (analysisHistory.length > 50) {
        analysisHistory = analysisHistory.slice(0, 50);
    }
    
    // Save to localStorage
    localStorage.setItem('analysisHistory', JSON.stringify(analysisHistory));
    
    // Update UI
    updateHistoryUI();
}

// Update history UI
function updateHistoryUI() {
    const historyList = document.getElementById('history-list');
    
    if (analysisHistory.length === 0) {
        historyList.innerHTML = `
            <div class="empty-state">
                <img src="{{ url_for('static', filename='images/empty.svg') }}" alt="No history" class="empty-icon">
                <p>No analysis history yet</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = analysisHistory.map(item => `
        <div class="history-item">
            <div class="history-text">${escapeHtml(item.tweet)}</div>
            <div class="history-sentiment ${item.sentiment.toLowerCase()}">
                ${item.sentiment} • ${formatDate(item.timestamp)}
            </div>
        </div>
    `).join('');
}

// Clear history
function clearHistory() {
    if (analysisHistory.length === 0) return;
    
    if (confirm('Are you sure you want to clear all analysis history?')) {
        analysisHistory = [];
        localStorage.removeItem('analysisHistory');
        updateHistoryUI();
        showToast('History cleared', 'success');
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format date for display
function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString();
}

// Update character count
function updateCharCount() {
    const count = tweetInput.value.length;
    charCount.textContent = `${count}/280`;
    
    if (count > 280) {
        charCount.style.color = 'var(--negative)';
    } else {
        charCount.style.color = 'var(--text-secondary)';
    }
}

// Handle Enter key in textarea
function handleTextareaKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeTweet();
    }
}

// Show/hide loading overlay
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// Toggle dark/light theme
function toggleTheme() {
    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.body.className = `${newTheme}-mode`;
    localStorage.setItem('theme', newTheme);
    updateThemeToggleIcon(newTheme);
}

// Update theme toggle icon
function updateThemeToggleIcon(theme) {
    const icon = themeToggle.querySelector('.toggle-icon');
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Trigger confetti effect
function triggerConfetti() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
}

// Add toast styles dynamically
const toastStyles = document.createElement('style');
toastStyles.textContent = `
.toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 24px;
    border-radius: 8px;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    box-shadow: var(--shadow);
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.3s;
}

.toast.show {
    opacity: 1;
}

.toast-success {
    border-left: 4px solid var(--positive);
}

.toast-error {
    border-left: 4px solid var(--negative);
}

.toast-warning {
    border-left: 4px solid #f59e0b;
}

.toast-info {
    border-left: 4px solid var(--primary);
}
`;
document.head.appendChild(toastStyles);