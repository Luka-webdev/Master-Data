from main import app
import dash
from dash.dependencies import Input, Output
import pandas as pd
from views.main_menu import *
from views.filling_table import *
from views.create_new_tab import *
from views.functions_variables import *


def filling_data():
    return html.Div([
        html.H3('Wprowadź dane do tabeli', className='text-primary'),
        inputs(len(columns_name), "new_data", "second"),
        html.Button('Zatwierdź', id='add_data', className='btn btn-info my-2')
    ])


@app.callback(
    [Output('table_content', 'children')],
    [Output('table_header', 'style')],
    [Output(item, 'value') for item in columns_name],
    [Input('add_data', 'n_clicks')],
    [Input('new_data', 'children')]
)
def update_table(btn, children):
    btn = dash.callback_context.triggered
    if btn[0]['prop_id'].split('.')[0] == 'add_data':
        data = {}
        for child in children:
            new_values.append(child['props']['value'])
        for col_name, col_value in zip(columns_name, new_values):
            data.update({
                col_name: col_value
            })
        global tab
        tab = tab.append(data, ignore_index=True)
        new_values.clear()
        return [
            add_table(tab, 'source_data'),
            {'display': 'none'},
        ]
