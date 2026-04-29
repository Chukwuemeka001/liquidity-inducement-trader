# core/poi.py
import pandas as pd
from typing import Dict
from .structure import MarketStructure

class POI:
    def identify_pri_poi(self, df: pd.DataFrame, direction: str = "bullish") -> Dict:
        """Full PRI POI with SC zone"""
        structure = MarketStructure()
        result = structure.find_pri_poi(df, direction)
        if result["valid"] and result.get("pri_poi_zone"):
            return {
                "type": "PRI_POI",
                "zone": result["pri_poi_zone"],
                "valid": True,
                "sc_zone": result["pri_poi_zone"],
                "direction": direction
            }
        return {"valid": False, "reason": result.get("reason", "Unknown")}
