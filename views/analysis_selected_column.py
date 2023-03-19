from main import app
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import pandas as pd
from views.filling_table import tab
from views.create_new_tab import *
from views.functions_variables import *


def analysis_selected_column():
    return html.Section([
    ], id='show_data')


@app.callback(
    Output('show_data', 'children'),
    [Input('source_data', 'data')]
)
def show(rows):
    tab_data = pd.DataFrame(rows)
    return html.Div([
        html.Div([
            html.P('Wybierz kolumnę do analizy',
                   className='text-center text-warning fw-bold'),
            dbc.Select(
                options=[{'label': item, 'value': item}
                         for item in tab_data.columns],
                id='selected_columns', className='my-3'),
            dbc.Button('Rozpocznij analizę',
                       id='start_analyse', className='w-100')
        ], className='col-3 start_analyse p-2'),
        html.Div(id='result_analyse', className='col-9 p-2')
    ], className='row m-0')


@app.callback(
    Output('result_analyse', 'children'),
    [Input('source_data', 'data')],
    [Input('selected_columns', 'value')],
    [Input('start_analyse', 'n_clicks')]
)
def show_results(rows, val2, btn):
    tab_data = pd.DataFrame(rows)
    tab_data[val2] = type_recognize(tab_data[val2], tab_data[val2][0])
    btn = dash.callback_context.triggered
    if btn[0]['prop_id'].split('.')[0] == 'start_analyse':
        if tab_data[val2].dtypes == 'int64' or tab_data[val2].dtypes == 'float64':
            return dbc.Accordion([
                dbc.AccordionItem([
                    html.P('Najwyższą wartością jest :' +
                           str(tab_data[val2].max()))
                ], title="Wartość maksymalna"),
                dbc.AccordionItem([
                    html.P('Najniższą wartością jest :' +
                           str(tab_data[val2].min()))
                ], title="Wartość minimalna"),
                dbc.AccordionItem([
                    html.P('Suma wszystkich wartości wynosi  :' +
                           str(tab_data[val2].sum()))
                ], title="Suma wszystkich wartości"),
                dbc.AccordionItem([
                    html.P('Srednia wszystkich wartości wynosi  :' +
                           str(tab_data[val2].mean()))
                ], title="Średnia wszystkich wartości"),
                dbc.AccordionItem([
                    html.P('Odchylenie standardowe wartości wynosi  :' +
                           str(tab_data[val2].std()))
                ], title="Odchylenie standardowe wartości"),
                dbc.AccordionItem([
                    html.Span(f'{item[0]} - {item[1]} /') for item in tab_data[val2].value_counts().iteritems()
                ], title="Liczebność poszczególnych wartości"),
            ])
        elif tab_data[val2].dtypes == 'object' or tab_data[val2].dtypes == 'category':
            return dbc.Accordion([
                dbc.AccordionItem([
                    dbc.InputGroup([
                        html.Span('Wpisz najpierw tekst'),
                        dbc.Input(type='text', id='txt', className='p-1 mx-1'),
                    ], className='w-50'),
                    dbc.Switch(
                        id='txt_toggle', label="Wyszukaj wiersze, które nie zawierają podanego tekstu.", value=False),

                    dbc.Button('Wyszukaj', id='search_txt',
                               className='bg-warning text-primary'),
                    html.P(id='result_txt')
                ], title="Ile wierszy zawiera określony tekst?"),
                dbc.AccordionItem([
                    dbc.InputGroup([
                        html.Span('Wpisz długość tekstu'),
                        dbc.Input(type='number', id='len',
                                  className='p-1 mx-1'),
                    ], className='w-50'),
                    dbc.Switch(
                        id='len_toggle', label="Wyszukaj wiersze, które zawierają tekst o długości innej niż podana.", value=False),

                    dbc.Button('Wyszukaj', id='search_len',
                               className='bg-warning text-primary'),
                    html.P(id='result_len')
                ], title="Ile wierszy zawiera tekst o podanej długości?"),
                dbc.AccordionItem([
                    html.Span('Wybierz wzorzec', id='tooltip', style={
                        "textDecoration": 'underline', 'cursor': 'pointer'}),
                    dbc.Tooltip(
                        'Za pomocą wzorca możesz wyszukiwać w kolumnie tekstowej np. kody pocztowe, numery telefonów itp.', target='tooltip'),
                    dbc.RadioItems(
                        options=[
                            {'label': 'Wyszukaj wiersze zawierające liczby o wskazanej ilości cyfr', 'value': 1},
                            {'label': 'Wyszukaj wiersze zawierające liczby o wskazanym układzie cyfr', 'value': 2},
                            {'label': 'Wyszukaj wiersze zaczynające się od określonego znaku lub słowa', 'value': 3},
                            {'label': 'Wyszukaj wiersze kończące się określonym znakiem lub słowem', 'value': 4},
                        ], id='pattern_option'
                    ),
                    dbc.Input(
                        placeholder='Tu wpisz wzorzec zgody z wybraną opcją', type='text', id='pattern', className='w-50'),
                    dbc.FormText(
                        'Układy cyfry należy wpisywać używając litery "d" np. dd-ddd'),
                    dbc.Switch(
                        id='pattern_toggle', label="Wyszukaj wiersze, które zawierają tekst niedopasowany do podanego wzorca.", value=False),
                    dbc.Button('Wyszukaj', id='search_pattern',
                               className='bg-warning text-primary'),
                    html.P(id='result_pattern')
                ], title="Ile wierszy zawiera tekst dopasowany do wskazanego wzorca?"),
            ])

# Szukanie wierszy zawierających określony tekst


