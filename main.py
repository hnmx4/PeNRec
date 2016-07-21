# -*- coding:utf-8 -*-

import modeling
import json
import codecs
import numpy as np
import pprint

from os.path import join, abspath, dirname
from os import listdir
from gensim.models import word2vec
from sklearn.cluster import KMeans


files = listdir(abspath(dirname(__file__)))
if 'word2vec.model' in files:
    model = word2vec.Word2Vec.load('word2vec.model')
else:
    model = modeling.create_word2vec_model()

vocab = model.vocab
f = open(join(abspath(dirname(__file__)), 'nouns.json'), 'r')
nouns = json.loads(f.read())
f.close()

features = np.empty([0, 200], float)
for noun in nouns:
    features = np.append(features, np.array(model[noun])[np.newaxis, :], axis=0)

kmeans_model = KMeans(n_clusters=20, random_state=10).fit(features)

labels = kmeans_model.labels_

cluster = {}
for label, noun in zip(labels, nouns):
    cluster[noun] = label

count = {}
for label in labels:
    count[label] = 0
f = open(join(abspath(dirname(__file__)), 'twitter-nouns.json'), 'r')
twitter_nouns = json.loads(f.read())
f.close()
for noun in twitter_nouns:
    count[cluster[noun]] += 1
most_interest_label = sorted(count.items(), key=lambda x: x[1], reverse=True)[0][0]

f = open(join(abspath(dirname(__file__)), 'nhk-articles.json'), 'r')
nhk_articles = json.loads(f.read())
f.close()
match_articles = {}
for k, v in nhk_articles.items():
    count = {}
    for label in labels:
        count[label] = 0
    deno = 0
    for word in v['nouns']:
        count[cluster[word]] += 1
        deno += 1
    most = sorted(count.items(), key=lambda x: x[1], reverse=True)[0]
    v['label'] = most[0]
    v['rate'] = most[1] / deno
    nhk_articles[k] = v

    if v['label'] == most_interest_label:
        match_articles[k] = v

match_articles = sorted(match_articles.items(), key=lambda x: x[1]['rate'], reverse=True)
for k, v in match_articles[:16]:
    print(k, v['url'], v['rate'])

interest = []
for noun in twitter_nouns:
    if cluster[noun] == most_interest_label:
        interest.append(noun)

print(interest)
