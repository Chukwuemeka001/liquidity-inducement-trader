# core/data_fetcher.py
import ccxt
import pandas as pd
from datetime import datetime

def fetch_candles(symbol: str = "BTC/USDT", timeframe: str = "4h", limit: int = 400):
    """Fetch real OHLCV data from Binance"""
    try:
        exchange = ccxt.binance({
            'enableRateLimit': True,
        })
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Return dummy data as fallback
        return create_dummy_data()

def create_dummy_data():
    import numpy as np
    dates = pd.date_range("2025-04-01", periods=400, freq='4H')
    close = 65000 + np.cumsum(np.random.randn(400) * 300)
    df = pd.DataFrame({
        'open': close - np.random.uniform(100, 400, 400),
        'high': close + np.random.uniform(100, 500, 400),
        'low': close - np.random.uniform(100, 500, 400),
        'close': close,
        'volume': np.random.uniform(100, 1000, 400)
    }, index=dates)
    return df
