from main import app
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.express as px
from views.functions_variables import *

# Zawartość strony do wstawiania wykresów


def create_chart():
    return html.Section([
    ], id='charts_wrapper', className='row charts_wrapper')


@app.callback(
    Output('charts_wrapper', 'children'),
    [Input('source_data', 'data')]
)
def show(rows):
    tab_data = pd.DataFrame(rows)
    return [
        html.Div([
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/punktowy.png", top=True),
                    dbc.Button("Wykres punktowy",
                               color="primary", className='fs-6', id='open-offcanvas-placement'),
                ], className='w-75'
            )
        ], id='type_charts', className='col-2 h-100'),
        html.Div([
            chart_options(tab_data.columns),
            html.Div([

            ], id='chart')
        ], id='chart_view', className='col-10 h-100 bg-info')
    ]

# Wybór koloru punktu na wykresie


marker_color = html.Div(
    [
        dbc.Label(["Wybierz kolor punktu", html.Span(id="marker_color")]),
        dbc.Input(
            type="color",
            id="color_marker",
            value="#000000",
            style={"width": 75, "height": 50},
        ),
    ]
)


@app.callback(
    Output("marker_color", "style"),
    Input("color_marker", "value"),
)
def update_color_marker(color):
    return {"color": color}

# Wybór rozmiaru punktu


def marker_size():
    return html.Div([
        dbc.Label('Ustaw rozmiar punktów'),
        dcc.Slider(10, 70, 10, id='size_marker')
    ])

# Wybór kolou tła wykresu


bg_color = html.Div(
    [
        dbc.Label(["Wybierz kolor tła", html.Span(id="bg_color")]),
        dbc.Input(
            type="color",
            id="color_bg",
            value="#000000",
            style={"width": 75, "height": 50},
        ),
    ]
)


@app.callback(
    Output("bg_color", "style"),
    Input("color_bg", "value"),
)
def update_color_bg(color):
    return {"color": color}

# Zawartość rozwijanego menu zawierającego opcje do wykresów


def chart_options(tabela):
    return html.Div(
        [
            dbc.Offcanvas(
                html.Div([
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Oś X"),
                            dbc.Select(
                                options=[{'label': item, 'value': item} for item in tabela], id='axis_X'),
                        ]
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Oś Y"),
                            dbc.Select(
                                options=[{'label': item, 'value': item} for item in tabela], id='axis_Y'),
                        ]
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Tytuł"),
                            dbc.Input(type='text', id='title'),
                        ]
                    ),
                    bg_color,
                    marker_color,
                    marker_size(),
                    dbc.Card([
                        html.P('Opcja dodatkowa', id='tooltip_target', style={
                            'textDecoration': 'underline', 'cursor': 'pointer'}),
                        dbc.InputGroup([
                            dbc.InputGroupText('Wybierz kategorie'),
                            dbc.Select(
                                options=[{'label': item, 'value': item} for item in tabela], id='category'),
                        ]),
                        dbc.Tooltip(
                            'Jeżeli w twoich danych jest kolumna z kategoriami tzn. zawiera wartości z niewielkiego zbioru to możesz wyróżnić punkty 				 						odpowiadające każdej z nich.', target='tooltip_target'
                        )
                    ]),
                    dbc.Button('Insert chart', id='insert_chart')
                ]),
                id="offcanvas-placement",
                is_open=False,
                placement='end'
            ),
        ]
    )

# Zwijanie i rozwijanie menu z opcjami do wykresów


@app.callback(
    Output("offcanvas-placement", "is_open"),
    Input("open-offcanvas-placement", "n_clicks"),
    [State("offcanvas-placement", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Wstawianie wykresów


@app.callback(
    Output('chart', 'children'),
    Input('insert_chart', 'n_clicks'),
    Input('axis_X', 'value'),
    Input('axis_Y', 'value'),
    Input('title', 'value'),
    Input("color_bg", "value"),
    Input("color_marker", "value"),
    Input("size_marker", "value"),
    Input("category", "value"),
    Input('source_data', 'data')
)
def insert_charts(btn, val1, val2, val3, val4, val5, val6, val7, rows):
    tab_data = pd.DataFrame(rows)
    btn = dash.callback_context.triggered
    fig = px.scatter(tab_data, x=val1, y=val2, title=val3, color=val7)
    fig.update_layout({
        'plot_bgcolor': val4,
    })
    fig.update_traces({'marker_size': val6})
    if val7 == None:
        fig.update_traces({'marker_size': val6, 'marker_color': val5})
    if btn[0]['prop_id'].split('.')[0] == 'insert_chart':
        return html.Div([
            dcc.Graph(
                figure=fig
            )
        ])
