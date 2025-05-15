from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create database engine
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./stock_sentiment.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class StockAnalysis(Base):
    __tablename__ = "stock_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    price = Column(Float)
    sentiment = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Watchlist(Base):
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    ticker = Column(String, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)

# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)

# Database operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_analysis(ticker, data):
    """Save stock analysis data to database."""
    db = SessionLocal()
    try:
        analysis = StockAnalysis(
            ticker=ticker,
            price=data['price'],
            sentiment=data['sentiment'],
            volume=data['volume'],
            timestamp=data['timestamp']
        )
        db.add(analysis)
        db.commit()
    except Exception as e:
        print(f"Error saving analysis: {e}")
        db.rollback()
    finally:
        db.close()

def get_recent_analysis(ticker, limit=10):
    """Get recent analysis data for a ticker."""
    db = SessionLocal()
    try:
        return db.query(StockAnalysis)\
            .filter(StockAnalysis.ticker == ticker)\
            .order_by(StockAnalysis.timestamp.desc())\
            .limit(limit)\
            .all()
    finally:
        db.close()

def add_to_watchlist(user_id, ticker):
    """Add a ticker to user's watchlist."""
    db = SessionLocal()
    try:
        watchlist_item = Watchlist(user_id=user_id, ticker=ticker)
        db.add(watchlist_item)
        db.commit()
    except Exception as e:
        print(f"Error adding to watchlist: {e}")
        db.rollback()
    finally:
        db.close()

def get_watchlist(user_id):
    """Get user's watchlist."""
    db = SessionLocal()
    try:
        return db.query(Watchlist)\
            .filter(Watchlist.user_id == user_id)\
            .order_by(Watchlist.added_at.desc())\
            .all()
    finally:
        db.close() 