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
                        dbc.InputGroup([
                            dbc.InputGroupText(
                                "Pokaż wiersze, które w kolumnie"),
                            dbc.Select(
                                options=[{'label': item, 'value': item}
                                         for item in tab_data.columns],
                                id='selected_columns'),
                        ]),
                        dbc.InputGroupText('mają wartość'),
                        dbc.Select(
                            options=[{'label': key, 'value': value}
                                     for key, value in opcje.items()],
                            id='selected_option'),
                        dbc.Input(
                            type='text', id='target', placeholder='Wypełnij w przypadku wyboru opcji większa, równa, mniejsza'),
                        dbc.Button('Pokaż', color='success', id='show_rows'),
                        ], className='col-12'),
        html.Div(id='found_rows', className='col-12')
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
