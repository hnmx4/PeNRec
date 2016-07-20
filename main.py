# -*- coding:utf-8 -*-

import modeling
import json
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

kmeans_model = KMeans(n_clusters=8, random_state=10).fit(features)

labels = kmeans_model.labels_

for label, noun in zip(labels, nouns):
    print(label, noun)
