from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.express as px
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
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
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
                                for region in ['CO', 'NO2', 'TEMP', 'RH']
                            ],
                            value="CO",
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
        html.Div( [
        html.H2("กราฟแสดงผลการพยากรณ์ PM 2.5 อีก 1 สัปดาห์ข้างหน้า"),
        dcc.Graph(
            id='pm25-forecast-graph',
            figure={
                'data': [
                    {'x': data.index, 'y': data['PM25'], 'type': 'line', 'name': 'PM 2.5'}
                ],
                'layout': {
                    'title': 'การพยากรณ์ PM 2.5 อีก 1 สัปดาห์ข้างหน้า'
                }
            }
        ),
    ]),
    ]
)


@app.callback(
    [Output("price-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, start_date, end_date):
    mask = (
        (data.columns == region)
        & (data.DATE >= start_date)
        & (data.DATE <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["DATE"],
                "y": filtered_data["PM25"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    
    return price_chart_figure

def update_pm25_graph(selected_date):
    # นำเสนอกราฟ PM2.5 ตามวันที่ที่เลือก
    # ในกรณีที่ใช้ Pycaret สามารถใช้ผลลัพธ์ที่ได้จากการพยากรณ์
    # ดึงข้อมูล PM2.5 จากตัวแปรที่เก็บผลลัพธ์ของ Pycaret มาใช้
    # ตัวอย่าง: pm25_data = pycaret_result.get_data('PM2.5')
    # สร้างกราฟ pm25_data ด้วย Plotly Express
    fig = px.line(x=..., y=..., title='PM 2.5 Forecast')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
