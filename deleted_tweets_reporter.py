#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitter import *
from collections import OrderedDict
import datetime
from gmail import *

REPORTING_EMAIL_ADDRES = "xxxxxxxxxx@xx.xx"
TWITTER_CONSUMER_KEY = "xxxxxxxxxx"
TWITTER_CONSUMER_SECRET = "xxxxxxxxxx"
TWITTER_TOKEN = "xxxxxxxxxx"
TWITTER_TOKEN_SECRET = "xxxxxxxxxx"
GMAIL_ADDRESS = "xxxxxxxxxx@gmail.com"
GMAIL_PASSWORD = "xxxxxxxxxx"

NUM_REPORTING_TWEETS = 50
CACHE_SIZE = 10000

def send_deleted_tweet_mail(deleted_tweets):
    subject = "Deleted Tweet Report [" + str(datetime.datetime.today()) + "]"
    body = u"\n\n".join(deleted_tweets)
    gmail = GMail(GMAIL_ADDRESS, GMAIL_PASSWORD)
    msg = Message(subject, to=REPORTING_EMAIL_ADDRES, text=body)
    gmail.send(msg)


auth = OAuth(
    consumer_key=TWITTER_CONSUMER_KEY,
    consumer_secret=TWITTER_CONSUMER_SECRET,
    token=TWITTER_TOKEN,
    token_secret=TWITTER_TOKEN_SECRET
)
twitter_userstream = TwitterStream(auth=auth, domain="userstream.twitter.com")

tweets_dict = OrderedDict()
deleted_tweets = []

for tweet in twitter_userstream.user():
    if "id" in tweet and "text" in tweet and "user" in tweet and "screen_name" in tweet["user"]:
        tweets_dict[tweet["id"]] = (tweet["user"]["screen_name"], tweet["text"])
    elif "delete" in tweet and "status" in tweet["delete"] and "id" in tweet["delete"]["status"]:
        deleted_tweet_id = tweet["delete"]["status"]["id"]
        if deleted_tweet_id in tweets_dict:
            deleted_tweet = tweets_dict[deleted_tweet_id]
            deleted_tweets.append(u"{0}:\t{1}".format(deleted_tweet[0], deleted_tweet[1]))

    if len(deleted_tweets) >= NUM_REPORTING_TWEETS:
        send_deleted_tweet_mail(deleted_tweets)
        deleted_tweets = []

    if len(tweets_dict) > CACHE_SIZE:
        tweets_dict.popitem(last=False) # 最初に追加したのアイテムを削除

