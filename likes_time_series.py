import time
from matplotlib import markers
import pandas as pd
import plotly.express as px
import chart_studio.plotly as py
from credential_file import *
import chart_studio.tools as tls

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file
data_path = 'data/'
time_period = 'monthly'

color_map = {
    'Meloni':'#000000',
    'Salvini':'#17A556',
    'Letta':'#E2202B',
    'Renzi':'#F3147E',
    'Conte':'#F5BE23',
    'Calenda':'#002A8D'
}

meloni = pd.read_csv(data_path+'tweets_meloni.csv')
salvini = pd.read_csv(data_path+'tweets_salvini.csv')
letta = pd.read_csv(data_path+'tweets_letta.csv')
renzi = pd.read_csv(data_path+'tweets_renzi.csv')
conte = pd.read_csv(data_path+'tweets_conte.csv')
calenda = pd.read_csv(data_path+'tweets_calenda.csv')

def get_likes_count(df, time_period):
    if time_period=='daily':
        df['datetime'] = pd.to_datetime(df.datetime).dt.date
    elif time_period=='weekly':
        #TODO
        df['datetime'] = pd.to_datetime(df.datetime).dt.strftime('%Y-%m')
    elif time_period=='monthly':
        df['datetime'] = pd.to_datetime(df.datetime).dt.strftime('%Y-%m')
    else:
        df['datetime'] = pd.to_datetime(df.datetime)
    df = df[['id', 'datetime', 'like_count']]
    df = df.groupby('datetime').agg({'id':'count', 'like_count':'sum'}).reset_index().rename(columns={'id':'tweet_count'})
    df['likes_norm'] = df['like_count']/df['tweet_count']
    return df

def get_likes_time_series_plot(df_likes):
    fig = px.scatter(df_likes, x='datetime', y='like_count', size='tweet_count')
    return fig

meloni_likes  = get_likes_count(meloni, time_period)
salvini_likes = get_likes_count(salvini, time_period)
letta_likes   = get_likes_count(letta, time_period)
renzi_likes   = get_likes_count(renzi, time_period)
conte_likes   = get_likes_count(conte, time_period)
calenda_likes   = get_likes_count(calenda, time_period)

meloni_likes['leader'] = 'Meloni'
salvini_likes['leader'] = 'Salvini'
letta_likes['leader'] = 'Letta'
renzi_likes['leader'] = 'Renzi'
conte_likes['leader'] = 'Conte'
calenda_likes['leader'] = 'Calenda'

mel_sal = pd.concat([meloni_likes, salvini_likes], ignore_index=True)
mel_sal_let = pd.concat([mel_sal, letta_likes], ignore_index=True)
mel_sal_let_ren = pd.concat([mel_sal_let, renzi_likes], ignore_index=True)
mel_sal_let_ren_cal = pd.concat([mel_sal_let_ren, calenda_likes], ignore_index=True)
total_likes = pd.concat([mel_sal_let_ren_cal, conte_likes], ignore_index=True)

fig = px.scatter(total_likes, x='datetime', y='like_count', size='tweet_count', color='leader', color_discrete_map=color_map, facet_col='leader', facet_col_wrap=3, title = 'Aggregated number of likes for each month of legislature', labels = {'datetime': '', 'like_count': '', "leader": "Leader"})
fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16,color='#7F7F7F'))
fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16,color='#7F7F7F'))
fig.update_layout(autosize=True
                  , plot_bgcolor='white'
                  , yaxis_title=None
                  , xaxis_title=None
                  , title={
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'}
                  , title_font_color='#7F7F7F')
fig.update_traces(marker={'opacity':0.8, 'line':{'width':0}})
fig.write_html('results/'+time_period+'_likes.html')
py.plot(fig, filename=time_period+'_likes', auto_open = False)

fig_norm = px.scatter(total_likes, x='datetime', y='likes_norm', color='leader', color_discrete_map=color_map, facet_col='leader', facet_col_wrap=3, title = 'Number of likes per month and per tweet', labels = {'datetime': '', 'likes_norm': '', "leader": "Leader"})
fig_norm.update_yaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16,color='#7F7F7F'))
fig_norm.update_xaxes(showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot',tickfont=dict(size=16,color='#7F7F7F'))
fig_norm.update_traces(marker={'size': 15, 'opacity':0.8, 'line':{'width':0}})
fig_norm.update_layout(autosize=True
                       , plot_bgcolor='white'
                       , yaxis_title=None
                       , xaxis_title=None
                       , title={
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'}
                       , title_font_color='#7F7F7F')
fig_norm.write_html('results/'+time_period+'_likes_norm.html')
py.plot(fig_norm, filename=time_period+'_likes_norm', auto_open = False)