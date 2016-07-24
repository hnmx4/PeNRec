# -*- coding:utf-8 -*-

import modeling
import numpy as np
import matplotlib.pyplot as plot
import pprint

from os.path import join, abspath, dirname
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from common import read_json_file


model = modeling.create_word2vec_model()

nouns = read_json_file('nouns')

features = np.empty([0, 200], float)
for noun in nouns:
    features = np.append(features, np.array(model[noun])[np.newaxis, :], axis=0)

n_clusters = 6
kmeans_model = KMeans(n_clusters=n_clusters, random_state=10).fit(features)

labels = kmeans_model.labels_

cluster = {}
for label, noun in zip(labels, nouns):
    cluster[noun] = label

count = {}
for label in labels:
    count[label] = 0

twitter_nouns = read_json_file('twitter-nouns')
for noun in twitter_nouns:
    count[cluster[noun]] += 1
most_interest_label = sorted(count.items(), key=lambda x: x[1], reverse=True)[0][0]

nhk_articles = read_json_file('nhk-articles')
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

pca = PCA(n_components=2)
pca.fit(features)
pa = pca.components_

lb_pa = []
# [
#     [[], []],
#     [[], []],
#     ...
# ]

for i in range(n_clusters):
    lb_pa.append([[], []])
for noun, x, y in zip(nouns, pa[0], pa[1]):
    lb_pa[cluster[noun]][0].append(x)
    lb_pa[cluster[noun]][1].append(y)

col = {0: 'b', 1: 'g', 2: 'r', 3: 'c', 4: 'm', 5: 'y', 6: 'k', 7: 'w'}
for i, e in enumerate(lb_pa):
    plot.scatter(e[0], e[1], c=col[i], alpha=0.7)

plot.title('features')

plot.show()
