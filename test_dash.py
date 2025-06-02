import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import uvicorn
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

# Sample DataFrame
data = {'Date': pd.date_range(start='2025-06-01', periods=10, freq='D'),
        'Sales': [100, 150, 200, 130, 170, 210, 190, 250, 230, 280]}
df = pd.DataFrame(data)

# Create Dash app
dash_app = dash.Dash(__name__, requests_pathname_prefix="/dash/")
dash_app.layout = html.Div([
    html.H1("Sales Over Time"),
    dcc.Graph(id='sales-chart', figure=px.line(df, x='Date', y='Sales'))
])

# Create FastAPI app
app = FastAPI()

# Mount Dash app inside FastAPI
app.mount("/dash", WSGIMiddleware(dash_app.server))

if __name__ == "__main__":
    uvicorn.run("test_dash:app", host="127.0.0.1", port=9091, reload=True, log_level="debug")
