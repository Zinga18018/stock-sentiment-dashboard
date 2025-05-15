# 📈 Stock Sentiment Dashboard

A modern Streamlit web app for analyzing stock sentiment using real-time data from Twitter, Reddit, and news sources, combined with technical analysis and company fundamentals.

---

## Features
- **User Authentication**: Secure login for dashboard access
- **Stock Data Visualization**: Interactive charts with technical indicators (RSI, MACD, etc.)
- **Sentiment Analysis**: Aggregates and analyzes sentiment from Twitter, Reddit, and news
- **Watchlist**: Track your favorite tickers
- **Company Info**: Key statistics and profile for each stock
- **Database Storage**: Saves analysis results for future reference

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-dashboard.git
   cd stock-sentiment-dashboard
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file** (see below)

5. **Initialize the database** (optional, usually auto-created)
   ```bash
   python -c "from database import init_db; init_db()"
   ```

6. **Create your first user**
   - Create a file `create_user_script.py`:
     ```python
     from auth import create_user
     create_user("your_email@example.com", "your_email@example.com", "yourpassword")
     print("User created!")
     ```
   - Run:
     ```bash
     python create_user_script.py
     ```

7. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 Environment Variables (`.env`)
Create a `.env` file in your project root with the following:

```env
# Twitter API credentials
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Reddit API credentials
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_reddit_user_agent

# NewsAPI credentials
NEWS_API_KEY=your_newsapi_key
```

**Never commit your `.env` file!**

---

## 🛡️ Security Best Practices
- `.env` and all secrets are in `.gitignore` by default
- Never hardcode API keys or passwords in code
- Use strong, unique passwords for user accounts
- Re-enable authentication before deploying publicly

---

## ☁️ Deployment Tips
- Set environment variables in your cloud provider’s dashboard (not in code)
- Use a production-ready database for scaling (e.g., PostgreSQL)
- Monitor API usage to avoid rate limits
- Comply with all third-party API terms of service

---

## 📚 License
MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋‍♂️ Questions or Contributions?
Open an issue or pull request on GitHub!
