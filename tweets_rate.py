import pandas as pd
import plotly.express as px
import chart_studio.plotly as py
from credential_file import *
import chart_studio.tools as tls
from datetime import date

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file
data_path = 'data/'

def get_days_number(start_date, end_date):
    d0 = start_date
    d1 = end_date
    return (d1 - d0).days

total_days = get_days_number(start_date = date(2018, 3, 23), end_date=date(2022, 8, 30))

color_map = {
    'meloni':'#000000',
    'salvini':'#17A556',
    'letta':'#E2202B',
    'renzi':'#F3147E',
    'conte':'#F5BE23',
    'calenda':'#002A8D'
}

meloni = pd.read_csv(data_path+'tweets_meloni.csv')
salvini = pd.read_csv(data_path+'tweets_salvini.csv')
letta = pd.read_csv(data_path+'tweets_letta.csv')
renzi = pd.read_csv(data_path+'tweets_renzi.csv')
conte = pd.read_csv(data_path+'tweets_conte.csv')
calenda = pd.read_csv(data_path+'tweets_calenda.csv')

df = pd.DataFrame({'leader':['meloni', 'salvini', 'letta', 'renzi', 'conte', 'calenda']})
df['tweet_rate'] = [len(meloni.index), len(salvini.index), len(letta.index), len(renzi.index), len(conte.index), len(calenda.index)]
df['tweet_rate_daily'] = df['tweet_rate']/total_days
df['tweet_rate_daily_percentage'] = round(df['tweet_rate_daily'], 1)
df['tweet_rate_daily_percentage'] = df['tweet_rate_daily_percentage'].astype(str)

fig = px.bar(df, x='tweet_rate_daily', y='leader', color='leader', orientation='h', color_discrete_map=color_map, title='<b>Average number of tweets per day</b>',
text='tweet_rate_daily_percentage')
fig.update_yaxes(tickmode = 'array'
                 , tickvals = ['conte', 'letta', 'renzi', 'meloni', 'salvini', 'calenda']
                 , ticktext = ['Conte', 'Letta', 'Renzi', 'Meloni', 'Salvini', 'Calenda']
                 , tickfont=dict(size=16,color='#7F7F7F'))
fig.update_layout(autosize=True
                  , yaxis={'categoryorder':'total ascending'}
                  , plot_bgcolor='white'
                  , xaxis_visible=False
                  , yaxis_title=None
                  , showlegend=False
                  , title={
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'}
                  , title_font_color='#7F7F7F'
                  , title_font_size=20)
fig.write_html('results/tweet_rate_daily.html')
py.plot(fig, filename='tweet_rate_daily', auto_open = False)