from main import app
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from views.analysis_selected_column import *
from views.find_rows import *
from views.create_chart import *

offcanvas = html.Div(
    [
        dbc.Button("Options", id="open-offcanvas",
                   n_clicks=0, className='position-fixed bottom-0 start-0" fs-4'),
        dbc.Offcanvas(
            html.Div([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Analiza wybranej kolumny",
                                    className="card-title"),
                            html.Hr(),
                            html.Div([
                                html.P(
                                    "Wykonaj szczegółową analizę dla wybranej kolumny.",
                                    className="card-text col-9",
                                ),
                                dbc.Button(
                                    "Dalej", id='analysis_selected_column', color="success", className="col-3"
                                )
                            ], className='row')
                        ]
                    ), className='col-3'
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Znajdź wiersze", className="card-title"),
                            html.Hr(),
                            html.Div([
                                html.P(
                                    "Wyszukaj rekordy spełniające określone warunki.",
                                    className="card-text col-9",
                                ),
                                dbc.Button(
                                    "Dalej", id='find_rows', color="success", className="col-3"
                                )
                            ], className='row')
                        ]
                    ), className='col-3'
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Stwórz wykres", className="card-title"),
                            html.Hr(),
                            html.Div([
                                html.P(
                                    "Przedstaw swoje dane w postaci graficznej.",
                                    className="card-text col-9",
                                ),
                                dbc.Button(
                                    "Dalej", id='create_chart', color="success", className="col-3"
                                )
                            ], className='row')
                        ]
                    ), className='col-3'
                ),
            ], className='row px-2'),
            id="offcanvas",
            is_open=False,
            placement='bottom'
        ),
    ], className='main_menu'
)


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


main_menu_content = html.Div([
    offcanvas,
    html.Section([

    ], id='content')
])


@app.callback(
    Output('content', 'children'),
    [Input('analysis_selected_column', 'n_clicks')],
    [Input('find_rows', 'n_clicks')],
    [Input('create_chart', 'n_clicks')]
)
def choice_option(btn1, btn2, btn3):
    btn1 = dash.callback_context.triggered
    btn2 = dash.callback_context.triggered
    btn3 = dash.callback_context.triggered
    if btn1[0]['prop_id'].split(".")[0] == 'analysis_selected_column':
        return analysis_selected_column()
    elif btn2[0]['prop_id'].split(".")[0] == 'find_rows':
        return find_rows()
    elif btn3[0]['prop_id'].split(".")[0] == 'create_chart':
        return create_chart()
