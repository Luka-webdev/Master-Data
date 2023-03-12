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
                    dbc.InputGroup([dbc.InputGroupText('Ile kolumn ma mieć tabela'),
                                    dcc.Input(type='number', id='num_cols', style={
                                              'width': '50px', 'font-size': '20px', 'padding': '10px'}),
                                    ], size='lg'),
                     dbc.Button('Utwórz pola do wpisania nazw kolumn', id='create_headers',
                                className='btn btn-success', style={'font-size': '20px'}),
                     ], id='insert_cols', style={'margin': '20px'}),
        html.Section(id='name_cols'),
        html.Section(id='add_rows'),
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
                html.Button('Utwórz tabelę', id='create_tab'),
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
            add_table(tab,'source_data'),
            {'display': 'none'},
            {'display': 'none'},
            filling_data()
        ]
