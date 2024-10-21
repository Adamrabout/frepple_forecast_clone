import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from sqlalchemy.orm import sessionmaker
from models import engine, Forecast
from forecast import generate_forecast
import base64
import io

# Connect to the database
Session = sessionmaker(bind=engine)
session = Session()

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define layout
app.layout = html.Div([
    html.H1("Frepple Forecast Clone"),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'marginBottom': '20px'
        },
        multiple=False
    ),
    
    html.Div(id='output-upload'),
    dcc.Graph(id='forecast-graph'),
    
    html.Button("Recalculate Forecast", id='recalculate-button'),
    html.Div(id='recalculate-output'),
])

# Callback to handle file upload
@app.callback(
    [Output('output-upload', 'children'),
     Output('forecast-graph', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def upload_and_forecast(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        # Generate forecast
        forecast_df = generate_forecast(df)

        # Plot the forecast
        fig = px.line(forecast_df, x='ds', y='yhat', title='Forecasted Demand')

        return f'File {filename} uploaded successfully.', fig
    return 'No file uploaded.', {}

# Callback to recalculate forecast
@app.callback(
    Output('recalculate-output', 'children'),
    [Input('recalculate-button', 'n_clicks')]
)
def recalculate_forecast(n_clicks):
    if n_clicks:
        return 'Recalculated successfully!'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
