import pandas as pd
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator
from collections import Counter

politician_name = 'meloni'
font_path = 'silianrail.otf'

nlp = spacy.load("it_core_news_sm")

df = pd.read_csv('tweets_'+politician_name+'.csv')
df = df['text'].to_list()
df = ' '.join(df)
df = df.replace("un'", "una ").replace("un’", "una ")
doc = nlp(df)

def is_good_token(token):
    return not token.is_stop and not token.is_punct and not token.is_space and len(token.text)>2 and token.pos_!='ADP' and token.pos_!='AUX' and token.pos_!='ADV' and not 'https://' in token.text and not '@' in token.text

lemmas = [token.lemma_.lower() for token in doc if is_good_token(token)]
lemma_occurrences = Counter(lemmas)
most_common_40_lemma_occurrences = lemma_occurrences.most_common(40)

mask = np.array(Image.open('masks/'+politician_name+'_mask.png'))
mask_colors = ImageColorGenerator(mask)
word_cloud = WordCloud(font_path=font_path, 
                       mask=mask, 
                       background_color="white", 
                       max_words=2000, max_font_size=256, random_state=42, 
                       width=mask.shape[1], height=mask.shape[0],
                       color_func=mask_colors
                       ).generate_from_frequencies(lemma_occurrences)
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis('off')
plt.savefig('results/'+politician_name+'_wc.png', dpi=500)