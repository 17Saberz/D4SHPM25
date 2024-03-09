from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("mean.csv")
data["DATE"] = pd.to_datetime(data["DATE"], format="%Y-%m-%d")
data.sort_values("DATE", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "PM2.5 Forecaster!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🫥", className="header-emoji"),
                html.H1(
                    children="Air's Compnents", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in ['PM25','CO', 'NO2', 'TEMP', 'RH']
                            ],
                            value="PM25",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.DATE.min().date(),
                            max_date_allowed=data.DATE.max().date(),
                            start_date=data.DATE.min().date(),
                            end_date=data.DATE.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("region-filter", "value"),
    ],
)
def update_charts(start_date, end_date,region):

    
    mask = (
        (data.DATE >= start_date)
        & (data.DATE <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["DATE"],
                "y": filtered_data[region], 

                "type": "lines",
                "hovertemplate": "PM25%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "PM25",  # Adjusted the chart title
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return price_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)
