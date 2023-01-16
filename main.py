import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

app = Dash(__name__)

app.layout = html.Div([

])

if __name__ == '__main__':
    app.run_server(debug=True)
