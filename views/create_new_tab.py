from main import app
import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from views.main_menu import *
from views.functions_variables import *
from views.filling_table import *


def new_tab():
    return html.Div([
        html.Section([
                    html.Div([
                        dbc.InputGroupText(
                            'Liczba kolumn w tabeli', className='col-lg-9 col-12 label'),
                        dcc.Input(type='number', id='num_cols', className='col-lg-3 col-12')], className='row'),
                     dbc.Button('Utwórz pola do wpisania nazw kolumn', id='create_headers',
                                className='btn btn-success my-2'),
                     ], id='insert_cols'),
        html.Section(id='name_cols',
                     className='my-2'),
        html.Section(id='add_rows'),
    ])


@app.callback(
    Output('name_cols', 'children'),
    [Input('num_cols', 'value')],
    [Input('create_headers', 'n_clicks')]
)
def create_columns(value, btn):
    if value != None:
        btn = dash.callback_context.triggered
        if btn[0]['prop_id'].split('.')[0] == 'create_headers':
            return html.Div([
                inputs(value, 'input_wrap', 'first'),
                html.Button('Utwórz tabelę', id='create_tab',
                            className='btn btn-warning my-2'),
            ])


@app.callback(
    [Output('table_header', 'children'),
     Output('insert_cols', 'style'),
     Output('name_cols', 'style'),
     Output('add_rows', 'children')],
    [Input('create_tab', 'n_clicks')],
    [Input('input_wrap', 'children')],

)
def create_table(btn, children):
    btn = dash.callback_context.triggered
    if btn[0]['prop_id'].split('.')[0] == 'create_tab':
        for child in children:
            columns_name.append(child['props']['value'])
        return [
            add_table(tab, 'source_data'),
            {'display': 'none'},
            {'display': 'none'},
            filling_data()
        ]
