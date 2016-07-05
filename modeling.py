# -*- coding:utf-8 -*-

import dotenv
import tweepy
import MeCab
import yaml
import pprint

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
        text = tweet.text
        entity = tweet.entities
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

        res = mecab.parse(text)
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
