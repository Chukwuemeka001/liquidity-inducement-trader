# core/poi.py
from .structure import MarketStructure
from typing import Dict

class POI:
    def identify_pri_poi(self, df, direction: str = "bullish") -> Dict:
        structure = MarketStructure()
        result = structure.find_pri_poi(df, direction)
        if result.get("valid") and result.get("pri_poi_zone"):
            return {
                "type": "PRI_POI",
                "zone": result["pri_poi_zone"],
                "valid": True,
                "sc_zone": result["pri_poi_zone"],
                "direction": direction
            }
        return {
            "valid": False,
            "reason": result.get("reason", "No PRI POI found"),
            "pri_poi_zone": None
        }
