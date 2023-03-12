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
columns_types = {'Liczba całkowita': 'int64', 'Liczba zmiennoprzecinkowa': 'float64',
                 'Kategoria': 'category', 'Tekst': 'object', 'Data': 'datetime64'}
                 
opcje={'zawierającą':'contain','równą':'equal','większą niż':'bigger','większa-równa':'equal_bigger','mniejszą niż':'lower','mniejsza-równa':'lower_equal','wartości zduplikowane':'duplicated','brak wartości':'Nan'}


def inputs(val1, val2, key):
    if key == 'first':
        return html.Div([dcc.Input(type='text', id=str(col)) for col in range(val1)], id=val2)
    elif key == 'second':
        return html.Div([dcc.Input(type='text', placeholder=columns_name[col], id=str(col)) for col in range(val1)], id=val2)


def add_table(tab,idParam):
    return html.Div([
        dash_table.DataTable(
            id=idParam,
            data=tab.to_dict('records'),
            columns=[{'id': i, "name": i} for i in columns_name],
            style_cell={'font-size': '20px', 'width': '210px'},
            fill_width=False,
            editable=True,
            sort_action='native',
        ),
    ])

def type_recognize(axis,first_value):
	if first_value.isalpha():
		axis=axis.astype('category')
		return axis
	else:
		if '.'  in first_value or ',' in first_value:
			axis=axis.apply(lambda x: x.replace(',','.'))
			axis=axis.astype('float64')
			return axis
		else:
			axis=axis.astype('int64')
			return axis
