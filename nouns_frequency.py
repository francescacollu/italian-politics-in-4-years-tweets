import pandas as pd
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator
import csv


font_path = 'silianrail.otf'

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
    plt.savefig('results/'+politician_name+'_wc.png', dpi=500)

meloni_nouns = pd.read_csv('results/meloni/meloni_NOUNS.csv')
salvini_nouns = pd.read_csv('results/salvini/salvini_NOUNS.csv')
letta_nouns = pd.read_csv('results/letta/letta_NOUNS.csv')
renzi_nouns = pd.read_csv('results/renzi/renzi_NOUNS.csv')
conte_nouns = pd.read_csv('results/conte/conte_NOUNS.csv')
calenda_nouns = pd.read_csv('results/calenda/calenda_NOUNS.csv')

create_and_save_wordcloud('meloni', meloni_nouns)
create_and_save_wordcloud('salvini', salvini_nouns)
create_and_save_wordcloud('letta', letta_nouns)
create_and_save_wordcloud('renzi', renzi_nouns)
create_and_save_wordcloud('conte', conte_nouns)
create_and_save_wordcloud('calenda', calenda_nouns)
