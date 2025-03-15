import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio


file_path = 'CleanHistoricalDataBitcoin.csv'
data = pd.read_csv(file_path)


data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.sort_values(by='Date', inplace=True)
data.set_index('Date', inplace=True)



data['Daily Return'] = data['Close'].pct_change() * 100



data['Cumulative Return'] = (1 + data['Daily Return'] / 100).cumprod()


data['Year'] = data.index.to_period('Y')
annual_returns = data.groupby('Year')['Close'].apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)

running_max = data['Close'].cummax()
drawdowns = (data['Close'] / running_max - 1) * 100


data['Daily Return'] = data['Daily Return'].round(2)
data['Cumulative Return'] = data['Cumulative Return'].round(2)
annual_returns = annual_returns.round(2)
drawdowns = drawdowns.round(2)


#Interactive charts with Plotly


# 1. Cumulative Returns Chart
cumulative_returns_fig = go.Figure()
cumulative_returns_fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Cumulative Return'],
    mode='lines',
    name='Cumulative Returns',
    line=dict(color='blue')
))
cumulative_returns_fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Growth of $1',
    hovermode='x unified',
    width=800,  
    height=400,  
    margin=dict(l=20, r=20, t=40, b=20), 
    autosize=False
)
pio.write_html(cumulative_returns_fig, file='bitcoin_cumulative_returns_chart.html')

# 2. Annual Returns Chart
annual_returns_fig = go.Figure()
annual_returns_fig.add_trace(go.Bar(
    x=annual_returns.index.astype(str),
    y=annual_returns.values,
    name='Annual Returns',
    marker_color='skyblue'
))
years = annual_returns.index.astype(str) 
tick_values = [year for year in years if int(year) % 10 == 0 and int(year) >= 1930]  # Filter years

annual_returns_fig.update_layout(
    title='Annual Returns',
    xaxis_title='Year',
    yaxis_title='Return (%)',
    hovermode='x unified',
    width=800,  
    height=400,  
    margin=dict(l=20, r=20, t=40, b=20),  
    autosize=False,  
    xaxis=dict(
        tickmode='array',  
        tickvals=tick_values,  
        ticktext=tick_values 
    )
)
pio.write_html(annual_returns_fig, file='bitcoin_annual_returns_chart.html')






