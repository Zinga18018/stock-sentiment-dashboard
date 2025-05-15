import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    """Calculate various technical indicators for the given price data."""
    indicators = {}
    
    # Simple Moving Averages
    indicators['SMA_20'] = df['Close'].rolling(window=20).mean()
    indicators['SMA_50'] = df['Close'].rolling(window=50).mean()
    indicators['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Exponential Moving Averages
    indicators['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    indicators['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    
    # MACD
    indicators['MACD'] = indicators['EMA_12'] - indicators['EMA_26']
    indicators['MACD_Signal'] = indicators['MACD'].ewm(span=9, adjust=False).mean()
    indicators['MACD_Hist'] = indicators['MACD'] - indicators['MACD_Signal']
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    indicators['BB_Middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    indicators['BB_Upper'] = indicators['BB_Middle'] + (bb_std * 2)
    indicators['BB_Lower'] = indicators['BB_Middle'] - (bb_std * 2)
    
    # Volume indicators
    indicators['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
    indicators['Volume_Ratio'] = df['Volume'] / indicators['Volume_SMA']
    
    # ATR (Average True Range)
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    indicators['ATR'] = true_range.rolling(14).mean()
    
    return indicators 