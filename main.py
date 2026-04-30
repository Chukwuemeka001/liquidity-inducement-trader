# main.py
from core.structure import MarketStructure
from core.poi import POI
from core.liquidity import LiquidityEngine
from core.data_fetcher import fetch_candles
from core.visualization import plot_with_poi

print("🚀 Liquidity & Inducement Pure Price Action V2")
print("=" * 70)

df = fetch_candles("BTC/USDT", "4h", 500)

structure = MarketStructure()
poi_engine = POI()
liquidity = LiquidityEngine()

bos = structure.detect_bos(df, "bullish")
pri_poi_result = poi_engine.identify_pri_poi(df, "bullish")
inducement = liquidity.find_inducement_liquidity(df, "bullish")

print(f"\n📊 BTC/USDT 4H Results:")
print(f"BOS (Bullish): {bos}")
print(f"PRI POI Found: {pri_poi_result.get('valid')}")
if pri_poi_result.get('valid'):
    print(f"PRI POI Zone: {pri_poi_result.get('zone')}")

print(f"Inducement Liquidity: {inducement}")

try:
    plot_with_poi(df, pri_poi_result.get('zone'), "BTC/USDT 4H - PRI POI Detection")
except Exception as e:
    print(f"Plot skipped: {e}")

print("\n✅ Engine updated!")
