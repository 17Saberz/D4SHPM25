from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from pycaret.regression import predict_model, load_model
import pandas as pd

data = pd.read_csv("HKT_clean.csv")
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("DATETIMEDATA", inplace=True)

df_mean = pd.read_csv("mean.csv")
df_mean["DATE"] = pd.to_datetime(df_mean["DATE"], format="%Y-%m-%d")
df_mean.sort_values("DATE", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.title = "🫥PM2.5 Forecaster!"

navbar = html.Div(
    className="navbar",  # Added a class name for styling
    children=[
        html.Nav(
            className="nav",
            children=[
                html.A('Analysis', href='/'),
                html.A('PredictionPM25', href='/page-2'),
                html.A('PredictionTEMP', href='/page-3'),
                html.A('GUS', href='/privacy'),
                html.A('Naii', href='/terms')
            ]
        )
    ]
)


template_1 = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🫥", className="header-emoji"),
                html.H1(
                    children="Data", className="header-title"
                ),
                html.H2(
                    children="Analysis", className="header-second"
                ),
                html.P(
                    children=
"Exploring the Impact of Environmental Factors on Air Quality",
                    className="header-description",
                ),
            ],
            className="header-one",
        ),
    ]
)

template_2 = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🫥", className="header-emoji"),
                html.H1(
                    children="PM25 PREDICT GRAPH", className="header-title"
                ),
                html.H2(
                    children="PredictionPM25 ", className="header-second"
                ),
                html.P(
                    children=
"Exploring the Impact of Environmental Factors on Air Quality",
                    className="header-description",
                ),
            ],
            className="header-two",
        ),
    ]
)

template_3 = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🫥", className="header-emoji"),
                html.H1(
                    children="TEMP PREDICT GRAPH", className="header-title"
                ),
                html.H2(
                    children="PredictionTEMP", className="header-second"
                ),
                html.P(
                    children=
"Exploring the Impact of Environmental Factors on Air Quality",
                    className="header-description",
                ),
            ],
            className="header-two",
        ),
    ]
)

layout1 = html.Div(
    children=[
        navbar,
        template_1,
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": col, "value": col}
                                for col in ['PM25', 'CO', 'NO2', 'TEMP', 'RH']
                            ],
                            value="PM25",
                            clearable=False,
                            searchable=False,
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
                            min_date_allowed=data["DATETIMEDATA"].min().date(),
                            max_date_allowed=data["DATETIMEDATA"].max().date(),
                            start_date=data["DATETIMEDATA"].min().date(),
                            end_date=data["DATETIMEDATA"].max().date(),
                            display_format='YYYY-MM-DD',
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
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
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
    Output("volume-chart", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("region-filter", "value"),
    ],
)
def update_charts(start_date, end_date, region):
    mask = ((data["DATETIMEDATA"] >= start_date) 
    & (data["DATETIMEDATA"] <= end_date))
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["DATETIMEDATA"],
                "y": filtered_data[region],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"{region}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Datetime", "fixedrange": True},
            "yaxis": {"title": region, "fixedrange": True},
            "colorway": ["#b8c9b4"],
        },
    }

    mask2 = ((df_mean['DATE'] >= start_date) 
    & (df_mean['DATE'] <= end_date))
    filtered_data2 = df_mean.loc[mask2, :]
    mean_chart_figure = {
        "data": [
            {
                "x": filtered_data2["DATE"],
                "y": filtered_data2[region],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"{region} mean",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "DATE", "fixedrange": True},
            "yaxis": {"title": region, "fixedrange": True},
            "colorway": ['#b8c9b4'],
        },
    }
    return price_chart_figure, mean_chart_figure

layout2 = html.Div(
    children=[
        navbar,
        template_2,
            html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="PM25-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        
    ]
)



