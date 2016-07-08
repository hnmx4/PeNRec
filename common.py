# -*- coding:utf-8 -*-

import dotenv

from os.path import join, dirname, abspath


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)


def regist_emotion_dict(c_emotion_dict):
    with open(join(abspath(dirname(__file__)), 'wago.121808.pn')) as f:
        for l in f.readlines():
            l = l.split('\t')
            c_emotion_dict.insert({
                'word': l[1].replace(' ', '').replace('\n', ''),
                'value': 1 if l[0].startswith('ポジ') else -1
            })
    with open(join(abspath(dirname(__file__)), 'pn.csv.m3.120408.trim')) as f:
        for l in f.readlines():
            l = l.split('\t')
            table = {'n': -1, 'e': 0, 'p': 1}
            if l[1] in table:
                c_emotion_dict.insert({
                    'word': l[0],
                    'value': table[l[1]]
                })
