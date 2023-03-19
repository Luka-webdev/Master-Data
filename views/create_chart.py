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
                    dbc.Button("Punktowy",
                               color="primary", id='scatter'),
                ], className='w-75 my-2 p-0'
            ),
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/liniowy.png", top=True),
                    dbc.Button("Liniowy",
                               color="primary", id='line'),
                ], className='w-75 my-2 p-0'
            ),
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/powierzchniowy.png", top=True),
                    dbc.Button("Powierzchniowy",
                               color="primary", id='area'),
                ], className='w-75 my-2 p-0'
            ),
            dbc.Card(
                [
                    dbc.CardImg(
                        src="/assets/images_charts/słupkowy.png", top=True),
                    dbc.Button("Słupkowy",
                               color="primary", id='bar'),
                ], className='w-75 my-2 p-0'
            )
        ], id='type_charts', className='col-2 d-flex flex-column align-items-center'),
        html.Div([
            chart_options(tab_data.columns),
            html.Div([

            ], id='chart')
        ], id='chart_view', className='col-10 h-100')
    ]


# Wybór koloru elementu na wykresie

def item_color(target):
    return html.Div(
        [
            dbc.Label([f"Wybierz kolor {target}", html.Span(
                id="item_color")], className='col-10'),
            dbc.Input(
                type="color",
                id="color_item",
                value="#000000",
                className='col-2'
            ),
        ], className='row px-0'
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
            dcc.Slider(10, 70, 10, id='size', className='px-1')
        ])
    elif type == 'line':
        return html.Div([
            dbc.Label('Ustaw rozmiar linii'),
            dcc.Slider(1, 7, 1, id='size', className='px-1')
        ])
    elif type == 'area':
        return html.Div(id='size')
    elif type == 'bar':
        return html.Div(id='size')

# Wybór koloru tła wykresu


bg_color = html.Div(
    [
        dbc.Label(["Wybierz kolor tła", html.Span(
            id="bg_color")], className='col-10'),
        dbc.Input(
            type="color",
            id="color_bg",
            value="#000000",
            className='col-2'
        ),
    ], className='row'
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
                        ], className='my-1 input_ax'
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Oś Y"),
                            dbc.Select(
                                options=[{'label': item, 'value': item} for item in tabela], id='axis_Y'),
                        ], className='my-1 input_ax'
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Tytuł"),
                            dbc.Input(type='text'),
                        ], className='my-1 input_title'
                    ),
                    html.Div(id='specific_options'),
                    bg_color,
                    dbc.Card([
                        html.P('Opcja dodatkowa', id='tooltip_target', style={
                            'textDecoration': 'underline', 'cursor': 'pointer'}),

                        dbc.Label('Wybierz kategorie', className='m-0'),
                        dbc.Select(
                            options=[{'label': item, 'value': item} for item in tabela], id='category'),

                        dbc.Tooltip(
                            'Jeżeli w twoich danych jest kolumna z kategoriami tzn. zawiera wartości z niewielkiego zbioru to możesz wyróżnić punkty 				 						odpowiadające każdej z nich.', target='tooltip_target'
                        )
                    ], className='choice_category'),
                    dbc.Button(id='insert_chart',
                               className='my-2')
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
    tab_data[aX] = type_recognize(tab_data[aX], tab_data[aX][0])
    tab_data[aY] = type_recognize(tab_data[aY], tab_data[aY][0])
    btn = dash.callback_context.triggered
    if "punktowy" in child:
        fig = px.scatter(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
        fig.update_traces({'marker_size': s})
        if c == None:
            fig.update_traces({'marker_color': ci})
    elif "liniowy" in child:
        fig = px.line(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
        if c == None:
            fig.update_traces(line=dict(width=s, color=ci))
    elif "powierzchniowy" in child:
        fig = px.area(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
        if c == None:
            fig.update_traces(fillcolor=ci)
    elif "słupkowy" in child:
        fig = px.bar(tab_data, x=aX, y=aY, title=t, color=c)
        fig.update_layout({
            'plot_bgcolor': cb,
        })
        if c == None:
            fig.update_traces({'marker_color': ci})
    if btn[0]['prop_id'].split('.')[0] == 'insert_chart':
        return html.Div([
            dcc.Graph(
                        figure=fig
                        )
        ])
