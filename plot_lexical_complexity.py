import pandas as pd
import plotly.express as px
import chart_studio.plotly as py
from credential_file import *
import chart_studio.tools as tls
from datetime import date

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file
results_path = 'results/'

color_map = {
    'meloni':'#000000',
    'salvini':'#17A556',
    'letta':'#E2202B',
    'renzi':'#F3147E',
    'conte':'#F5BE23',
    'calenda':'#002A8D'
}

df = pd.read_csv(results_path+'lexical_richness.csv')
df['L-TTR_percentage'] = (round(df['L-TTR'], 2)*100).astype(int)
df['L-TTR_percentage'] = df['L-TTR_percentage'].astype(str)
df['percentage_symbol'] = '%'
df['L-TTR_percentage'] = df['L-TTR_percentage']+df['percentage_symbol']

fig = px.bar(df, x='L-TTR', y='leader', color='leader', orientation='h', color_discrete_map=color_map, 
text='L-TTR_percentage')
fig.update_yaxes(tickmode = 'array'
                 , tickvals = ['conte', 'letta', 'renzi', 'meloni', 'salvini', 'calenda']
                 , ticktext = ['Conte', 'Letta', 'Renzi', 'Meloni', 'Salvini', 'Calenda']
                 , tickfont=dict(size=16,color='#7F7F7F'))
fig.update_layout(autosize=True
                  , yaxis={'categoryorder':'total ascending'}
                  , plot_bgcolor='white'
                  , xaxis_visible=False
                  , yaxis_title=None
                  , showlegend=False)
fig.write_html('results/lexical_richness_L-TTR.html')
py.plot(fig, filename='lexical_richness_L-TTR', auto_open = False)