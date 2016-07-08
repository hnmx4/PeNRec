# -*- coding:utf-8 -*-

import dotenv
import tweepy
import MeCab
import yaml
import pprint

from os.path import join, dirname
from pymongo import MongoClient


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)


auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

client = MongoClient('localhost', 27017)
db = client.penrec
collection_tweets = db.tweets
collection_words = db.wors
collection_positive = db.positive
collection_negative = db.negative


def process_tweet(tw):
    if not tw.retweeted:
        text = tw.text
        entity = tw.entities
        if 'media' in entity:
            for media in entity['media']:
                text = text.replace(media['display_url'], '')
                text = text.replace(media['expanded_url'], '')

        if len(entity['urls']) > 0:
            for url in entity['urls']:
                text = text.replace(url['url'], '')
        elif len(entity['user_mentions']) > 0:
            for user in entity['user_mentions']:
                identity = '@' + user['screen_name']
                text = text.replace(identity, '')
        return text


def extract_nouns(sen):
    nouns = []
    mecab = MeCab.Tagger('')
    for chunk in mecab.parse(sen).splitlines():
        if chunk == 'EOS':
            continue
        (surface, feature) = chunk.split('\t')
        if feature.startswith('名詞'):
            nouns.append(surface)
    return nouns


tweets = api.user_timeline(count=50)
words = []
for tweet in tweets:
    processed_tweet = process_tweet(tweet)
    if processed_tweet:
        words.extend(extract_nouns(processed_tweet))

frec = {}
for word in words:
    if word in frec:
        frec[word] += 1
    else:
        frec[word] = 1

f = open(join(dirname(__file__), 'word_list.yml'), 'w')
f.write(yaml.dump(frec, allow_unicode=True))
f.close()
