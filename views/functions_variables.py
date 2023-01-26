from main import app
import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from views.create_new_tab import *

new_values = []
columns_name = []
tab = pd.DataFrame()


def inputs(val1, val2, key):
    if key == 'first':
        return html.Div([dcc.Input(type='text', id=str(col)) for col in range(val1)], id=val2)
    elif key == 'second':
        return html.Div([dcc.Input(type='text', placeholder=columns_name[col], id=str(col)) for col in range(val1)], id=val2)


def add_table():
    return html.Div([
        dash_table.DataTable(
            data=tab.to_dict('records'),
            columns=[{'id': i, "name": i} for i in columns_name],
            style_cell={'font-size': '20px', 'width': '210px'},
            fill_width=False,
            editable=True,
            sort_action='native',
        ),
    ])
