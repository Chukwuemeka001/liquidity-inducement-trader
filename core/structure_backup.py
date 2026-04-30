# core/structure.py - Improved to match your rules
import pandas as pd
from typing import Dict, Optional, Tuple

class MarketStructure:
    def detect_bos(self, df: pd.DataFrame, direction: str = "bullish") -> bool:
        if len(df) < 15:
            return False
        if direction == "bullish":
            prev_high = df['high'].iloc[:-8].max()   # look further back
            return df['high'].iloc[-1] > prev_high or df['close'].iloc[-1] > prev_high
        else:
            prev_low = df['low'].iloc[:-8].min()
            return df['low'].iloc[-1] < prev_low or df['close'].iloc[-1] < prev_low

    def detect_mbms(self, df: pd.DataFrame, direction: str = "bullish") -> Optional[Tuple[float, float]]:
        """Find first internal BOS inside pullback (your mbms)"""
        if len(df) < 20:
            return None

        # Look for pullback then internal break
        for i in range(10, len(df)-5):
            segment = df.iloc[i-10:i+5]
            if self.detect_bos(segment, direction):
                # SC candle = last opposing candle
                sc_high = df['high'].iloc[i-1]
                sc_low = df['low'].iloc[i-1]
                return (sc_low, sc_high)
        return None

    def find_pri_poi(self, df: pd.DataFrame, direction: str = "bullish") -> Dict:
        bos = self.detect_bos(df, direction)
        mbms_zone = self.detect_mbms(df, direction)

        return {
            "valid": mbms_zone is not None,
            "pri_poi_zone": mbms_zone,
            "bos_detected": bos,
            "direction": direction,
            "reason": "PRI POI + mbms found" if mbms_zone else "No mbms detected yet"
        }
