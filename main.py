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


# PCA
pca = PCA(n_components=2)
pc_features = pca.fit_transform(features)


# K-means
kmeans = KMeans(n_clusters=6, random_state=10).fit(pc_features)


labels = kmeans.labels_
cluster = {noun: label for label, noun in zip(labels, nouns)}


# calculate most frequent cluster in twitter-noun
twitter_nouns = read_json_file('twitter-nouns')
count = {label: 0 for label in labels}
for noun in twitter_nouns:
    count[cluster[noun]] += 1

most_interest_label = sorted(count.items(), key=lambda x: x[1], reverse=True)[0][0]


# match nhk-news with user's interest
nhk_articles = read_json_file('nhk-articles')
matching_articles = {}

for k, v in nhk_articles.items():
    count = {label: 0 for label in labels}
    deno = 0
    for word in v['nouns']:
        count[cluster[word]] += 1
        deno += 1
    most = sorted(count.items(), key=lambda x: x[1], reverse=True)[0]
    v['label'] = most[0]
    v['rate'] = most[1] / deno
    nhk_articles[k] = v

    if v['label'] == most_interest_label:
        matching_articles[k] = v

match_articles = sorted(matching_articles.items(), key=lambda x: x[1]['rate'], reverse=True)
for k, v in match_articles[:16]:
    print(k, v['url'], v['rate'])


# draw graph
lb_pc = []
# [
#     [[], []],
#     [[], []],
#     ...
# ]
for i in range(len(kmeans.cluster_centers_)):
    lb_pc.append([[], []])
for noun, f in zip(nouns, pc_features):
    lb_pc[cluster[noun]][0].append(f[0])
    lb_pc[cluster[noun]][1].append(f[1])

col = {0: 'b', 1: 'g', 2: 'r', 3: 'c', 4: 'm', 5: 'y', 6: 'k', 7: 'w'}
for i, e in enumerate(lb_pc):
    plot.scatter(e[0], e[1], c=col[i], alpha=0.7)
    center = kmeans.cluster_centers_[i]
    for x, y in zip(e[0], e[1]):
        plot.scatter([center[0], x], [center[1], y], c=col[i])

plot.title('features')

plot.show()
