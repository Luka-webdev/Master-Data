from main import app
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

offcanvas = html.Div(
    [
        dbc.Button("Options", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            html.Div([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Analiza tabeli", className="card-title"),
                            html.Hr(),
                            html.Div([
                                html.P(
                                    "Poznaj podstawowe informacje o swojej tabeli.",
                                    className="card-text col-9",
                                ),
                                dbc.Button(
                                    "Dalej", color="success", className="col-3"
                                ),
                            ], className='row')
                        ]
                    ), className='col-3'
                ),
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
                                    "Dalej", color="success", className="col-3"
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
                                    "Dalej", color="success", className="col-3"
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
                                    "Dalej", color="success", className="col-3"
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
