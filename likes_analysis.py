import pandas as pd
import plotly.express as px

meloni = pd.read_csv('tweets_meloni.csv')
meloni['datetime'] = pd.to_datetime(meloni.datetime).dt.date
meloni['datetime'] = meloni['datetime'].astype(str).strftime('%Y-%m')
meloni = meloni[['id', 'datetime', 'like_count']]
meloni = meloni.groupby('datetime').agg({'id':'count', 'like_count': 'sum'}).reset_index().rename(columns={'id':'tweet_count'})

fig = px.scatter(meloni, x='datetime', y='like_count', size='tweet_count')
fig.show()