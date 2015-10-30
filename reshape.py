#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64decode
import codecs
import sys
import os

from s9_archive import Simple9Archiver
from fib_archive import FibonacciArchiver

if   (sys.argv[1] == 'f'): a = True
elif (sys.argv[1] == 's'): a = False
else: raise ValueError

if a: fib = FibonacciArchiver(199460)  # all_docs=199456
else:  s9 =   Simple9Archiver()

#  2 files:
#     + (word  offset  size) concat
#     + bin_archived_(back_index)_concat-ed

if not os.path.exists('data'):
    os.makedirs('data')

with open('./data/backward.bin', 'wb') as fdata:
    with codecs.open('./data/index.txt', 'w', encoding='utf-8') as findex:
        for line in codecs.open(sys.argv[1] if len(sys.argv) > 1 else './data/reduced.txt', 'r', encoding='utf-8'):
            word, coded = line.strip().split()

            data = b64decode(coded)
            if check:
                if a: print fib.decode(data)
                else: print  s9.decode(data)

            print >>findex, u'%s\t%d\t%d' % (word, fdata.tell(), len(data))
            fdata.write(data)

