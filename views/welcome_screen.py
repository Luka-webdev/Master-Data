from main import app
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from views.create_new_tab import *
from views.main_menu import *

app.config.suppress_callback_exceptions = True


def make_layout():
    return html.Div([
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([
                html.Section([
                    html.H1(
                        'Master Data', className='col-12 text-center fw-bold h-50 py-2 title'),
                    dbc.Col(
                        html.Div(
                            [
                                html.H2("Wczytaj dane",
                                        className="display-5 fw-bold"),
                                html.Hr(className="my-2"),
                                html.Div([
                                    html.P(
                                        "Wczytaj dane z pliku zewnętrznego i przeprowadź ich analizę.", className='col-9'
                                    ),
                                    dbc.Button("Dalej", id='load_data', href='load_data',
                                               color="light", outline=True, className='col-3 h-50'),
                                ], className='row'),

                            ],
                            className="h-100  p-3 text-white rounded-3 welcome_option_1",
                        ),

                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H2("Stwórz tabelę",
                                        className="display-5 fw-bold"),
                                html.Hr(className="my-2"),
                                html.Div([
                                    html.P(
                                        "Utwórz tabelę od zera, wprawdzaj dane i je analizuj.", className='col-9'
                                    ),
                                    dbc.Button("Dalej", id='new_tab', href='new_tab',
                                               color="light", outline=True, className='col-3 h-50'),
                                ], className='row')
                            ],
                            className="h-100  p-3 text-white rounded-3 welcome_option_2",
                        ),
                    ),
                ], className='w-75 h-50 row'),
            ], id='welcome_screen', className='position-absolute top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center'),
            html.Div(id='wrap_project',
                     className='position-absolute top-0 start-0 w-100'),
        ], id='main_wrapper', className='position-relative container-fluid')
    ])


@app.callback(
    Output('wrap_project', 'children'),
    [Input('url', 'pathname')]
)
def start_project(path):
    if path == '/load_data':
        return html.Div([

        ], className='container-fluid w-100 file_data')
    elif path == '/new_tab':
        return dcc.Tabs([
            dcc.Tab(
                        label='Wprowadzanie danych',
                        children=[
                            html.Div([
                                html.Section([
                                    new_tab()
                                ], id='insert_data', className="col-3 bg-dark h-100 p-3"),
                                html.Section([
                                    html.Div(id='table_header'),
                                    html.Div(id='table_content'),
                                ], id='result_area', className='col-9 bg-info h-100 p-3')
                            ], className='row mx-0 create_data')
                        ]
                        ),
            dcc.Tab(
                label='Analiza danych',
                children=[
                    html.Div([
                        main_menu_content
                    ], id='data_analysis')
                ]
            )
        ])
