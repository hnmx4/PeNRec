# -*- coding:utf-8 -*-

import dotenv
import json
import codecs

from os.path import join, dirname, abspath


def denv(envkey):
    return dotenv.get_key(join(dirname(__file__), '.env'), envkey)


def read_json_file(filename):
    f = open(join(abspath(dirname(__file__)), filename + '.json'), 'r')
    ret = json.loads(f.read())
    f.close()
    return ret


def write_json_file(data, filename):
    f = codecs.open(join(abspath(dirname(__file__)), filename + '.json'), 'w', 'utf-8')
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()


def write_file(data, filename):
    f = open(join(abspath(dirname(__file__)), filename), 'w')
    f.write(data)
    f.close()


def register_noun(c):
    with open(join(abspath(dirname(__file__)), 'pn.csv.m3.120408.trim')) as f:
        for l in f.readlines():
            l = l.split('\t')
            table = {'n': -1, 'e': 0, 'p': 1}
            if l[1] in table:
                c.insert({
                    'word': l[0],
                    'value': table[l[1]]
                })


def register_declinable_word(c):
    with open(join(abspath(dirname(__file__)), 'wago.121808.pn')) as f:
        for l in f.readlines():
            l = l.replace('\t\n', '').replace('\n', '').split('\t')
            if len(l) > 1:
                l[1] = l[1].split()
                c.insert({
                    'index': l[1][0],
                    'word': l[1],
                    'value': 1 if l[0].startswith('ポジ') else -1
                })
