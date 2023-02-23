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
                               color="primary", className='fs-6', id='scatter'),
                ], className='w-75'
            ),
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/liniowy.png", top=True),
                    dbc.Button("Wykres liniowy",
                               color="primary", className='fs-6', id='line'),
                ], className='w-75'
            ),
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/powierzchniowy.png", top=True),
                    dbc.Button("Wykres powierzchniowy",
                               color="primary", className='fs-6', id='area'),
                ], className='w-75'
            ),
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/słupkowy.png", top=True),
                    dbc.Button("Wykres słupkowy",
                               color="primary", className='fs-6', id='bar'),
                ], className='w-75'
            )
        ], id='type_charts', className='col-2 h-100'),
        html.Div([
            chart_options(tab_data.columns),
            html.Div([

            ], id='chart')
        ], id='chart_view', className='col-10 h-100 bg-info')
    ]


# Wybór koloru elementu na wykresie

def item_color(target):
    return html.Div(
        [
            dbc.Label([f"Wybierz kolor {target}", html.Span(id="item_color")]),
            dbc.Input(
                type="color",
                id="color_item",
                value="#000000",
                style={"width": 75, "height": 50},
            ),
        ]
    )


@app.callback(
    Output("item_color", "style"),
    Input("color_item", "value"),
)
def update_color_item(color):
    return {"color": color}

# Wybór rozmiaru elementu wykresu


def size(type):
    if type == 'scatter':
        return html.Div([
            dbc.Label('Ustaw rozmiar punktów'),
            dcc.Slider(10, 70, 10, id='size')
        ])
    elif type == 'line':
        return html.Div([
            dbc.Label('Ustaw rozmiar linii'),
            dcc.Slider(1, 5, 1, id='size')
        ])
    elif type == 'area':
        return html.Div(id='size')
    elif type == 'bar':
        return html.Div(id='size')

# Wybór koloru tła wykresu


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
                    html.Div(id='specific_options'),
                    bg_color,
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
                    dbc.Button(id='insert_chart')
                ]),
                id="offcanvas-placement",
                is_open=False,
                placement='end'
            ),
        ]
    )

# Zwijanie i rozwijanie menu z opcjami do wykresów


@app.callback(
    [Output("offcanvas-placement", "is_open"),
     Output('specific_options', 'children'),
     Output('insert_chart', 'children')],
    Input("scatter", "n_clicks"),
    Input("line", "n_clicks"),
    Input("area", "n_clicks"),
    Input("bar", "n_clicks"),
    [State("offcanvas-placement", "is_open")],
)
def toggle_offcanvas(n1, n2, n3, n4, is_open):
    n1 = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    n2 = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    n3 = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    n4 = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if n1 == 'scatter':
        return not is_open, [item_color('punktu'), size('scatter')], 'Wstaw wykres punktowy'
    elif n2 == 'line':
        return not is_open, [item_color('linii'), size('line')], 'Wstaw wykres liniowy'
    elif n3 == 'area':
        return not is_open, [item_color('powierzchni'), size('area')], 'Wstaw wykres powierzchniowy'
    elif n4 == 'bar':
        return not is_open, [item_color('słupka'), size('bar')], 'Wstaw wykres słupkowy'
    return is_open


# Wstawianie wykresów


@app.callback(
    Output('chart', 'children'),
    Input('insert_chart', 'n_clicks'),
    Input('insert_chart', 'children'),
    Input('axis_X', 'value'),
    Input('axis_Y', 'value'),
    Input('title', 'value'),
    Input("color_bg", "value"),
    Input("color_item", "value"),
    Input("size", "value"),
    Input("category", "value"),
    Input('source_data', 'data')
)
def insert_charts(btn, child, aX, aY, t, cb, ci, s, c, rows):
    tab_data = pd.DataFrame(rows)
    btn = dash.callback_context.triggered
    if "punktowy" in child:
        fig = px.scatter(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
        fig.update_traces({'marker_size': s})
        if c == None:
            fig.update_traces({'marker_size': s, 'marker_color': ci})
    elif "liniowy" in child:
        fig = px.line(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,

        })
    elif "powierzchniowy" in child:
        fig = px.area(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
    elif "słupkowy" in child:
        fig = px.bar(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
    if btn[0]['prop_id'].split('.')[0] == 'insert_chart':
        return html.Div([
            dcc.Graph(
                        figure=fig
                        )
        ])
