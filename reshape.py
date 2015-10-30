#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


#  надо 2 файла
#   (word  offset  size) concat
#   bin_archived_(back_index)_concat-ed

with open('data', 'wb') as fdata:
    with open('index', 'w') as findex:
        for line in sys.stdif():
            word, data = line.strip(),split()

            pos = fdata.tell()
            findex.write(word + '\t' + str(pos) + '\t' + str(len(data)) + '\n')
            fdata.write(data)

