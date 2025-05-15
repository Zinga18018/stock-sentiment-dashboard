from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def clean_text(text):
    """Clean and preprocess text for sentiment analysis."""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

def analyze_sentiment(texts):
    """Analyze sentiment of a list of texts using multiple methods."""
    if not texts:
        return 0.0
    
    # Initialize sentiment analyzers
    sia = SentimentIntensityAnalyzer()
    
    # Calculate sentiment scores
    vader_scores = []
    textblob_scores = []
    
    for text in texts:
        # Clean the text
        cleaned_text = clean_text(text)
        
        # VADER sentiment analysis
        vader_score = sia.polarity_scores(cleaned_text)['compound']
        vader_scores.append(vader_score)
        
        # TextBlob sentiment analysis
        blob = TextBlob(cleaned_text)
        textblob_scores.append(blob.sentiment.polarity)
    
    # Combine scores (weighted average)
    vader_avg = sum(vader_scores) / len(vader_scores) if vader_scores else 0
    textblob_avg = sum(textblob_scores) / len(textblob_scores) if textblob_scores else 0
    
    # Weighted average (VADER is generally more accurate for social media)
    final_score = (vader_avg * 0.7) + (textblob_avg * 0.3)
    
    return final_score

def get_sentiment_label(score):
    """Convert sentiment score to label."""
    if score >= 0.5:
        return "Very Positive"
    elif score >= 0.1:
        return "Positive"
    elif score > -0.1:
        return "Neutral"
    elif score > -0.5:
        return "Negative"
    else:
        return "Very Negative"

def analyze_sentiment_trend(texts, timestamps):
    """Analyze sentiment trend over time."""
    if not texts or not timestamps:
        return []
    
    # Sort texts and timestamps
    sorted_data = sorted(zip(timestamps, texts))
    timestamps, texts = zip(*sorted_data)
    
    # Calculate sentiment for each time period
    sentiments = []
    for text in texts:
        sentiment = analyze_sentiment([text])
        sentiments.append(sentiment)
    
    return list(zip(timestamps, sentiments))

def get_sentiment_breakdown(texts):
    """Get detailed sentiment breakdown."""
    sia = SentimentIntensityAnalyzer()
    
    # Initialize counters
    sentiment_counts = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }
    
    # Analyze each text
    for text in texts:
        cleaned_text = clean_text(text)
        scores = sia.polarity_scores(cleaned_text)
        
        if scores['compound'] >= 0.05:
            sentiment_counts['positive'] += 1
        elif scores['compound'] <= -0.05:
            sentiment_counts['negative'] += 1
        else:
            sentiment_counts['neutral'] += 1
    
    # Calculate percentages
    total = len(texts)
    if total > 0:
        return {
            'positive': (sentiment_counts['positive'] / total) * 100,
            'neutral': (sentiment_counts['neutral'] / total) * 100,
            'negative': (sentiment_counts['negative'] / total) * 100
        }
    return {'positive': 0, 'neutral': 0, 'negative': 0}
