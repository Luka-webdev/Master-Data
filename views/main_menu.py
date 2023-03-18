from main import app
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from views.analysis_selected_column import *
from views.find_rows import *
from views.create_chart import *

offcanvas = html.Div(
    [
        dbc.Button("Opcje analizy", id="open-offcanvas",
                   n_clicks=0, className='position-fixed bottom-0 start-0 btn btn-danger'),
        dbc.Offcanvas(
            html.Div([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Analiza wybranej kolumny",
                                    className="card-title fw-bold m-0"),
                            html.Hr(className='my-1'),
                            html.Div([
                                html.P(
                                    "Wykonaj szczegółową analizę dla wybranej kolumny.",
                                    className="card-text col-10 p-2 m-0",
                                ),
                                dbc.Button(
                                    [html.I(className="bi bi-arrow-right-square-fill text-success")], id='analysis_selected_column', className=' border-0 col-2 bg-transparent p-0'
                                )
                            ], className='row')
                        ]
                    ), className='col-4 p-0 bg-warning bg-gradient menu_card'
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Znajdź wiersze",
                                    className="card-title fw-bold m-0"),
                            html.Hr(className='my-1'),
                            html.Div([
                                html.P(
                                    "Wyszukaj rekordy spełniające określone warunki.",
                                    className="card-text col-10 p-2 m-0",
                                ),
                                dbc.Button(
                                    [html.I(className="bi bi-arrow-right-square-fill text-success")], id='find_rows', className=' border-0 col-2 bg-transparent p-0'
                                )
                            ], className='row')
                        ]
                    ), className='col-3 p-0 bg-warning bg-gradient menu_card'
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Stwórz wykres",
                                    className="card-title fw-bold m-0"),
                            html.Hr(className='my-1'),
                            html.Div([
                                html.P(
                                    "Przedstaw swoje dane w postaci graficznej.",
                                    className="card-text col-10 p-2 m-0",
                                ),
                                dbc.Button(
                                    [html.I(className="bi bi-arrow-right-square-fill text-success")], id='create_chart', className=' border-0 col-2 bg-transparent p-0'
                                )
                            ], className='row')
                        ]
                    ), className='col-3 p-0 bg-warning bg-gradient menu_card'
                ),
            ], className='row px-2 d-flex justify-content-around'),
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
