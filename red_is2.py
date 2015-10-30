#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
from operator import itemgetter

from fib_archive import FibonacciArchiver
from s9_archive import Simple9Archiver

import codecs
import sys


if 1: fib = FibonacciArchiver(199460)  # all_docs=199456
else: spl = Simple9Archiver()

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for word, group in groupby((line.strip().split(u'\t', 1) for line in sys.stdin), itemgetter(0)):
    if 1: coded = fib.code([ int(g[1]) for g in group ])
    else: coded = spl.code([ int(g[1]) for g in group ])
    print u'%s\t%s' % (word, coded)

# получается: "слово - архив"  --- max_id штук
