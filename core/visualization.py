# core/visualization.py - Improved local zone marking
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Tuple

def plot_with_poi(df: pd.DataFrame, pri_poi_zone: Optional[Tuple[float, float]] = None, title="BTC/USDT 4H - PRI POI Detection"):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Price"
    ))

    if pri_poi_zone and len(df) > 10:
        low, high = pri_poi_zone
        # Draw local zone box around last ~30 candles (more realistic)
        start_idx = max(0, len(df) - 40)
        end_idx = len(df) - 1
        
        fig.add_shape(
            type="rect",
            x0=df.index[start_idx], x1=df.index[end_idx],
            y0=low, y1=high,
            fillcolor="rgba(0, 255, 100, 0.25)",
            line=dict(color="lime", width=2),
            name="PRI POI Zone"
        )

        # Add label
        fig.add_annotation(
            x=df.index[end_idx - 5],
            y=high,
            text="PRI POI",
            showarrow=False,
            font=dict(color="lime", size=14),
            bgcolor="rgba(0,0,0,0.7)"
        )

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Price",
        height=700
    )
    fig.show()
