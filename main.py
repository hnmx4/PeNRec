# -*- coding:utf-8 -*-

import common
import modeling

from gensim.models import word2vec
from os import listdir
from os.path import dirname, abspath


files = listdir(abspath(dirname(__file__)))
if 'word2vec.model' in files:
    model = word2vec.Word2Vec.load('word2vec.model')
else:
    model = modeling.create_word2vec_model()

vocab = model.vocab
words = vocab.keys()
