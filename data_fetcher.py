import tweepy
import praw
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize API clients
def init_twitter_api():
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError("Missing Twitter API credentials in environment variables.")
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def init_reddit_api():
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')
    if not all([client_id, client_secret, user_agent]):
        raise ValueError("Missing Reddit API credentials in environment variables.")
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def init_news_api():
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        raise ValueError("Missing News API key in environment variables.")
    return NewsApiClient(api_key=api_key)

# Fetch data from different sources
def fetch_tweets(ticker):
    """Fetch recent tweets about the given ticker."""
    try:
        api = init_twitter_api()
        query = f"${ticker} stock"
        tweets = api.search_tweets(q=query, lang="en", count=100)
        return [tweet.text for tweet in tweets]
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return ["Error fetching tweets. Please check your Twitter API credentials."]

def fetch_reddit_posts(ticker):
    """Fetch recent Reddit posts about the given ticker."""
    try:
        reddit = init_reddit_api()
        subreddits = ['stocks', 'investing', 'wallstreetbets']
        posts = []
        
        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            search_results = subreddit.search(ticker, limit=10)
            for post in search_results:
                posts.append(f"{post.title} - r/{subreddit_name}")
        
        return posts
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return ["Error fetching Reddit posts. Please check your Reddit API credentials."]

def fetch_news(ticker):
    """Fetch recent news articles about the given ticker."""
    try:
        newsapi = init_news_api()
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        articles = newsapi.get_everything(
            q=ticker,
            from_param=from_date,
            language='en',
            sort_by='relevancy'
        )
        
        return [f"{article['title']} - {article['source']['name']}" 
                for article in articles['articles']]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return ["Error fetching news. Please check your News API credentials."]

def fetch_company_info(ticker):
    """Fetch detailed company information."""
    try:
        # This would typically use a financial data API
        # For now, return placeholder data
        return {
            'name': f"{ticker} Company",
            'sector': 'Technology',
            'industry': 'Software',
            'market_cap': 1000000000,
            'pe_ratio': 25.5,
            'eps': 2.5,
            'dividend_yield': 0.02
        }
    except Exception as e:
        print(f"Error fetching company info: {e}")
        return {} 