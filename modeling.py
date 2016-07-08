# -*- coding:utf-8 -*-

import tweepy
import MeCab
import yaml

from common import denv
from os.path import join, dirname, abspath
from pprint import pprint
from pymongo import MongoClient


auth = tweepy.OAuthHandler(denv('CONSUMER_KEY'), denv('CONSUMER_SECRET'))
auth.set_access_token(denv('ACCESS_TOKEN'), denv('ACCESS_SECRET'))
api = tweepy.API(auth)

client = MongoClient('localhost', 27017)
db = client.penrec
c_tweets = db.tweets
c_words = db.wors
c_positive = db.positive
c_negative = db.negative
c_senti_noun_dict = db.sentiment_noun_dict
c_senti_dec_word_dict = db.sentiment_declinable_word_dict


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


def extract_nouns(s):
    nouns = []
    mecab = MeCab.Tagger('')
    for chunk in mecab.parse(s).splitlines():
        if chunk == 'EOS':
            continue
        (surface, feature) = chunk.split('\t')
        if feature.startswith('名詞'):
            nouns.append(surface)
    return nouns


def calculate_sentiment_value(s):
    nouns = extract_nouns(s)
    np_dict = {doc['word']: doc['value'] for doc in c_senti_noun_dict.find({}, {'word': 1, 'value': 1})}
    val = 0
    cnt = 0
    for noun in nouns:
        val = (lambda x: x + np_dict[noun] if noun in np_dict else x)(val)
        cnt += 1
    return val / cnt if cnt > 0 else 0


tweets = api.user_timeline(count=50)
words = []
senti = {}
for tweet in tweets:
    tweet = process_tweet(tweet)
    if tweet:
        words.extend(extract_nouns(tweet))
        senti[tweet] = calculate_sentiment_value(tweet)

frec = {}
for word in words:
    if word in frec:
        frec[word] += 1
    else:
        frec[word] = 1

f = open(join(dirname(__file__), 'word_list.yml'), 'w')
f.write(yaml.dump(frec, allow_unicode=True))
f.close()

f = open(join(dirname(__file__), 'senti_list.yml'), 'w')
f.write(yaml.dump(senti, allow_unicode=True))
f.close()
