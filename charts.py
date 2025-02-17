import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Load data
file_path = 'CleanHistoricalDataSP500.csv'
data = pd.read_csv(file_path)

# Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.sort_values(by='Date', inplace=True)
data.set_index('Date', inplace=True)

# Daily Returns
data['Daily Return'] = data['Close'].pct_change() * 100

# Cumulative Returns
data['Cumulative Return'] = (1 + data['Daily Return'] / 100).cumprod()

# Annual Returns
data['Year'] = data.index.to_period('Y')
annual_returns = data.groupby('Year')['Close'].apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)

# Maximum Drawdowns
running_max = data['Close'].cummax()
drawdowns = (data['Close'] / running_max - 1) * 100

# Round percentages to 2 decimal places
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
    title='',
    xaxis_title='Date',
    yaxis_title='Growth of $1',
    hovermode='x unified',
    width=800,  
    height=400,  
    margin=dict(l=20, r=20, t=40, b=20), # Reduce margins
    autosize=False
)
pio.write_html(cumulative_returns_fig, file='cumulative_returns_chart.html')


# 2. Annual Returns Chart
annual_returns_fig = go.Figure()

# Add bars with conditional coloring
annual_returns_fig.add_trace(go.Bar(
    x=annual_returns.index.astype(str),
    y=annual_returns.values,
    name='Annual Returns',
    marker_color=['green' if val >= 0 else 'red' for val in annual_returns.values]  # Conditional coloring
))

years = annual_returns.index.astype(str)
tick_values = [year for year in years if int(year) % 10 == 0 and int(year) >= 1930]  # Filter years

annual_returns_fig.update_layout(
    title='',
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

pio.write_html(annual_returns_fig, file='annual_returns_chart.html')

# 3. Drawdowns Chart
drawdowns_fig = go.Figure()
drawdowns_fig.add_trace(go.Scatter(
    x=data.index,
    y=drawdowns,
    mode='lines',
    name='Drawdowns',
    line=dict(color='red')
))
drawdowns_fig.update_layout(
    title='',
    xaxis_title='Date',
    yaxis_title='Drawdown (%)',
    hovermode='x unified',
    width=800,  
    height=400,  
    margin=dict(l=20, r=20, t=40, b=20),  
    autosize=False  
)
pio.write_html(drawdowns_fig, file='drawdowns_chart.html')