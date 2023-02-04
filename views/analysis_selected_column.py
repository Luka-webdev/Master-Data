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
    ],id='show_data')

       
@app.callback(
	Output('show_data','children'),
	[Input('source_data','data')]
)
def show(rows):
	tab_data=pd.DataFrame(rows)
	return [
		dbc.InputGroup([
			dbc.InputGroupText('Wybierz kolumnę do analizy'),
			dbc.Select(
			options=[{'label':item,'value':item} for item in tab_data.columns],
			id='selected_columns'),
			dbc.InputGroupText('Wybierz typ wartości w kolumnie'),
			dbc.Select(
			options=[{'label':key,'value':value} for key,value in columns_types.items()],
			id='type_columns'),
			dbc.Button('Rozpocznij analizę',id='start_analyse')	
		]),
		html.Div(id='result_analyse')
	]
	
@app.callback(
	Output('result_analyse','children'),
	[Input('source_data','data')],
	[Input('type_columns','value')],
	[Input('selected_columns','value')],
	[Input('start_analyse','n_clicks')]
)
def show_results(rows,val1,val2,btn):
	tab_data=pd.DataFrame(rows)
	tab_data[val2]=tab_data[val2].astype(val1)
	btn = dash.callback_context.triggered
	if btn[0]['prop_id'].split('.')[0] == 'start_analyse':
		if val1=='int64' or val1=='float64':
			return dbc.Accordion([
       		dbc.AccordionItem([
        			html.P('Najwyższą wartością jest :' + str(tab_data[val2].max()))
        		],title="Wartość maksymalna"),
        		dbc.AccordionItem([
        			html.P('Najniższą wartością jest :' + str(tab_data[val2].min()))
        		],title="Wartość minimalna"),
        		dbc.AccordionItem([
        			html.P('Suma wszystkich wartości wynosi  :' + str(tab_data[val2].sum()))
        		],title="Suma wszystkich wartości"),
				dbc.AccordionItem([
					html.P('Srednia wszystkich wartości wynosi  :' + str(tab_data[val2].mean()))
        		],title="Średnia wszystkich wartości"),
        		dbc.AccordionItem([
        			html.P('Odchylenie standardowe wartości wynosi  :' + str(tab_data[val2].std()))
        		],title="Odchylenie standardowe wartości"),
        		dbc.AccordionItem([
					html.Span(f'{item[0]} - {item[1]} /') for item in tab_data[val2].value_counts().iteritems()
        		],title="Liczebność poszczególnych wartości"),
        	])
        	
		elif val1=='category' or val1=='object':    	
			return dbc.Accordion([
				dbc.AccordionItem([
        			html.Span('Wpisz najpierw tekst'),
        			dbc.Input(type='text',id='tekst'),
        			dbc.Button('Wyszukaj',id='search'),
        			html.P(id='result')
        		],title="Ile wierszy zawiera określony tekst")
        	])
        		
@app.callback(
	Output('result','children'),
	[Input('tekst','value')],
	[Input('search','n_clicks')],
	[Input('selected_columns','value')],
	[Input('source_data','data')]
)
def search_text(val1,btn,val2,rows):
	tab_data=pd.DataFrame(rows)
	btn = dash.callback_context.triggered
	if btn[0]['prop_id'].split('.')[0] == 'search':
		return html.Span(f'Ciąg tekstowy {val1} wystepuje w {tab_data[tab_data[val2].str.contains(val1)].shape[0]}')