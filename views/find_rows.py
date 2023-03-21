from main import app
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, dash_table
import pandas as pd
from views.functions_variables import *


def find_rows():
    return html.Section([
    ], id='part_table')


@app.callback(
    Output('part_table', 'children'),
    [Input('source_data', 'data')]
)
def show_table(rows):
    tab_data = pd.DataFrame(rows)
    return html.Section([
        html.Div([

            html.P("Pokaż wiersze, które w kolumnie",
                   className='text-center text-warning fw-bold my-2'),
            dbc.Select(
                options=[{'label': item, 'value': item}
                         for item in tab_data.columns],
                id='selected_columns'),
            html.P('mają wartość', className='text-center text-warning fw-bold'),
            dbc.Select(
                options=[{'label': key, 'value': value}
                         for key, value in opcje.items()],
                id='selected_option', className='my-2'),
            dbc.Input(
                type='text', id='target', className='my-2'),
            dbc.Button('Pokaż wyniki', color='success',
                       id='show_rows', className='my-2'),
        ], className='col-3 indication_rows'),
        html.Div(id='found_rows', className='col-9 py-2')
    ], className='row mx-0')


@app.callback(
    Output('found_rows', 'children'),
    [Input('show_rows', 'n_clicks')],
    [Input('selected_columns', 'value')],
    [Input('selected_option', 'value')],
    [Input('target', 'value')],
    [Input('source_data', 'data')]
)
def show_found_rows(btn, sc, so, t, rows):
    tab_data = pd.DataFrame(rows)
    btn = dash.callback_context.triggered
    if btn[0]['prop_id'].split('.')[0] == 'show_rows':
        if so == 'contain':
            result = tab_data[tab_data[sc].str.contains(t)]
            return add_table(result, 'filtered_data')
        elif so == 'equal':
            result = tab_data[tab_data[sc] == t]
            return add_table(result, 'filtered_data')
        elif so == 'bigger':
            result = tab_data[tab_data[sc] > t]
            return add_table(result, 'filtered_data')
        elif so == 'equal_bigger':
            result = tab_data[tab_data[sc] >= t]
            return add_table(result, 'filtered_data')
        elif so == 'lower':
            result = tab_data[tab_data[sc] < t]
            return add_table(result, 'filtered_data')
        elif so == 'lower_equal':
            result = tab_data[tab_data[sc] <= t]
            return add_table(result, 'filtered_data')
        elif so == 'Nan':
            result = tab_data[tab_data[sc].isnull()]
            return add_table(result, 'filtered_data')
        elif so == 'duplicated':
            result = tab_data[tab_data[sc].duplicated()]
            return add_table(result, 'filtered_data')
