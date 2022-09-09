import pandas as pd
import string 
from stop_words import get_stop_words
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import os

main_theme = 'putin'
path = 'data/text_replies_'+main_theme+'.csv'
df = pd.read_csv(path)

tweets = df['body'].astype(str)

# Fissiamo il numero di cluster
n_clusters = 10

# Definire il tokenizzatore, cioè il metodo di divisione delle stringhe in tokens ovvero sequenze di caratteri che adottiamo come forme grafiche (unità statistiche)
def mytokenizer(tweet):
    tokenlist = tweet.split()
    tokenlist = [token for token in tokenlist if token != """ ' """ and len(token) > 3] # escludo gli apostrofi, spesso non riconosciuti tra i caratteri di punteggiatura
    new_tweet = []
    for t in tokenlist:
        if (t[0:4] != "http") and (t[0] != "@"):
            new_tweet.append(t)
    new_tweet = " ".join(new_tweet)
    clean_tweet = new_tweet.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    tokens = clean_tweet.split(" ")
    new_tokens = []
    for token in tokens:
        if(token.isalnum() and token.isnumeric()==False):
            new_tokens.append(token)
    return new_tokens

nlp = spacy.load('it_core_news_sm')
def mylemmatizer(tweet):
    sent = []
    doc = nlp(tweet)
    for word in doc:
        sent.append(word.lemma_)
    return " ".join(sent)

tweets = [mylemmatizer(doc) for doc in tweets]

stoplist_1 = get_stop_words("it")
stoplist_2 = stopwords.words("italian")
stoplist = list(set(stoplist_1+stoplist_2))

# Vettorizzazione: è cruciale adottare il giusto metodo in base alle analisi che si vogliono produrre in seguito

# Usiamo un metodo di vettorizzazione non più basato sul mero conteggio di frequenze (TF) ma introduciamo un ftweetre di scala legato ai documenti. Utilizziamo quindi una vettorizzazione basata sull'indice TF-IDF (Term Frequency - Inverse Document Frequency) che misura l'importanza di un termine rispetto a un documento o a una collezione di documenti.
print('Let us begin vectorization!')
vett = TfidfVectorizer(ngram_range=(1,3),
                       max_features=1000, # n.massimo di parole da considerare
                       stop_words=stoplist_1,
                       min_df = 4, # frequenza minima di una forma grafica per essere considerata
                       tokenizer=mytokenizer)

V = vett.fit_transform(tweets) # il parametro di input deve essere una stringa
words = vett.get_feature_names_out()

print('Vectorization just finished!')

# Ora abbiamo ottenuto una matrice documenti x forme grafiche con una metrica TF*IDF e possiamo operare una riduzione dimensionale.

# Una riduzione dimensionale su una matrice testuale è un tipo di tecnica per ottenere una estrazione dei ftweetri latenti che caratterizzano le variabili  (= parole) del corpus.
# Utilizziamo il metodo di Non-Negative Matrix Factorization, mediante cui una matrice V può essere decomposta nel prodotto di due matrici W e H (W x H = V))

model = NMF(n_components=n_clusters, random_state=1) # occorre specificare il n. di ftweetri da estrarre

print('Writing Frobenius norm of the matrices difference')

# Model fit
W = model.fit_transform(V) # matrice documenti x punteggi topic
with open('results/clusterization_'+main_theme+'/FrobeniusNormMatricesDifference.txt', 'w') as f:
    f.write(str(model.reconstruction_err_))
H = model.components_

# Osserviamo le saturazione delle forme grafiche sui vari topic
# Ovver: i maggiori punteggi di factor loading delle parole sui ftweetri estratti

word_topic_df = pd.DataFrame(H.T, index=words)

print('Wordcloud started!')
# Adesso iteriamo su ognuna delle colonne del word topic dataframe:
sns.set_style("whitegrid", {'axes.grid' : False}) # Settiamo il tema di Seaborn senza griglia
for topic in range(len(word_topic_df.columns)):
    #print("Topic " +str(topic)+ " top words\n", word_topic_df[topic].sort_values(ascending=False).head(6), "\n\n")
    wordcloud = WordCloud(background_color='black', max_words=100).generate_from_frequencies(word_topic_df[topic])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('Topic '+str(topic))
    plt.savefig('results/clusterization_'+main_theme+'/Topic '+str(topic)+'.png')
    plt.close()


# Adesso esporiamo le matrici ottenute via decomposizione (W e H) in due fogli di calcolo dello stesso file Excel:
writer = pd.ExcelWriter('results/clusterization_'+main_theme+'/Topic_modeling_NMF.xlsx') # Inizializziamo il writer

document_topic_df = pd.DataFrame(W)
document_topic_df["topic"] = document_topic_df.idxmax(axis=1) # Etichetta del topic
document_topic_df["tweet_id"] = df["tweet_id"]
document_topic_df["body"] = df["body"]
#document_topic_df["ProposingParty"] = df["NomeGruppoParlamentare"]

# Esportiamo i 2 dataframe
document_topic_df.to_excel(writer, sheet_name='document_topic')
word_topic_df.to_excel(writer, sheet_name='word_topic')

def get_number_of_tweets_per_topic(document_topic_df):
    df = pd.DataFrame()
    df['topic'] = document_topic_df['topic'].unique()
    df['tweets_number'] = document_topic_df.groupby(['topic']).size()
    return df

def WriteClusterFeatures(writer, word_topic_df):
    df = pd.DataFrame()
    for topic in range(len(word_topic_df.columns)):
        df[topic]= word_topic_df[topic].sort_values(ascending=False).head(50).index
    df.to_excel(writer, sheet_name='clusters_features')

WriteClusterFeatures(writer, word_topic_df)
writer.save()

df_topic_distribution = get_number_of_tweets_per_topic(document_topic_df)
df_topic_distribution = df_topic_distribution.sort_values(by=['tweets_number'])
ax = df_topic_distribution.plot.barh(x='topic', y='tweets_number', rot=60, color='#822433', legend=False)
plt.tight_layout
plt.title('Bills distribution over topics')
plt.savefig('results/clusterization_'+main_theme+'/BillsDistributionOverTopics.png')
