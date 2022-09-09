import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import chart_studio.plotly as py
from credential_file import *
import chart_studio.tools as tls
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt

font_path = 'silianrail.otf'
tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file


def retrieve_name_from_df(i):
    if i==0:
        return 'meloni'
    elif i==1:
        return 'salvini'
    elif i==2:
        return 'letta'
    elif i==3:
        return 'renzi'
    elif i==4:
        return 'conte'
    elif i==5:
        return 'calenda'

wordcloud_color_map = {
    'meloni':(0,0,0),
    'salvini':(23, 165, 86),
    'letta':(226, 32, 43),
    'renzi':(243, 20, 126),
    'conte':(245, 190, 35),
    'calenda':(0, 42, 141)
}

meloni = pd.read_csv('results/meloni/meloni_red_PROPNS.csv', names=['propns', 'counts'])
salvini = pd.read_csv('results/salvini/salvini_red_PROPNS.csv', names=['propns', 'counts'])
letta = pd.read_csv('results/letta/letta_red_PROPNS.csv', names=['propns', 'counts'])
renzi = pd.read_csv('results/renzi/renzi_red_PROPNS.csv', names=['propns', 'counts'])
conte = pd.read_csv('results/conte/conte_red_PROPNS.csv', names=['propns', 'counts'])
calenda = pd.read_csv('results/calenda/calenda_red_PROPNS.csv', names=['propns', 'counts'])

leaders = [meloni, salvini, letta, renzi, conte, calenda]

def pick_color_by_leader(politician_name):
    return wordcloud_color_map[politician_name]

def create_and_save_wordcloud(politician_name, df):
    print(politician_name)
    df = list(df.to_records(index=False))
    df = [(el[0], int(el[1])) for el in df]
    word_cloud = WordCloud(font_path=font_path, 
                        background_color="white", 
                        max_words=2000, max_font_size=256, random_state=42, 
                        width=1200,
                        height=1000,
                        color_func=lambda *args, **kwargs: pick_color_by_leader(politician_name)
                        ).generate_from_frequencies(dict(df))
    word_cloud.recolor()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('results/'+politician_name+'_wc.png', dpi=500)

for i, leader in enumerate(leaders):
    create_and_save_wordcloud(retrieve_name_from_df(i), leader)

# meloni = pd.read_csv('results/meloni/meloni_PROPNS.csv', names=['propns', 'counts'])
# salvini = pd.read_csv('results/salvini/salvini_PROPNS.csv', names=['propns', 'counts'])
# letta = pd.read_csv('results/letta/letta_PROPNS.csv', names=['propns', 'counts'])
# renzi = pd.read_csv('results/renzi/renzi_PROPNS.csv', names=['propns', 'counts'])
# conte = pd.read_csv('results/conte/conte_PROPNS.csv', names=['propns', 'counts'])
# calenda = pd.read_csv('results/calenda/calenda_PROPNS.csv', names=['propns', 'counts'])

# meloni['leader'] = 'Meloni'
# salvini['leader'] = 'Salvini'
# letta['leader'] = 'Letta'
# renzi['leader'] = 'Renzi'
# conte['leader'] = 'Conte'
# calenda['leader'] = 'Calenda'

# mel_sal = pd.concat([meloni, salvini], ignore_index=True)
# mel_sal_let = pd.concat([mel_sal, letta], ignore_index=True)
# mel_sal_let_ren = pd.concat([mel_sal_let, renzi], ignore_index=True)
# propns_count = pd.concat([mel_sal_let_ren, conte], ignore_index=True)

# chosen_meloni['leader'] = 'Meloni'
# chosen_salvini['leader'] = 'Salvini'
# chosen_letta['leader'] = 'Letta'
# chosen_renzi['leader'] = 'Renzi'
# chosen_conte['leader'] = 'Conte'

# chosen_mel_sal = pd.concat([chosen_meloni, chosen_salvini], ignore_index=True)
# chosen_mel_sal_let = pd.concat([chosen_mel_sal, chosen_letta], ignore_index=True)
# chosen_mel_sal_let_ren = pd.concat([chosen_mel_sal_let, chosen_renzi], ignore_index=True)
# chosen_propns_count = pd.concat([chosen_mel_sal_let_ren, chosen_conte], ignore_index=True)

# chosen_propns_count['total'] = chosen_propns_count['counts'].groupby(chosen_propns_count['leader']).transform('sum')

# chosen_propns_count['percentage'] = chosen_propns_count['counts']/chosen_propns_count['total']

# fig = px.bar(chosen_propns_count, x="percentage", y="propns"
#             , color_discrete_map=color_map
#             , facet_col="leader"
#             , facet_col_wrap=5
#             , color='leader'
#             , orientation='h', text='propns'
#             #, facet_row_spacing=0.05 # default is 0.07 when facet_col_wrap is used
#             #, facet_col_spacing=0.04) # default is 0.03)#, opacity=0.)
#             , height=500, width=1000)
# #fig.update_traces(marker_color='white')
# fig.update_traces(textposition='outside', 
#                   insidetextanchor='start')
# fig.update_yaxes(matches=None
#                  #, tickmode = 'array'
#                  , visible=False
#                  , categoryorder = 'total ascending')
# fig.update_xaxes(visible=False
#                 #, showline=True, linewidth=0.5, linecolor='black', gridcolor='rgb(204,204,204)', spikedash='dot'
#                 #,  tickmode = 'array'
#                 , range=[0, 1]
#                 , tickvals = [0., 0.2, 0.4, 0.6, 0.8, 1.]
#                 , ticktext = ['0%', '20%', '40%', '60%', '80%', '100%'])
#                 #,tickfont=dict(size=16,color='#7F7F7F'))
# fig.update_traces(textfont_size=15, textfont_color='black')
# fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig.for_each_annotation(lambda a: a.update(font=dict(size=20, color='black')))
# fig.for_each_annotation(lambda a: a.update(text='<b>'+a.text+'</b>'))
# #fig.for_each_annotation(lambda a: a.update(opacity=0.3))
# fig.update_layout(autosize=True
#                   #, yaxis={'categoryorder':'total ascending'}
#                   , plot_bgcolor='white'
#                   , yaxis_visible=False
#                   , yaxis_title=None
#                   , showlegend=False)
# fig.write_html('results/most_common_propns.html')
# py.plot(fig, filename='most_common_propns', auto_open = False)