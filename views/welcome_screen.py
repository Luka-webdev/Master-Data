from main import app
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


def make_layout():
    return html.Div([
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([
                html.Section([
                    html.H1(
                        'Master Data', className='col-12 text-center fw-bold h-50 py-3 title'),
                    dbc.Button('Wczytaj dane z tabeli', id='load_data', href='load_data',
                               className='btn col-12 my-3'),
                    dbc.Button('Stwórz nową tabelę', id='new_tab', href='new_tab',
                               className='btn col-12')
                ], className='w-50 h-50'),
            ], id='welcome_screen', className='position-absolute top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center'),
            html.Div(id='wrap-project',
                     className='position-absolute top-0 start-0 w-100')
        ], id='main_wrapper', className='position-relative container-fluid')
    ])


@app.callback(
    Output('wrap-project', 'children'),
    [Input('url', 'pathname')]
)
def start_project(path):
    if path == '/load_data':
        return html.Div([

        ], className='container-fluid w-100 file_data')
    elif path == '/new_tab':
        return html.Div([

        ], className='container-fluid w-100 create_data')
