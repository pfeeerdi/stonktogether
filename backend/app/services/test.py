search_words="Apple"
tweets=2
import pandas as pd
import numpy
pd.options.mode.chained_assignment = None
import os
import tweepy as tw
#print(os.getcwd())

#Twitter API config
consumer_key= 'vvoCCekgIRltBaA28KPeqV5PH'
consumer_secret= 'wbJdfJgPQo6bojNVWtX2FoH8RNXMG7OA7xNis1HOS5tt4E3kN7'
access_token= '216684460-uXpFa0MbWSjZyKrLLajc42VELc7GzFZPIs53PV3g'
access_token_secret= 'quTUm4pTmVv9Uy2AZanWQcErohcDdoFWzUWg17pLtTriC'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

print("Done line 19")

#Twitter data
tweets = tw.Cursor(api.search_tweets, 
                            q=search_words,
                            lang="en"
                    ).items(tweets)
print("Done line 27")
users_tweets = [[tweet.id, tweet.user.screen_name, tweet.text, tweet.created_at, tweet.user.location] for tweet in tweets]
#Open dataframe to use Sentiment Analysis
tweet_text = pd.DataFrame(data=users_tweets, 
                    columns=['id', 'user', "text", "created_at", "location"])
print("Done line 28")
print(tweet_text)
#NLP
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer

#Cleaning dataset
for i in range(0, len(tweet_text)):
    #Tokenize and set words to lowercase 
    review = tweet_text["text"][i]
    review = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",review).split())
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower()
    review = review.split()

    #stopwords: 
    all_stopwords = [word for word in stopwords.words("english") if word not in ["no","nor","not"]]
    all_stopwords.extend(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","&amp","amp","amp;","&amp;","nhs", "rt"])
    #lemmatization:
    lemma = nltk.wordnet.WordNetLemmatizer()
    review = " ".join([lemma.lemmatize(word) for word in review if word not in set(all_stopwords)])    
    tweet_text["text"][i] = review


#Sentiment analysis with NLTK
tweet_text["sentiment"] = dict
tweet_text["sentiment_compound"] = 0.0

def sentiment_score(dataset):
    sia = SentimentIntensityAnalyzer()
    for i in range(len(dataset)):
        dataset["sentiment"][i] = sia.polarity_scores(dataset["text"][i])
        dataset["sentiment_compound"][i] = dataset["sentiment"][i]["compound"]
sentiment_score(tweet_text)
tweet_ids = tweet_text[['id', 'sentiment', 'sentiment_compound']]
tweet_ids = tweet_text.sort_values("sentiment_compound", ascending=False, ignore_index=True)
#save as csv
#tweet_text.to_csv("saved_sentiment_data/tweet_complete.csv")
#tweet_ids.to_csv("saved_tweet_ids/tweet_ids.csv")

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statistics
import scipy
from scipy import signal

#tweets = pd.read_csv("../sentiment/saved_sentiment_data/tweet_complete.csv", index_col=0, converters={'hashtags': eval, 'sentiment':eval})
tweets = tweet_text
pos_sentiment = [sentiment for sentiment in tweets["sentiment_compound"] if (sentiment >= 0.33)]
neg_sentiment = [sentiment for sentiment in tweets["sentiment_compound"] if (sentiment <= - 0.33)]
neu_sentiment = [sentiment for sentiment in tweets["sentiment_compound"] if (sentiment < 0.33 and sentiment > -0.33)]

fig = px.box(
    y=tweets["sentiment_compound"],
    title = "Overall Sentiment",
    labels={"y":"Sentiment"})
#fig.show()
#fig.write_html("output/Sentiment_Boxplot.html")
fig.write_image("output/Sentiment_Boxplot.png")

fig = px.bar(
    x=["Positive", "Neutral", "Negative"],
    y=[len(pos_sentiment), len(neu_sentiment), len(neg_sentiment)],
    title="Amount of tweets by sentiment",
    labels={"x":"Sentiment","y":"Amount of tweets"})
#fig.show()
#fig.write_html("output/Sentiment_Amount.html")
fig.write_image("output/Sentiment_Amount.png")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(data, title="", filename=""):
    text = " ".join(t for t in data.dropna())
    stopwords = ["amp", "stonks", "https", "RT", "Retweet this", "Airdrop", "t co", "Link"]
    wordcloud = WordCloud(stopwords = stopwords, scale=4, max_font_size=50, max_words=200,background_color="white").generate(text)
    wordcloud.to_file(filename)

generate_wordcloud(tweets["text"], "Most common Words among all tweets", "output/wordcloud_all.png")
generate_wordcloud(tweets["text"][tweets["sentiment_compound"] >= 0.33], "Most common Words in tweets with positive sentiment", "output/wordcloud_positive.png")
generate_wordcloud(tweets["text"][tweets["sentiment_compound"] <= -0.33], "Most common Words in tweets with negative sentiment", "output/wordcloud_negative.png")

#keyword_sentiment("Apple", 200)