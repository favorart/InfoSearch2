#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64decode
from zlib import decompress

import codecs
import sys
import re


import zipimport
importer = zipimport.zipimporter('bs123.zip')
bs4 = importer.load_module('bs4')


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for line in sys.stdin:

    id, doc = line.strip().split()
    html = decompress(b64decode(doc))
    html = html.decode('utf8', 'ignore')

    try:
        bs = bs4.BeautifulSoup(html, 'html.parser')
    except:
        continue
    text = bs.get_text()

    text = re.sub(ur'[^a-zа-яё0-9]', ur' ', text.lower())
    text = re.sub(ur'[ ]+', ur' ', text.lower())

    words = text.split(u' ')
    for word in [ w for w in list(set(words)) if len(w) > 2 ]:
        print u'%s\t%s' % (word, id) 

