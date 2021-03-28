import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_reusable_components as drc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np


def Header(name, app):
    title = html.H2(name, style={"margin-top": 15})
    logo = html.Img(
        src=app.get_asset_url("logo-large.png"), style={"float": "right", "height": 50, "margin-top": 15}
    )

    return dbc.Row([dbc.Col(title, md=9), dbc.Col(logo, md=3)])


# Start the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


incident_df = pd.read_csv('incidents_final.csv')
crimes_2019_df = pd.read_csv('2019.csv')
crimes_2018_df = pd.read_csv('2018.csv')
crimes_2017_df = pd.read_csv('2017.csv')


def update_figures():
    num_inc_df = pd.read_csv('num_inc.csv')
    dates = list(num_inc_df['Date'])
    datetimes = sorted([datetime.strptime(x, '%m-%d-%Y') for x in dates])
    fig = go.Figure(data=go.Scatter(x=datetimes, y=list(
        num_inc_df['Num']), mode='lines+markers'))
    fig.update_layout(
        title={
            'text': "Daily Incidents",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Dates",
        yaxis_title="Number of Incidents",
        font=dict(
            size=14,
            color="black"))

    return fig


def map_figure(df, hover_data, map_type):

    if map_type == "Emergency Phones":
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_data=hover_data, color_discrete_sequence=[
                                "blue"], zoom=12, height=300, size="Number of Emergency Phones")
    else:
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_data=hover_data,
                                color_discrete_sequence=["red"], zoom=12, height=300)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def donut():
    df = pd.read_csv('incidents_final.csv')

    labels = ['Night', 'Late Night', 'Morning', 'Afternoon']
    times = list(df['Times'])
    freq = {}
    for items in times:
        freq[items] = times.count(items)

    values = list(freq.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(
        title={
            'text': "Time of Incidents",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            size=14,
            color="black"))

    return fig


def histogram():
    freq = {}
    arr = list(incident_df['Nature'])
    for items in arr:
        freq[items] = arr.count(items)

    fig = {
        "data": [
            {
                "type": "bar",
                "x": list(freq.values()),
                "y": list(freq.keys()),
                "marker": {"color": "red"},
                "orientation": "h",
                "selected": {"marker": {"opacity": 1, "color": "red"}},
                "unselected": {"marker": {"opacity": 1, "color": "black"}},
                "showlegend": False,
            },
        ],
        "layout": {
            "barmode": "overlay",
            "selectdirection": "v",
            "clickmode": "event+select",
            "selectionrevision": True,
            "height": 600,
            "margin": {"l": 10, "r": 80, "t": 10, "b": 10},
            "xaxis": {
                "title": {"text": "Count"},
                "automargin": True,
            },
            "yaxis": {
                "type": "category",
                "categoryorder": "array",
                "categoryarray": list(freq.keys()),
                "side": "left",
                "automargin": True,
            },
        },
    }

    return fig


def histogram_crime_location(location, year):
    if year == "2019":
        arr = list(crimes_2019_df[location])
    elif year == "2018":
        arr = list(crimes_2018_df[location])
    else:
        arr = list(crimes_2017_df[location])

    crimes = list(crimes_2019_df['Offense'])

    fig = {
        "data": [
            {
                "type": "bar",
                "x": arr,
                "y": crimes,
                "marker": {"color": "red"},
                "orientation": "h",
                "selected": {"marker": {"opacity": 1, "color": "red"}},
                "unselected": {"marker": {"opacity": 1, "color": "black"}},
                "showlegend": False,
            },
        ],
        "layout": {
            "barmode": "overlay",
            "selectdirection": "v",
            "clickmode": "event+select",
            "selectionrevision": True,
            "height": 600,
            "margin": {"l": 10, "r": 80, "t": 10, "b": 10},
            "xaxis": {
                "title": {"text": "Count"},
                "automargin": True,
            },
            "yaxis": {
                "type": "category",
                "categoryorder": "array",
                "side": "left",
                "automargin": True,
            },
        },
    }

    return fig


# Card components
cards = [
    dbc.Card(
        [
            html.H2(id="number_of_incidents"),
            html.P(id="incident_card_text"),
        ],
        body=True,
        color="dark",
        inverse=True,

    ),
    dbc.Card(
        [
            html.H2(id="number_of_incidents_year"),
            html.P(id="incident_year_card_text"),
        ],
        body=True,
        color="dark",
        inverse=True,

    )
]

# Graph components
graphs = [
    [
        dbc.Card([dcc.RadioItems(
            id="checklist",
            options=[{"label": x, "value": x}
                     for x in ["Incidents", "Emergency Phones"]],
            value="Incidents",
            labelStyle={'display': 'inline-block'}
        )]),
        dcc.Graph(id="map-figure-id"),

    ],
    [
        dcc.Graph(figure=update_figures()),
    ],
    dcc.Graph(figure=donut()),
    dcc.Graph(
        id="current-histogram",
        figure=histogram(),
    ),
    dcc.Graph(
        id="history-histogram",
        figure=histogram_crime_location("On Campus", "2019"),
    ),
]

app.layout = dbc.Container(
    [
        Header("Stay Safe UVA", app),
        html.Hr(),
        html.Br(),
        html.H4("Current Incidents and Emergency Phones"),
        html.Hr(),
        dbc.Row([dbc.Col(cards[0])]),
        html.Br(),
        dbc.Row([dbc.Col(graphs[0])]),
        html.Br(),
        dbc.Row([dbc.Col(graphs[3])]),
        html.Br(),
        html.H4("Statistics for Recent Incidents"),
        html.Hr(),
        dbc.Row([dbc.Col(graphs[1]), dbc.Col(graphs[2])]),
        html.Br(),
        html.H4("Historic Incidents based on Location and Year"),
        html.Hr(),
        dbc.Row([dbc.Col(cards[1])]),
        html.Br(),
        dbc.Row([dbc.Col(drc.CustomDropdown(
            id='dropdown-location',
            options=[
                {'label': 'On Campus',
                    'value': 'On Campus'},
                {'label': 'Non-Grounds/Non-Campus Building or Property',
                    'value': 'Non-Grounds/Non-Campus Building or Property'},
                {'label': 'Public Property', 'value': 'Public Property'},
            ],
            searchable=True,
            value='On Campus',
            placeholder='On Campus'
        ),),
            dbc.Col(drc.CustomDropdown(
                id='dropdown-year',
                options=[
                    {'label': '2019', 'value': '2019'},
                    {'label': '2018', 'value': '2018'},
                    {'label': '2017', 'value': '2017'},
                ],
                searchable=True,
                value='2019',
                placeholder='2019'
            ),)]),
        dbc.Row([dbc.Col(graphs[4])]),
        html.Br(),

    ],
    fluid=False,
)


@app.callback(
    [Output("number_of_incidents", "children"), Output(
        "incident_card_text", "children"), Output("map-figure-id", "figure")],
    [Input("current-histogram", "selectedData"), Input("checklist", "value")]
)
def update_number(selectedData, map_type):
    if selectedData is None and map_type == "Incidents":
        hover_data = ["Nature", "case status", "Date"]
        n_selected = len(incident_df)
        incident_chosen = "Total Number of Incidents in 60 Days"
        fig = map_figure(incident_df, hover_data, "Incidents")

    elif selectedData is not None and map_type == "Incidents":
        hover_data = ["Nature", "case status", "Date"]
        temp_df = incident_df[incident_df['Nature']
                              == selectedData['points'][0]['label']]
        n_selected = len(temp_df)
        incident_chosen = "Number of {}".format(
            selectedData['points'][0]['label']).title()
        fig = map_figure(temp_df, hover_data, "Incidents")

    elif map_type == "Emergency Phones":
        hover_data = ["Name", "Number of Emergency Phones"]
        df = pd.read_csv('blue_light_phones.csv')
        n_selected = df['Number of Emergency Phones'].sum()
        incident_chosen = "Total Number of Emergency Phones on Campus"
        fig = map_figure(df, hover_data, "Emergency Phones")

    return (n_selected,  incident_chosen, fig)


@app.callback(
    [Output("history-histogram", "figure"), Output("incident_year_card_text",
                                                   "children"), Output("number_of_incidents_year", "children")],
    [Input("dropdown-location", "value"), Input("dropdown-year", "value")]
)
def update_location_graph(location, year):
    fig = histogram_crime_location(location, year)
    incident_year_card_text = "Incidents reported for {}".format(year)

    if year == "2019":
        number_of_incidents_year = int(crimes_2019_df['TOTAL'].sum())
    elif year == "2018":
        number_of_incidents_year = int(crimes_2018_df['TOTAL'].sum())
    else:
        number_of_incidents_year = int(crimes_2017_df['TOTAL'].sum())

    return fig, incident_year_card_text, number_of_incidents_year


if __name__ == "__main__":
    app.run_server(debug=True)
