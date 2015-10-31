#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode
from itertools import groupby
from operator import itemgetter
import codecs
import sys

import zipimport
importer = zipimport.zipimporter('bs123.zip')
fib_archive = importer.load_module('fib_archive')
s9_archive = importer.load_module('s9_archive')


if   (sys.argv[1] == 'f'): a = True
elif (sys.argv[1] == 's'): a = False
else: raise ValueError

if a: fib = fib_archive.FibonacciArchiver(199460)  # all_docs=199456
else: spl =  s9_archive.Simple9Archiver()

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for word, group in groupby((line.strip().split('\t', 1) for line in sys.stdin), itemgetter(0)):
    ids = [ int(g[1]) for g in group ]
    ids.sort()

    if a: coded = fib.code(ids)
    else: coded = spl.code(ids)
    print u'%s\t%s' % (word, b64encode(coded))

