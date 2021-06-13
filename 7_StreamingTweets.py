from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from unidecode import unidecode
import time

from keys import *

# Tweepy is an open source Python package that gives you a very convenient way to access the Twitter API with Python. 
# Tweepy includes a set of classes and methods that represent Twitter’s models and RESTful API endpoints, and it transparently handles various implementation details.

# A RESTful API is an architectural style for an application program interface (API) that uses HTTP requests to access and use data. 
# That data can be used to GET, PUT, POST and DELETE data types, which refers to the reading, updating, creating and deleting of operations concerning resources.

# REST = Representational State Transfer. REST or RESTful API design (Representational State Transfer) is designed to take advantage of existing protocols. 
# While REST can be used over nearly any protocol, it usually takes advantage of HTTP when used for Web APIs. 
# This means that developers do not need to install libraries or additional software in order to take advantage of a REST API design. 


# creates a table if it doesnt exists
conn = sqlite3.connect('twitter.db')
c = conn.cursor()

# def create_table():
#     c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
#     conn.commit()

# create_table()

# This is to make it faster but it is a memory hog
def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()



analyzer = SentimentIntensityAnalyzer()

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']

            # ==== Sentiment ====
            # vs = analyzer.polarity_scores(tweet)
            # sentiment = vs['compound']

            # ==== textblob ====
            analysis = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity
            
            # if analysis.sentiment.polarity >= 0.0001:
            #     if analysis.sentiment.polarity > 0:
            #         sentiment = analysis.sentiment.polarity
            # elif analysis.sentiment.polarity <= -0.0001:
            #     if analysis.sentiment.polarity <= 0:
            #         sentiment = analysis.sentiment.polarity
                    
            # if sentiment is not None:
            # print(time_ms, tweet, sentiment)
            # print(data)
            #sentiment is the table we created above - sqlite language
            print(tweet)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)

# auth = OAuthHandler(ckey, csecret)
# auth.set_access_token(atoken, asecret)

# twitterStream = Stream(auth, listener())
# twitterStream.filter(track=["a","e","i","o","u"])

# for some reason this would break every now and then so created error handling to just wait 5 seconds
while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        # twitterStream.filter(track=["a","e","i","o","u"])
        twitterStream.filter(track=["Sun"])
    except Exception as e:
        print(str(e))
        time.sleep(5)


# once we ran this it created a db twitter.db of all those tweets