# -*- coding: utf-8 -*-

from base64 import b64encode
from itertools import groupby
from operator import itemgetter
import codecs
import sys

import zipimport
importer = zipimport.zipimporter('bs123.zip')


if   (sys.argv[1] == 'f'):
    module = importer.load_module('fib_archive')
    archiver = module.FibonacciArchiver( max(199460, 564550) ) # all_docs= povarenok:199456, lenta:564548
elif (sys.argv[1] == 's'):
    module = importer.load_module('s9_archive')
    archiver = module.Simple9Archiver()
else: raise ValueError


sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
# sys.stdin codecs.open('.\data\mapped.txt', 'r', encoding='utf-8')
for word, group in groupby((line.strip().split('\t', 1) for line in sys.stdin), itemgetter(0)):
    
    ids = list(set([ int(g[1]) for g in group if len(g) == 2 ]))
    ids.sort()

    for i in xrange(len(ids) - 1, 0, -1):
        ids[i] -= ids[i-1]

    coded = archiver.code(ids)
    print u'%s\t%s' % (word, b64encode(coded))
    del coded
    del ids

