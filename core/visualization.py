# core/visualization.py
import plotly.graph_objects as go
import pandas as pd

def plot_with_poi(df: pd.DataFrame, pri_poi_zone=None, title="Price Action with POI"):
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Price"
    ))
    
    if pri_poi_zone:
        fig.add_shape(type="rect",
                      x0=df.index[0], x1=df.index[-1],
                      y0=pri_poi_zone[0], y1=pri_poi_zone[1],
                      fillcolor="rgba(0,255,0,0.2)", line=dict(color="green"))
    
    fig.update_layout(title=title, xaxis_title="Time", yaxis_title="Price")
    fig.show()