@app.callback(
    Output('result_txt', 'children'),
    [Input('txt', 'value')],
    [Input('search_txt', 'n_clicks')],
    [Input('selected_columns', 'value')],
    [Input('txt_toggle', 'value')],
    [Input('source_data', 'data')]
)
def search_text(val1, btn, val2, val3, rows):
    tab_data = pd.DataFrame(rows)
    btn = dash.callback_context.triggered
    results_pos = tab_data[tab_data[val2].str.contains(val1)].shape[0]
    results_neg = tab_data[~tab_data[val2].str.contains(val1)].shape[0]
    if btn[0]['prop_id'].split('.')[0] == 'search_txt':
        if val3 == False:
            if results_pos == 0:
                return html.Span('Podany ciąg tekstowy nie występuje we wskazanej tabeli')
            else:
                return html.Span(f'Ciąg tekstowy {val1} wystepuje {results_pos} razy.')
        else:
            return html.Span(f'Ciąg tekstowy {val1} nie wystepuje w {results_neg} wierszach.')

# Szukanie wierszy zawierających tekst o określonej długości


@app.callback(
    Output('result_len', 'children'),
    [Input('len', 'value')],
    [Input('search_len', 'n_clicks')],
    [Input('selected_columns', 'value')],
    [Input('len_toggle', 'value')],
    [Input('source_data', 'data')]
)
def search_length(val1, btn, val2, val3, rows):
    tab_data = pd.DataFrame(rows)
    results_pos = tab_data[tab_data[val2].apply(
        lambda x: len(x) == val1)].shape[0]
    results_neg = tab_data[~tab_data[val2].apply(
        lambda x: len(x) == val1)].shape[0]
    btn = dash.callback_context.triggered
    if btn[0]['prop_id'].split('.')[0] == 'search_len':
        if val3 == False:
            if results_pos == 0:
                return html.Span('We wskazanej kolumnie nie ma tekstów o podanej długości.')
            else:
                return html.Span(f'Tekst o długości {val1} wystepuje {results_pos} razy')
        else:
            return html.Span(f'Tekst o długości {val1} nie wystepuje {results_neg} razy')

# Szukanie wierszy dopasowanych do wzorca


@app.callback(
    Output('result_pattern', 'children'),
    [Input('pattern_option', 'value')],
    [Input('pattern', 'value')],
    [Input('pattern_toggle', 'value')],
    [Input('selected_columns', 'value')],
    [Input('search_pattern', 'n_clicks')],
    [Input('source_data', 'data')]
)
def search_pattern(val1, val2, val3, val4, btn, rows):
    tab_data = pd.DataFrame(rows)
    btn = dash.callback_context.triggered
    if btn[0]['prop_id'].split('.')[0] == 'search_pattern':
        if val1 == 1:
            results_pos = tab_data[tab_data[val4].str.contains(
                pat='\\b\\w{'+val2+'}\\b', regex=True)].count()[val4]
            results_neg = tab_data[~tab_data[val4].str.contains(
                pat='\\b\\w{'+val2+'}\\b', regex=True)].count()[val4]
            if val3 == False:
                if results_pos == 0:
                    return html.Span('We wskazanej kolumnie nie ma wierszy zawierających liczby o podanej ilości cyfr.')
                else:
                    return html.Span(f'W kolumnie {val4} jest {results_pos} wierszy zawierających liczby {val2} cyfrowe.')
            else:
                return html.Span(f'W kolumnie {val4} jest {results_neg} wierszy nie zawierających liczb {val2} cyfrowych.')
        elif val1 == 2:
            val2 = val2.replace('d', '\d')
            results_pos = tab_data[tab_data[val4].str.contains(
                pat='( |\w)*'+val2+'( |\w)*', regex=True)].count()[val4]
            results_neg = tab_data[~tab_data[val4].str.contains(
                pat='( |\w)*'+val2+'( |\w)*', regex=True)].count()[val4]
            if val3 == False:
                if results_pos == 0:
                    return html.Span('We wskazanej kolumnie nie ma wierszy zawierających ciągów liczb o podanym układzie.')
                else:
                    return html.Span(f'W kolumnie {val4} jest {results_pos} wierszy zawierających ciagi liczb o podanym układzie.')
            else:
                return html.Span(f'W kolumnie {val4} jest {results_neg} wierszy, które nie zawierają ciągów liczb o podanym układzie.')
        elif val1 == 3:
            results_pos = tab_data[tab_data[val4].str.contains(
                pat='^'+val2, regex=True)].count()[val4]
            results_neg = tab_data[~tab_data[val4].str.contains(
                pat='^'+val2, regex=True)].count()[val4]
            if val3 == False:
                if results_pos == 0:
                    return html.Span('We wskazanej kolumnie nie ma wierszy rozpoczynających się od podanego wzorca.')
                else:
                    return html.Span(f'W kolumnie {val4} jest {results_pos} wierszy rozpoczynających się podanym wzorcem.')
            else:
                return html.Span(f'W kolumnie {val4} jest {results_neg} wierszy, które nie rozpocznają się podanym wzorcem.')
        elif val1 == 4:
            results_pos = tab_data[tab_data[val4].str.contains(
                pat=val2+'$', regex=True)].count()[val4]
            results_neg = tab_data[~tab_data[val4].str.contains(
                pat=val2+'$', regex=True)].count()[val4]
            if val3 == False:
                if results_pos == 0:
                    return html.Span('We wskazanej kolumnie nie ma wierszy kończących się podanym wzorcem.')
                else:
                    return html.Span(f'W kolumnie {val4} jest {results_pos} wierszy kończących się podanym wzorcem.')
            else:
                return html.Span(f'W kolumnie {val4} jest {results_neg} wierszy, które nie kończą się podanym wzorcem.')
