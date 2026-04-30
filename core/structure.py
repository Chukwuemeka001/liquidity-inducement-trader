# core/structure.py - ChatGPT Engine (STRICT STRUCTURE LOGIC)

import pandas as pd
from typing import List, Tuple, Optional, Dict

class MarketStructure:

    # --- SWING DETECTION ---
    def find_swings(self, df: pd.DataFrame) -> Tuple[List[Tuple[int, float]], List[Tuple[int, float]]]:
        swing_highs = []
        swing_lows = []

        for i in range(2, len(df) - 2):
            if (
                df['high'].iloc[i] > df['high'].iloc[i-1] and
                df['high'].iloc[i] > df['high'].iloc[i-2] and
                df['high'].iloc[i] > df['high'].iloc[i+1] and
                df['high'].iloc[i] > df['high'].iloc[i+2]
            ):
                swing_highs.append((i, df['high'].iloc[i]))

            if (
                df['low'].iloc[i] < df['low'].iloc[i-1] and
                df['low'].iloc[i] < df['low'].iloc[i-2] and
                df['low'].iloc[i] < df['low'].iloc[i+1] and
                df['low'].iloc[i] < df['low'].iloc[i+2]
            ):
                swing_lows.append((i, df['low'].iloc[i]))

        return swing_highs, swing_lows


    # --- STRICT BOS ---
    def detect_bos(self, df: pd.DataFrame, direction: str = "bullish") -> bool:
        swing_highs, swing_lows = self.find_swings(df)

        if direction == "bullish":
            if not swing_highs:
                return False
            last_swing_high = swing_highs[-1][1]
            return df['close'].iloc[-1] > last_swing_high

        else:
            if not swing_lows:
                return False
            last_swing_low = swing_lows[-1][1]
            return df['close'].iloc[-1] < last_swing_low


    # --- MBMS (YOUR REAL LOGIC) ---
    def detect_mbms(self, df: pd.DataFrame, direction: str = "bullish") -> Optional[Tuple[float, float]]:
        """
        LL → LH → break LH → HH
        First valid internal break only
        """

        swing_highs, swing_lows = self.find_swings(df)

        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return None

        # Combine and sort swings
        structure = []
        for i, price in swing_lows:
            structure.append((i, price, "low"))
        for i, price in swing_highs:
            structure.append((i, price, "high"))

        structure.sort(key=lambda x: x[0])

        # Scan for LL → LH → break LH
        for i in range(2, len(structure) - 1):

            p1 = structure[i-2]
            p2 = structure[i-1]
            p3 = structure[i]

            # LL → LH → LL
            if (
                p1[2] == "low" and
                p2[2] == "high" and
                p3[2] == "low" and
                p3[1] < p1[1]
            ):
                lh_price = p2[1]

                # Look for break of LH
                for j in range(i+1, len(df)):
                    close_price = df['close'].iloc[j]

                    if close_price > lh_price:
                        # SC = last bearish candle before break
                        sc_index = j - 1
                        sc_high = df['high'].iloc[sc_index]
                        sc_low = df['low'].iloc[sc_index]

                        return (sc_low, sc_high)

        return None


    # --- PRI POI ---
    def find_pri_poi(self, df: pd.DataFrame, direction: str = "bullish") -> Dict:
        bos = self.detect_bos(df, direction)
        mbms = self.detect_mbms(df, direction)

        return {
            "valid": mbms is not None,
            "pri_poi_zone": mbms,
            "bos_detected": bos,
            "direction": direction
        }