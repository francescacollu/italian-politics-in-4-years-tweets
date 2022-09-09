import pandas as pd
import spacy
from collections import Counter
import random

data_path = 'data/'

meloni = pd.read_csv(data_path+'tweets_meloni.csv')
salvini = pd.read_csv(data_path+'tweets_salvini.csv')
letta = pd.read_csv(data_path+'tweets_letta.csv')
renzi = pd.read_csv(data_path+'tweets_renzi.csv')
conte = pd.read_csv(data_path+'tweets_conte.csv')
calenda = pd.read_csv(data_path+'tweets_calenda.csv')

leaders = [meloni, salvini, letta, renzi, conte, calenda]
nlp = spacy.load("it_core_news_sm", disable=["parser", "ner"])

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

def get_total_number_of_tweeted_words():
    df = pd.DataFrame(columns=['leader', 'total_tw_number'])
    for i,leader in enumerate(leaders):
        df.at[i, 'leader'] = retrieve_name_from_df(i)
        df.at[i, 'number_of_tweeted_words'] = len((' '.join(leader['text'].to_list())).split())
    return df

def get_corpus(df):
    min_words_number = int(get_total_number_of_tweeted_words()['number_of_tweeted_words'].min())
    words_list = (' '.join(df['text'].to_list())).lower().split()
    corpus = ' '.join(random.sample(words_list, min_words_number))
    return corpus

def get_doc(df):
    corpus = get_corpus(df)
    doc = nlp(corpus)
    return doc

def is_good_token(token):
    return not token.is_punct and not token.is_space and not 'https://' in token.text and not '@' in token.text

def get_number_of_lemmas_in_corpus(doc):
    lemmas = [token.lemma_ for token in doc if is_good_token(token)]
    lemmas_occurrences = Counter(lemmas)
    lemmas_occurrences = lemmas_occurrences.most_common()
    if len(lemmas_occurrences)>0:
        return pd.DataFrame(lemmas_occurrences, columns=['lemma', 'frequency'])

def get_number_of_tokens_in_corpus(doc):
    tokens = [token.text for token in doc if is_good_token(token)]
    tokens_occurrences = Counter(tokens)
    tokens_occurrences = tokens_occurrences.most_common()
    if len(tokens_occurrences)>0:
        return pd.DataFrame(tokens_occurrences, columns=['token', 'frequency'])
    
# def get_number_of_stems_in_total_corpus(docs):
#     df_lemmas_occurrences = pd.DataFrame(columns=['lemma', 'frequency'])
#     for doc in docs:
#         df_lemmas_occurrences_per_doc = get_number_of_stems_in_corpus(doc)
#         df_lemmas_occurrences = pd.concat([df_lemmas_occurrences, df_lemmas_occurrences_per_doc])
#     df_lemmas_occurrences['frequency'] = df_lemmas_occurrences['frequency'].astype(int)
#     df_lemmas_occurrences = df_lemmas_occurrences.groupby('lemma').sum().reset_index()
#     df_lemmas_occurrences = df_lemmas_occurrences.sort_values(by='frequency', ascending=False)
#     return df_lemmas_occurrences

lexical_richness = pd.DataFrame(columns=['leader', 'TTR', 'L-TTR'])
for i, leader in enumerate(leaders):
    leader_name = retrieve_name_from_df(i)
    lexical_richness.at[i, 'leader'] = leader_name
    print(leader_name)
    doc = get_doc(leader)
    plain_corpus = get_corpus(leader)
    print(len(plain_corpus.split()))
    lexical_richness.at[i, 'L-TTR'] = len(get_number_of_lemmas_in_corpus(doc))/len(plain_corpus.split())
    lexical_richness.at[i, 'TTR'] = len(get_number_of_tokens_in_corpus(doc))/len(plain_corpus.split())

lexical_richness.sort_values(by='TTR', ascending=False).to_csv('results/lexical_richness.csv')