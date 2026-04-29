# core/structure.py
import pandas as pd
from typing import List, Tuple, Optional, Dict

class MarketStructure:
    def __init__(self):
        self.bos_history = []
        self.mbms_history = []

    def detect_bos(self, df: pd.DataFrame, direction: str = "bullish") -> bool:
        """Detect Break of Structure (wick or close counts)"""
        if len(df) < 5:
            return False

        if direction == "bullish":
            prev_high = df['high'].iloc[:-1].max()
            current_high = df['high'].iloc[-1]
            current_close = df['close'].iloc[-1]
            return current_high > prev_high or current_close > prev_high
        else:  # bearish
            prev_low = df['low'].iloc[:-1].min()
            current_low = df['low'].iloc[-1]
            current_close = df['close'].iloc[-1]
            return current_low < prev_low or current_close < prev_low

    def detect_mbms(self, pullback_df: pd.DataFrame, direction: str = "bullish") -> Optional[Tuple[float, float]]:
        """Detect Minor Break of Structure inside pullback"""
        if len(pullback_df) < 5:
            return None

        for i in range(3, len(pullback_df)):
            segment = pullback_df.iloc[:i+1]
            if self.detect_bos(segment, direction):
                sc_high = pullback_df['high'].iloc[i-1]
                sc_low = pullback_df['low'].iloc[i-1]
                return (sc_low, sc_high)  # SC zone as PRI POI
        return None

    def find_pri_poi(self, df: pd.DataFrame, direction: str = "bullish") -> Dict:
        """Main PRI POI detection"""
        if len(df) < 20:
            return {"valid": False, "reason": "not enough data"}

        bos_detected = self.detect_bos(df, direction)
        if not bos_detected:
            return {"valid": False, "reason": "no BOS yet"}

        pri_poi_zone = self.detect_mbms(df, direction)

        return {
            "valid": pri_poi_zone is not None,
            "pri_poi_zone": pri_poi_zone,
            "bos_detected": bos_detected,
            "direction": direction,
            "reason": "PRI POI found" if pri_poi_zone else "No mbms found"
        }
