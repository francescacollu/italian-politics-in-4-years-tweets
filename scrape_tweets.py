import snscrape.modules.twitter as sntwitter
import pandas as pd

tweets_list = []
politician_name = 'calenda'
start_date = '2018-03-23' #yyyy-mm-dd
end_date = '2022-08-30' #yyyy-mm-dd

def get_politician_username(politician_name):
    if politician_name=='meloni':
        return 'GiorgiaMeloni'
    elif politician_name=='salvini':
        return 'matteosalvinimi'
    elif politician_name=='letta':
        return 'EnricoLetta'
    elif politician_name=='renzi':
        return 'matteorenzi'
    elif politician_name=='conte':
        return 'GiuseppeConteIT'
    elif politician_name=='calenda':
        return 'CarloCalenda'
    


for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+get_politician_username(politician_name)+' since:'+start_date+' until:'+end_date).get_items()): 
    print(tweet.date)
    tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount]) # declare the attributes to be returned
    
# Creating a dataframe from the tweets list above: 
tweets_df = pd.DataFrame(tweets_list, columns=['id', 'datetime', 'text', 'username', 'reply_count', 'retweet_count', 'like_count', 'quote_count'])
tweets_df.to_csv('data/tweets_'+politician_name+'.csv')