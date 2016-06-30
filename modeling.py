# -*- coding:utf-8 -*-

import dotenv
import tweepy
import MeCab
import yaml

from os.path import join, dirname


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)


auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

tweets = api.user_timeline(count=50)
mecab = MeCab.Tagger('-Owakati')
words = []

for tweet in tweets:
    if not tweet.retweeted:
        res = mecab.parse(tweet.text)
        words.extend(res.split())

frec = {}
for word in words:
    if word in frec:
        frec[word] += 1
    else:
        frec[word] = 1

f = open(join(dirname(__file__), 'word_list.yml'), 'w')
f.write(yaml.dump(frec, allow_unicode=True))
f.close()
