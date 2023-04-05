import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

# load the CSV file into a Pandas dataframe
df = pd.read_csv("earthquakes.csv")
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S.%fZ')

# create a Dash app
app = dash.Dash(__name__)

# define the app layout
app.layout = html.Div([
    dcc.Graph(
        id="map",
        figure=px.scatter_mapbox(df, lat="latitude", lon="longitude", color="mag", zoom=3,
                                 mapbox_style="open-street-map"),
        style={"width": "1200px", "height": "600px"}
    ),
    dcc.RangeSlider(
        id="date-slider",
        min=df['time'].min().timestamp(),
        max=df['time'].max().timestamp(),
        value=[df['time'].min().timestamp(), df['time'].max().timestamp()],
        marks={
            timestamp: datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            for timestamp in pd.date_range(start=df['time'].min(), end=df['time'].max()).astype(int) / 10**9
        },
        step=None,
    )
])


# callback to update the map based on the selected date range
@app.callback(
    Output("map", "figure"),
    Input("date-slider", "value")
)
def update_map(date_range):
    start_date = datetime.fromtimestamp(date_range[0])
    end_date = datetime.fromtimestamp(date_range[1])
    filtered_df = df.loc[(df['time'] >= start_date) & (df['time'] <= end_date)]
    return px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", size="mag", zoom=3,
                             mapbox_style="open-street-map")


# run the app
if __name__ == "__main__":
    app.run_server(debug=True)
