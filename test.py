#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymorphy2
import codecs
import sys
import re

from InfoSearch2 import BooleanSearch
from reshape import reshape


if __name__ == '__main__':

    bin_name = sys.argv[2] if len(sys.argv) > 2 else './data/backward.bin'
    ndx_name = sys.argv[3] if len(sys.argv) > 3 else './data/index.txt'
    url_name = sys.argv[4] if len(sys.argv) > 4 else 'C:\\data\\povarenok.ru\\all\\urls.txt'
    mrk_name = sys.argv[5] if len(sys.argv) > 5 else 'C:\\data\\povarenok.ru\\all\\povarenok1000.tsv'

    urls = []
    with open(url_name, 'r') as f_urls:
        for line in f_urls.readlines():
            id, url = line.strip().split()
            url = re.sub(r'(?:^https?://(www\.)?povarenok\.ru/)|(?:/?\r?\n?$)', '', url)
            urls.append(url)

    found = 0
    morph = pymorphy2.MorphAnalyzer()
    bs = BooleanSearch(ndx_name, bin_name)
    with codecs.open(mrk_name, 'r', encoding='utf-8') as f_marks:
        for i,line in enumerate(f_marks.readlines()[2:]):
            splt = line.split('\t')
            if len(splt) == 2:
                query, mark_url = splt
                mark_url = re.sub(r'(?:^https?://(www\.)?povarenok\.ru/)|(?:/?\r?\n?$)', '', mark_url)

                query_words = [ morph.parse(w)[0].normal_form for w in query.split() ]

                query_words = ' AND '.join([ w for w in query_words if len(w) > 2 ]).split()
                answer = bs.search(query_words)

                # print "\n".join([ urls[i] for i in answer ])
                # print "\t", mark_url

                m = re.match("|".join([ urls[i] for i in answer ]), mark_url)
                if m is not None:
                    print (mark_url + ' ' + url)
                    found += 1
                # else: print '\t' + query.encode('cp866', 'ignore')
    print found

