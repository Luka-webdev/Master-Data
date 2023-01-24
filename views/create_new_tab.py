from main import app
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from views.menu import *

columns_name = []
tab = pd.DataFrame()
new_values = []


def inputs(val1, val2, key):
    if key == 'first':
        return html.Div([dcc.Input(type='text', id=str(col), style={'font-size': '20px', 'width': '200px', 'padding': '3px'}) for col in range(val1)], id=val2)
    elif key == 'second':
        return html.Div([dcc.Input(type='text', placeholder=columns_name[col], id=str(col), style={'font-size': '20px', 'width': '200px', 'padding': '3px'}) for col in range(val1)], id=val2)


def new_tab():
    return html.Div([
        html.Section([
                    dbc.InputGroup([dbc.InputGroupText('Ile kolumn ma mieć tabela'),
                                    dcc.Input(type='number', id='num_cols', style={
                                              'width': '50px', 'font-size': '20px', 'padding': '10px'}),
                                    ], size='lg'),
                     dbc.Button('Utwórz pola do wpisania nazw kolumn', id='create_headers',
                                className='btn btn-success', style={'font-size': '20px'}),
                     ], id='insert_cols', style={'margin': '20px'}),
        html.Section(id='name_cols'),
        html.Section(id='add_rows'),
        offcanvas
    ])


@app.callback(
    Output('name_cols', 'children'),
    [Input('num_cols', 'value'),
     Input('create_headers', 'n_clicks')]
)
def create_columns(value, btn):
    if value != None:
        btn = dash.callback_context.triggered
        if btn[0]['prop_id'].split('.')[0] == 'create_headers':
            return html.Div([
                inputs(value, 'input_wrap', 'first'),
                html.Button('Utwórz tabelę', id='create_tab', style={
                            'font-size': '20px', 'margin-top': '10px'}),
            ])
