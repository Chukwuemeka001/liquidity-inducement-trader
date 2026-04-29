# core/liquidity.py
import pandas as pd
from typing import Dict, Optional

class LiquidityEngine:
    def find_inducement_liquidity(self, df: pd.DataFrame, direction: str = "bullish") -> Optional[float]:
        """First low/high after BOS = Inducement Liquidity"""
        if len(df) < 10:
            return None
        # Placeholder - will be improved with real BOS detection
        if direction == "bullish":
            return df['low'].iloc[-5:].min()  # temporary logic
        return None

    def find_pri_liquidity(self, df: pd.DataFrame) -> Optional[float]:
        """Liquidity after mbms"""
        return df['low'].iloc[-3:].min()  # temporary
