import yfinance as yf
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import Input, Output

#import functions
from data import get_data
from window import fetch_stock_prices, calculate_fibonacci_levels, plot_stock_prices_with_plotly

app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#f2f2f2', 'padding': '20px'}, children=[
    html.H4('Stock price analysis', style={'color': 'black'}),
    dcc.Graph(id="time-series-chart"),
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
    html.Footer("Atharva Mehra and James Fourie", style={'textAlign': 'center', 'marginTop': '20px', 'color': 'gray'})

])
@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    start_date = '2024-02-01'
    end_date = '2024-03-25'
    stock_data = fetch_stock_prices(ticker, start_date, end_date)
    if stock_data is not None:
        high = np.max(stock_data['High'])
        low = np.min(stock_data['Low'])
        retracement_levels = calculate_fibonacci_levels(high, low)
        fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Stock Prices with Fibonacci Retracement Levels')
        
        # Adding Fibonacci retracement levels as horizontal lines
        for level in retracement_levels:
            fig.add_hline(y=level, line_dash="dash", line_color="orange", annotation_text=f'Fib {int(level)}%', annotation_position="bottom right")
        
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Price (USD)')
        return fig
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)

# symbol = 'MSFT'
# start_date = '2024-01-01'
# end_date = '2024-03-25'
# stock_data = fetch_stock_prices(symbol, start_date, end_date)
# if stock_data is not None:
#     high = np.max(stock_data['High'])
#     low = np.min(stock_data['Low'])
#     retracement_levels = calculate_fibonacci_levels(high, low)
#     plot_stock_prices_with_plotly(stock_data, retracement_levels)

#tickers = ['PANW', 'SHOP', 'META', 'TSM', 'NET', 'DELL', 'ON', 'CRM', 'SONY', 'CRWD', 'AMAT']
#print(get_data('TSM'))






