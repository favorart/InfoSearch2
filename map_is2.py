#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64decode
from zlib import decompress

import pymorphy2
import codecs
import sys
import re


import zipimport
importer = zipimport.zipimporter('bs123.zip')
bs4 = importer.load_module('bs4')


morph = pymorphy2.MorphAnalyzer()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for line in sys.stdin:

    id, doc = line.strip().split()
    html = decompress(b64decode(doc))
    
    try:
        html = html.decode('utf8', 'ignore')
        bs = bs4.BeautifulSoup(html, 'html.parser')

        # kill all script and style elements
        for script in bs(["script", "style"]):
            script.extract() # rip it out
        text = bs.get_text()
    except:
        continue
    
    text = re.sub(ur'[^a-zа-яё0-9]', ur' ', text.lower())
    text = re.sub(ur'[ ]+', ur' ', text)

    words = text.split(u' ')
    for word in [ w for w in list(set(words)) if len(w) > 0 ]:
        norm = morph.parse(word)[0].normal_form
        print u'%s\t%s' % (norm, id) 

