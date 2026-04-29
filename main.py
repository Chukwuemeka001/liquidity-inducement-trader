# main.py
import pandas as pd
from core.structure import MarketStructure
from core.poi import POI
from core.liquidity import LiquidityEngine

print("🚀 Liquidity & Inducement Detection Engine V2")
print("=" * 60)

# Test with dummy data (we'll replace with real data soon)
def create_dummy_data():
    dates = pd.date_range("2025-04-01", periods=50)
    data = {
        'open':  [65000 + i*100 + (i%5)*50 for i in range(50)],
        'high':  [65100 + i*100 + (i%5)*80 for i in range(50)],
        'low':   [64900 + i*100 - (i%5)*60 for i in range(50)],
        'close': [65050 + i*100 + (i%3)*30 for i in range(50)],
    }
    df = pd.DataFrame(data, index=dates)
    # Simulate a BOS + pullback
    df.loc[df.index[-10:], 'low'] = df['low'].iloc[-10:] - 800
    df.loc[df.index[-5:], 'high'] = df['high'].iloc[-5:] + 1200
    return df

df = create_dummy_data()

# Run detection
structure = MarketStructure()
poi_engine = POI()
liquidity = LiquidityEngine()

bos = structure.detect_bos(df, "bullish")
pri_poi = poi_engine.identify_pri_poi(df, "bullish")
inducement = liquidity.find_inducement_liquidity(df, "bullish")

print(f"BOS Detected: {bos}")
print(f"PRI POI: {pri_poi}")
print(f"Inducement Liquidity: {inducement}")

print("\n✅ Detection engine initialized successfully!")
