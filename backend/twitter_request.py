import tweepy
import Token
import json
from textblob import TextBlob
import datetime
from decimal import Decimal


def get_api():
    auth = tweepy.OAuthHandler(Token.consumer_key(), Token.consumer_secret())
    api = tweepy.API(auth)
    return api

def update_max_min(tweet_text,sentiment, data):
    if(data['max'][0] < sentiment):
        data['max'][0] = sentiment
        data['max'][1] = tweet_text
    if(data['min'][0] > sentiment):
        data['min'][0] = sentiment
        data['min'][1] = tweet_text
    return data


def get_tweets(long,lat,rad,q,datestr):
#lon,lat,radius, query
    api= get_api()
    longitude = long
    latitude = lat
    radius = rad
    query = q
    lang = 'en'
    result_type = 'mixed'
    geo = latitude+','+longitude+','+radius+'km'
    target_date = datetime.datetime.strptime(datestr,'%Y-%m-%d').date()
    api_date = target_date+ datetime.timedelta(days=1)
    #print('target date: {} api_date: {}'.format(target_date, api_date))
    #number of tweets to analize
    cnt = 200
    total_feeling = 0
    tweets = [tweet for tweet in tweepy.Cursor(api.search, q = query, geocode = geo, lang = lang, until = api_date, tweet_mode = 'extended').items(cnt)]
    max_min_tweets = {"min": [1,"min tweat"], "max": [-1, "max tweet"]}
    #print(max_min_tweets)

    valid_tweet_count = 0
    for tweet in tweets:
        #make sure tweet is on the target date
        tweet_date = tweet.created_at.date()
        if(tweet_date == target_date):
            valid_tweet_count+=1

            blob = TextBlob(tweet.full_text)
            feeling = blob.sentiment
            #update the max/min tweets
            max_min_tweets = update_max_min(tweet.full_text,feeling[0], max_min_tweets)

            total_feeling = total_feeling + feeling[0]

            #keep running list of most popular tags

    return_dictionary = {}
    if(valid_tweet_count > 0):
        average_feeling = total_feeling / valid_tweet_count
        return_dictionary['average_sentiment'] = average_feeling
        return_dictionary['max_sentiment'] = max_min_tweets['max']
        return_dictionary['min_sentiment'] = max_min_tweets['min']
        #print('The average sentiment on the day is: {}'.format(average_feeling))
    # else:
    #     print('No tweets for selection')

    #print(max_min_tweets)
    return_dictionary['number_of_tweets'] = valid_tweet_count
    #return_dictionary['date'] = target_date.strftime('%Y-%m-%d')
    outer_dictionary = {}
    key_day = target_date.strftime('%Y-%m-%d')
    outer_dictionary[key_day] = return_dictionary

    #print(return_dictionary)
    #print(json.dumps(outer_dictionary))
    return(json.dumps(outer_dictionary))

#test code
if __name__ == "__main__":
    longitude = '-87.785555'
    latitude = '41.812925'
    radius = '50'
    query = 'snow #winter -filter:retweets'
    date = '2020-11-24'
    get_tweets(longitude,latitude,radius,query, date)
    #YYYYMMDDHHmm
    # startDate = '202011160000'
    # endDate = '202011170000'
