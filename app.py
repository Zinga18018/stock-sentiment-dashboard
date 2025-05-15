import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

# Import custom modules
from sentiment_analysis import analyze_sentiment
from data_fetcher import fetch_tweets, fetch_reddit_posts, fetch_news
from technical_analysis import calculate_technical_indicators
from database import init_db, save_analysis
from auth import login_required, create_user

# Load environment variables
load_dotenv()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# Page config
st.set_page_config(
    page_title="Advanced Stock Sentiment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📈 Stock Dashboard")
    
    # Theme toggle
    theme = st.radio("Theme", ["Light", "Dark"])
    
    # Authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Add proper authentication logic here
            st.session_state.authenticated = True
            st.experimental_rerun()
    else:
        st.write(f"Welcome, {username}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.experimental_rerun()
    
    # Watchlist
    st.subheader("Watchlist")
    new_ticker = st.text_input("Add to watchlist")
    if st.button("Add"):
        if new_ticker:
            st.session_state.watchlist.append(new_ticker.upper())
    
    for ticker in st.session_state.watchlist:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(ticker)
        with col2:
            if st.button("X", key=f"remove_{ticker}"):
                st.session_state.watchlist.remove(ticker)
                st.experimental_rerun()

# Main content
if st.session_state.authenticated:
    st.title("📈 Advanced Stock Sentiment Dashboard")

    # Ticker input
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input('Enter stock ticker (e.g., TSLA, AAPL):', 'TSLA')
    with col2:
        timeframe = st.selectbox(
            'Select timeframe',
            ['1D', '1W', '1M', '3M', '1Y', '5Y']
        )

    if st.button('Analyze'):
        with st.spinner('Fetching and analyzing data...'):
            # Fetch stock data
            stock = yf.Ticker(ticker)
            
            # Get historical data
            period_map = {
                '1D': '1d', '1W': '5d', '1M': '1mo',
                '3M': '3mo', '1Y': '1y', '5Y': '5y'
            }
            hist = stock.history(period=period_map[timeframe])
            
            # Technical Analysis
            indicators = calculate_technical_indicators(hist)
            
            # Create price chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price'
            ))
            
            # Add moving averages
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=indicators['SMA_20'],
                name='20-day SMA',
                line=dict(color='blue')
            ))
            
            fig.update_layout(
                title=f'{ticker} Stock Price',
                yaxis_title='Price',
                xaxis_title='Date',
                template='plotly_dark' if theme == 'Dark' else 'plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Technical Indicators
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("RSI", f"{indicators['RSI'][-1]:.2f}")
            with col2:
                st.metric("MACD", f"{indicators['MACD'][-1]:.2f}")
            with col3:
                st.metric("Volume", f"{hist['Volume'][-1]:,.0f}")
            
            # Sentiment Analysis
            st.subheader("Sentiment Analysis")
            
            # Fetch and analyze data from different sources
            tweets = fetch_tweets(ticker)
            reddit_posts = fetch_reddit_posts(ticker)
            news = fetch_news(ticker)
            
            # Calculate sentiment scores
            tweet_sentiment = analyze_sentiment(tweets)
            reddit_sentiment = analyze_sentiment(reddit_posts)
            news_sentiment = analyze_sentiment(news)
            
            # Display sentiment scores
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Twitter Sentiment", f"{tweet_sentiment:.2f}")
            with col2:
                st.metric("Reddit Sentiment", f"{reddit_sentiment:.2f}")
            with col3:
                st.metric("News Sentiment", f"{news_sentiment:.2f}")
            
            # Display recent social media posts
            st.subheader("Recent Social Media Posts")
            tab1, tab2, tab3 = st.tabs(["Twitter", "Reddit", "News"])
            
            with tab1:
                for tweet in tweets[:5]:
                    st.markdown(f"- {tweet}")
            
            with tab2:
                for post in reddit_posts[:5]:
                    st.markdown(f"- {post}")
            
            with tab3:
                for article in news[:5]:
                    st.markdown(f"- {article}")
            
            # Company Information
            st.subheader("Company Information")
            info = stock.info
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Company Profile**")
                st.write(f"Name: {info.get('longName', 'N/A')}")
                st.write(f"Sector: {info.get('sector', 'N/A')}")
                st.write(f"Industry: {info.get('industry', 'N/A')}")
                st.write(f"Market Cap: ${info.get('marketCap', 0):,.2f}")
            
            with col2:
                st.write("**Key Statistics**")
                st.write(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
                st.write(f"EPS: {info.get('trailingEps', 'N/A')}")
                st.write(f"Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%")
                st.write(f"52 Week High: ${info.get('fiftyTwoWeekHigh', 0):.2f}")
            
            # Save analysis to database
            save_analysis(ticker, {
                'price': hist['Close'][-1],
                'sentiment': (tweet_sentiment + reddit_sentiment + news_sentiment) / 3,
                'volume': hist['Volume'][-1],
                'timestamp': datetime.now()
            })
else:
    st.warning("Please login to access the dashboard.")

# Temporary workaround
# create_user("your_email@example.com", "your_email@example.com", "yourpassword")