@app.callback(
    Output("PM25-chart", "figure"),
    [
        Input('interval-component', 'n_intervals')
    ]
)
def update_chart_PredictionPM25(n_intervals):
    train = pd.read_csv('Train.csv')
    train['DATETIMEDATA'] = pd.to_datetime(train['DATETIMEDATA'])

    loaded_model_PM25 = load_model('PM25_pipeline\PM25_pipeline')

    now = pd.Timestamp.now()
    start_date = now.date()
    end_date = start_date + pd.DateOffset(days=7)

    future_dates_PM25 = pd.date_range(start=start_date, end=end_date, freq='D')
    future_data_PM25 = pd.DataFrame({'DATETIMEDATA': future_dates_PM25})
    future_data_PM25['CO'] = train['CO'].mean().round(2)
    future_data_PM25['NO2'] = train['NO2'].mean().round(2)
    future_data_PM25['TEMP'] = train['TEMP'].mean().round(2)
    future_data_PM25['RH'] = train['PM25'].mean().round(2)

    predictions_PM25 = predict_model(loaded_model_PM25, data=future_data_PM25)
    predictions_PM25 = predictions_PM25.rename(columns={'Label': 'prediction_label'})
    predictions_PM25['prediction_label'] = predictions_PM25['prediction_label'].round(2)


    PM25_chart_figure = {
        "data": [
            {
                "x": future_dates_PM25,
                "y": predictions_PM25['prediction_label'].round(2),
                "type": "lines",
                'name': 'PM25 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': { 
                'text' : f'PM25 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'PM25 Forecast', "fixedrange": True},
            "colorway": ["#B5C0D0"],
        },
    }

    return PM25_chart_figure 

layout3 = html.Div(
    children=[
        navbar,
        template_3,
            html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="TEMP-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    
    Output("TEMP-chart", "figure"),
    [
        Input('interval-component', 'n_intervals')
    ]
)
def update_chart_PredictionPM25TEMP(n_intervals):
    train = pd.read_csv('Train.csv')
    train['DATETIMEDATA'] = pd.to_datetime(train['DATETIMEDATA'])

    loaded_model_TEMP = load_model('TEMP_pipeline')

    now = pd.Timestamp.now()
    start_date = now.date()
    end_date = start_date + pd.DateOffset(days=7)


    future_dates_TEMP = pd.date_range(start=start_date, end=end_date, freq='D')
    future_data_TEMP = pd.DataFrame({'DATETIMEDATA': future_dates_TEMP})
    future_data_TEMP['PM25'] = train['TEMP'].mean().round(2)
    future_data_TEMP['CO'] = train['CO'].mean().round(2)
    future_data_TEMP['NO2'] = train['NO2'].mean().round(2)
    future_data_TEMP['RH'] = train['PM25'].mean().round(2)

    predictions_TEMP = predict_model(loaded_model_TEMP, data=future_data_TEMP)
    predictions_TEMP = predictions_TEMP.rename(columns={'Label': 'prediction_label'})
    predictions_TEMP['prediction_label'] = predictions_TEMP['prediction_label'].round(2)



    TEMP_chart_figure = {
    "data": [
        {
            "x": future_dates_TEMP,
            "y": predictions_TEMP['prediction_label'].round(2),
            "type": "lines",
            'name': 'TEMP Forecast',  # แก้ชื่อที่นี่
            "hovertemplate": "%{y:.2f}<extra></extra>",
        },
    ],
    'layout': {
        'title': { 
            'text' : f'TEMP Forecast for Next 7 Days',
            "x": 0.05,
            "xanchor": "left",
        },
        'xaxis': {'title': 'Date', "fixedrange": True},
        'yaxis': {'title': 'TEMP Forecast', "fixedrange": True},
        "colorway": ["#ccc1b7"],
    },
}

    return TEMP_chart_figure 

privacy_policy_content = """
Privacy Policy Content Goes Here.
"""

terms_of_service_content = """
Terms of Service Content Goes Here.
"""

privacy_policy_layout = html.Div(
    children=[
        navbar,
        html.Div(
            className="content",
            children=[
                html.H1("Privacy Policy"),
                html.Div(privacy_policy_content)
            ]
        ),
        
    ]
)

terms_of_service_layout = html.Div(
    children=[
        navbar,
        html.Div(
            className="content",
            children=[
                html.H1("Terms of Service"),
                html.Div(terms_of_service_content)
            ]
        ),
        
    ]
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Interval(id='interval-component',interval=60000)
    ]
)

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return layout1
    elif pathname == '/page-2':
        return layout2
    elif pathname == '/page-3':
        return layout3
    elif pathname == '/privacy':
        return privacy_policy_layout
    elif pathname == '/terms':
        return terms_of_service_layout
    else:
        return '404 Page Not Found'

if __name__ == "__main__":
    app.run_server(debug=True)
