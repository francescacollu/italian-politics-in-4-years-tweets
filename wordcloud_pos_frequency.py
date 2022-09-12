import pandas as pd
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator
import csv


font_path = 'silianrail.otf'
pos_list = ['VERB','NOUN','ADJ','PROPN']

def create_and_save_wordcloud(politician_name, df):
    df = df.iloc[:, 1:]
    df = list(df.to_records(index=False))
    df = [(el[0], int(el[1])) for el in df]

    mask = np.array(Image.open('masks/'+politician_name+'_mask.png'))
    mask_colors = ImageColorGenerator(mask)
    word_cloud = WordCloud(font_path=font_path, 
                        mask=mask, 
                        background_color="white", 
                        max_words=2500, max_font_size=256, random_state=42, 
                        width=mask.shape[1], height=mask.shape[0],
                        color_func=mask_colors
                        ).generate_from_frequencies(dict(df))
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('results/'+politician_name+'_'+'+'.join(pos_list)+'_wc.png', dpi=500)

meloni_pos = pd.read_csv('results/meloni/meloni_'+'+'.join(pos_list)+'.csv')
salvini_pos = pd.read_csv('results/salvini/salvini_'+'+'.join(pos_list)+'.csv')
letta_pos = pd.read_csv('results/letta/letta_'+'+'.join(pos_list)+'.csv')
renzi_pos = pd.read_csv('results/renzi/renzi_'+'+'.join(pos_list)+'.csv')
conte_pos = pd.read_csv('results/conte/conte_'+'+'.join(pos_list)+'.csv')
calenda_pos = pd.read_csv('results/calenda/calenda_'+'+'.join(pos_list)+'.csv')

create_and_save_wordcloud('meloni', meloni_pos)
create_and_save_wordcloud('salvini', salvini_pos)
create_and_save_wordcloud('letta', letta_pos)
create_and_save_wordcloud('renzi', renzi_pos)
create_and_save_wordcloud('conte', conte_pos)
create_and_save_wordcloud('calenda', calenda_pos)
