
# coding: utf-8

import tweepy
import time


auth = tweepy.OAuthHandler(consumer_token, consumer_secret) #Your bot credentials
auth.set_access_token(access_token, access_token_secret) #Your access token from Twitter Developer account


api = tweepy.API(auth)#create an authorisation object to access your bot
try:
    api.verify_credentials()
    print("Authentication OK") 
except:
    print("Error during authentication")



api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True) 



user = api.get_user("...........")#Your Twitter Bot name


def most_retweeted_tweet(account):
    tweets = api.user_timeline(screen_name=account, count=10 ,include_rts = False, exclude_replies = True, tweet_mode = 'extended')
    retweet = dict()
    for tweet in tweets:
        if tweet.retweet_count > 15 or tweet.favorite_count > 50:
            retweet[tweet.id] = tweet.full_text
    return retweet

while True:
    accounts = []
    for follower in tweepy.Cursor(api.friends, user.screen_name).items(): 
        accounts.append(follower.screen_name)
    to_be_retweeted = []
    for account in accounts:
        to_be_retweeted.append(most_retweeted_tweet(account))
    for tweet_account in to_be_retweeted:
        for tweet_id in list(tweet_account.keys()):
            tweet = api.get_status(id=tweet_id)
            try:
                api.retweet(id=tweet_id)
                print(tweet.text)
            except tweepy.TweepError:
                continue    
    time.sleep(300)

