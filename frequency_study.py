import pandas as pd
import spacy
from collections import Counter
import os
import glob

data_path = 'data/'

color_map = {
    'Meloni':'#000000',
    'Salvini':'#17A556',
    'Letta':'#E2202B',
    'Renzi':'#F3147E',
    'Conte':'#F5BE23',
    'Calenda':'#002A8D'
}

def get_tweet_text_list(df):
    texts = list(df['text'])
    # text = ' '.join(df['text'].to_list())
    # text = text.replace("un'", "una ").replace("un’", "una ")
    return texts

meloni = pd.read_csv(data_path+'tweets_meloni.csv')
salvini = pd.read_csv(data_path+'tweets_salvini.csv')
letta = pd.read_csv(data_path+'tweets_letta.csv')
renzi = pd.read_csv(data_path+'tweets_renzi.csv')
conte = pd.read_csv(data_path+'tweets_conte.csv')
calenda = pd.read_csv(data_path+'tweets_calenda.csv')

nlp = spacy.load("it_core_news_sm", disable=["parser", "ner"])
leaders = [meloni, salvini, letta, renzi, conte, calenda]


def is_good_token(token):
    return not token.is_stop and not token.is_punct and not token.is_space and len(token.text)>1 and token.pos_!='ADP' and token.pos_!='AUX' and token.pos_!='ADV' and not 'https://' in token.text and not '@' in token.text

def get_docs(df):
    texts = get_tweet_text_list(df)
    #nlp.max_length = len(texts)
    docs = list(nlp.pipe(texts))
    return docs

def get_pos_occurrences_per_doc(doc, pos_list): #possible pos: 'VERB', 'NOUN', 'ADJ', 'PROPN'
    part_of_speech_elements = [token.lemma_ for token in doc if token.pos_ in pos_list and is_good_token(token)]
    part_of_speech_elements_occurrences = Counter(part_of_speech_elements)
    part_of_speech_elements_occurrences = part_of_speech_elements_occurrences.most_common()
    if len(part_of_speech_elements_occurrences)>0:
        return pd.DataFrame(part_of_speech_elements_occurrences, columns=['occurrence', 'frequency'])

def get_pos_occurrences_per_all_docs(docs, leader_name, pos_list):
    df_occurrences = pd.DataFrame(columns=['occurrence', 'frequency'])
    for doc in docs:
        df_occurrences_per_doc = get_pos_occurrences_per_doc(doc, pos_list)
        df_occurrences = pd.concat([df_occurrences, df_occurrences_per_doc])
    df_occurrences['frequency'] = df_occurrences['frequency'].astype(int)
    df_occurrences = df_occurrences.groupby('occurrence').sum().reset_index()
    df_occurrences = df_occurrences.sort_values(by='frequency', ascending=False)
    df_occurrences.to_csv('results/'+leader_name+'/'+leader_name+'_'+'+'.join(pos_list)+'.csv')


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

def clean_folder(leader_name):
    files = glob.glob('results/'+leader_name+'/*.csv')
    for f in files:
        os.remove(f)

for i, leader in enumerate(leaders):
    leader_name = retrieve_name_from_df(i)
    # clean_folder(leader_name)
    print(leader_name)
    docs = get_docs(leader)
    # get_pos_occurrences_per_all_docs(docs, leader_name, ['VERB','NOUN','ADJ','PROPN'])
    # print('VERBS+NOUNS+ADJS+PROPNS done!')
    # get_pos_occurrences_per_all_docs(docs, leader_name, ['VERB'])
    # print('VERBS done!')
    get_pos_occurrences_per_all_docs(docs, leader_name, ['NOUN'])
    print('NOUNS done!')
    # get_pos_occurrences_per_all_docs(docs, leader_name, ['ADJ'])
    # print('ADJS done!')
    # get_pos_occurrences_per_all_docs(docs, leader_name, ['PROPN'])
    # print('PROPNS done!')