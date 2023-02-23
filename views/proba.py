import plotly
import plotly.express as px
import pandas as pd

dane = pd.DataFrame(data={
    'Kat': ['A', 'B', 'C', 'D'],
    'Wynik': [23, 34, 19, 29]
})

fig = px.area(dane, x='Kat', y='Wynik')
fig.show()
