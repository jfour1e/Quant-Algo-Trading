import yfinance as yf
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime, timedelta
import schedule
import time

#import functions
from data import fetch_rsi, fetch_macd, fetch_stock_prices
from window import calculate_fibonacci_levels

app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#f2f2f2', 'padding': '20px'}, children=[
    html.H4('Stock price analysis', style={'color': 'black'}),
    dcc.Graph(id="stock-price-chart"),
    dcc.Graph(id="rsi-chart"),
    dcc.Graph(id="macd-chart"),
    html.Div([
        html.P("Select stock:", style={'fontSize': 18}),
        dcc.Dropdown(
            id="ticker",
            options=[
                {"label": "Palo Alto Networks (PANW)", "value": "PANW"},
                {"label": "Shopify (SHOP)", "value": "SHOP"},
                {"label": "Meta Platforms (META)", "value": "META"},
                {"label": "Taiwan Semiconductor Manufacturing (TSM)", "value": "TSM"},
                {"label": "Cloudflare (NET)", "value": "NET"},
                {"label": "Dell Technologies (DELL)", "value": "DELL"},
                {"label": "ON Semiconductor (ON)", "value": "ON"},
                {"label": "Salesforce (CRM)", "value": "CRM"},
                {"label": "Sony Corporation (SONY)", "value": "SONY"},
                {"label": "CrowdStrike Holdings (CRWD)", "value": "CRWD"},
                {"label": "Applied Materials (AMAT)", "value": "AMAT"}
            ],
            value="PANW",
            clearable=False,
            style={'fontSize': 16, 'width': '50%'}  # Adjust the width of the dropdown
        ),
    ], style={'display': 'flex', 'alignItems': 'center'}),  # Align dropdown vertically in center
    html.Footer("Atharva Mehra and James Fourie", style={'textAlign': 'center', 'marginTop': '20px', 'color': 'gray'}),
    dcc.Interval(
        id='interval-component',
        interval=15*60*1000,  # in milliseconds
        n_intervals=0
    )
])
# Callback to update data every 15 minutes
@app.callback(
    [Output("stock-price-chart", "figure"),
     Output("rsi-chart", "figure"),
     Output("macd-chart", "figure")],
    [Input("ticker", "value"),
     Input("interval-component", "n_intervals")])

def display_time_series(ticker, _):
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    stock_data = fetch_stock_prices(ticker, start_date, end_date)
    if stock_data is not None:
        high = np.max(stock_data['High'])
        low = np.min(stock_data['Low'])
        retracement_levels = calculate_fibonacci_levels(high, low)
        
        # Fetch RSI data
        rsi_data = fetch_rsi(ticker, start_date, end_date)
        
        # Fetch MACD data
        macd_data = fetch_macd(ticker, start_date, end_date)

        # Calculate MACD histogram
        macd_histogram = macd_data['MACD'] - macd_data['MACD Signal']
        
        # Create figure for stock price and Fibonacci levels
        stock_price_fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Stock Prices with Fibonacci Retracement Levels')
        for level in retracement_levels:
            stock_price_fig.add_hline(y=level, line_dash="dash", line_color="orange", annotation_text=f'Fib {int(level)}%', annotation_position="bottom right")
        
        # Create figure for RSI
        rsi_fig = px.line(rsi_data, x=rsi_data.index, y='RSI', title=f'{ticker} RSI')
        
        # Create figure for MACD
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(x=macd_data.index, y=macd_data['MACD'], mode='lines', name='MACD'))
        macd_fig.add_trace(go.Scatter(x=macd_data.index, y=macd_data['MACD Signal'], mode='lines', name='MACD Signal'))
        macd_fig.add_trace(go.Bar(x=macd_data.index, y=macd_histogram, name='MACD Histogram', marker_color='rgba(0, 128, 0, 0.5)'))  # Adjust color and opacity
        macd_fig.update_layout(barmode='overlay', title=f'{ticker} MACD', xaxis_title='Date', yaxis_title='MACD')
        macd_fig.update_traces(marker_line_width=1, marker_line_color="black")  # Adjust width and color of bar outlines


        # Generate buy and sell signals for MACD
        signals = []
        positions = []
        prev_signal = None
        
        for i in range(1, len(macd_data)):
            if macd_data['MACD'][i] > macd_data['MACD Signal'][i] and macd_data['MACD'][i-1] < macd_data['MACD Signal'][i-1]:
                signals.append('Buy')
                positions.append(macd_data.index[i])
                prev_signal = 'Buy'
            elif macd_data['MACD'][i] < macd_data['MACD Signal'][i] and macd_data['MACD'][i-1] > macd_data['MACD Signal'][i-1]:
                signals.append('Sell')
                positions.append(macd_data.index[i])
                prev_signal = 'Sell'
            else:
                signals.append(None)
                positions.append(None)

        # Plot buy and sell signals on MACD graph
        for i in range(len(signals)):
            if signals[i] is not None:
                signal_color = 'green' if signals[i] == 'Buy' else 'red'
                macd_fig.add_trace(go.Scatter(x=[positions[i]], y=[macd_data.loc[positions[i], 'MACD']], mode='markers', name=signals[i], marker=dict(color=signal_color, size=10), showlegend=False))

        # Update layout for MACD graph
        macd_fig.update_layout(showlegend=True)

        return stock_price_fig, rsi_fig, macd_fig
    else:
        return {}, {}, {}

if __name__ == '__main__':
    app.run_server(debug=True)

# def display_time_series(ticker):
#     start_date = '2024-02-01'
#     end_date = '2024-03-25'
#     stock_data = fetch_stock_prices(ticker, start_date, end_date)
#     if stock_data is not None:
#         high = np.max(stock_data['High'])
#         low = np.min(stock_data['Low'])
#         retracement_levels = calculate_fibonacci_levels(high, low)
#         fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Stock Prices with Fibonacci Retracement Levels')
        
#         # Adding Fibonacci retracement levels as horizontal lines
#         for level in retracement_levels:
#             fig.add_hline(y=level, line_dash="dash", line_color="orange", annotation_text=f'Fib {int(level)}%', annotation_position="bottom right")
        
#         fig.update_xaxes(title_text='Date')
#         fig.update_yaxes(title_text='Price (USD)')
#         return fig
#     else:
#         return {}