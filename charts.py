import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import re

# Load data
file_path = 'CleanHistoricalDataSP500.csv'
data = pd.read_csv(file_path)

# Convert Date column to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.sort_values(by='Date', inplace=True)
data.set_index('Date', inplace=True)

# Calculate returns and drawdowns
data['Daily Return'] = data['Close'].pct_change() * 100
data['Cumulative Return'] = (1 + data['Daily Return'] / 100).cumprod()

data['Year'] = data.index.to_period('Y')
annual_returns = data.groupby('Year')['Close'].apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)

running_max = data['Close'].cummax()
drawdowns = (data['Close'] / running_max - 1) * 100

# Define historical events
events = {
    "COVID-19": ("2020-02-01", "2020-06-01"),
    "2008 Financial Crisis": ("2008-09-01", "2009-06-01"),
    "US Election 2020": ("2020-10-01", "2020-12-01"),
    "Dot-com Bubble": ("2000-03-01", "2002-10-01"),
    "9/11 Attacks": ("2001-09-11", "2001-12-31"),
    "Gulf War": ("1990-08-01", "1991-02-28")
}

# Function to sanitize filenames
def sanitize_filename(event_name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', event_name)

# Function to create charts with event highlighting
def create_chart_with_event(event_name, event_range, y_data, title, filename, chart_type='line'):
    fig = go.Figure()
    
    if chart_type == 'line':
        fig.add_trace(go.Scatter(
            x=data.index, y=y_data,
            mode='lines', name=title,
            line=dict(color='blue')
        ))
    elif chart_type == 'bar':
        fig.add_trace(go.Bar(
            x=annual_returns.index.astype(str),
            y=annual_returns.values,
            name=title,
            marker_color=['green' if val >= 0 else 'red' for val in annual_returns.values]
        ))
    
    # Only add the highlighted area if an event range is provided
    if event_range[0] and event_range[1]:
        fig.add_vrect(
            x0=event_range[0], x1=event_range[1],
            fillcolor='rgba(255,0,0,0.2)', layer='below',
            line_width=0
        )
    
    fig.update_layout(
        title=f'{title} - {event_name}' if event_name else title,
        xaxis_title='Year',
        yaxis_title=title,
        hovermode='x unified',
        width=800,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        autosize=False
    )
    pio.write_html(fig, file=filename)

# Generate event-highlighted charts
for event, date_range in events.items():
    safe_event = sanitize_filename(event)
    create_chart_with_event(event, date_range, data['Cumulative Return'], 'Cumulative Returns', f'cumulative_returns_{safe_event}.html')
    create_chart_with_event(event, date_range, annual_returns, 'Annual Returns', f'annual_returns_{safe_event}.html', 'bar')
    create_chart_with_event(event, date_range, drawdowns, 'Drawdowns', f'drawdowns_{safe_event}.html')

# Generate default charts
default_charts = {
    'cumulative_returns_chart.html': ('Cumulative Return', data['Cumulative Return'], 'line'),
    'annual_returns_chart.html': ('Annual Returns', annual_returns, 'bar'),
    'drawdowns_chart.html': ('Drawdowns', drawdowns, 'line')
}

for filename, (title, y_data, chart_type) in default_charts.items():
    create_chart_with_event(None, (None, None), y_data, title, filename, chart_type)
