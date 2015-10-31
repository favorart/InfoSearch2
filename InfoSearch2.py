#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import numpy as np

import fib_archive
import s9_archive

"""
    Используя Hadoop MapReduce создать бинарный индекс сайта, и реализовать поиск по введенному запросу.

    Формат запроса:
        слово1 AND слово2 AND NOT слово3 OR слово4 (слово1 && слово2 && !слово3 || слово4)

    Формат выдачи:
        url1
        url2
        ...

    Система должна уметь сжимать индекс минимум 2-мя способами: VarByte или Фибоначчи (на выбор), и Simple9.

    Файлы в этих каталогах:
        docs-*.txt   -  строки вида docid base64(deflate(HTML))
        urls.txt     -  URL-ы соответствующие docid

    Соответственно алгоритм такой:

        Используя hadoop streaming парсим исходные файлы любого понравившегося сайта.
        Выходом задачи должен быть сжатый индекс по каждому терму.
        Этот индекс копируем на локальную машину и строим словарь термов.
        Делаем булев поиск по бинарному индексу

    4 программы:
        mapper и reducer для парсинга и сжатия индекса
        утилита, использующая вывод mapreduce-задачи, строящая финальный индекс и словарь к нему
        утилита поиска работающая со сжатым индексом
"""


# all, 1_10, 1_100
docs_file = 'C:\\Users\\MainUser\\Downloads\\Cloud.mail\\povarenok.ru\\1_1000\\docs-000.txt'
urls_file = 'C:\\Users\\MainUser\\Downloads\\Cloud.mail\\povarenok.ru\\1_1000\\urls.txt'

if __name__ == '__main__':
    
    if    sys.argv[1] == 's':
        decoder =  s9_archive.Simple9Archiver()
    elif  sys.argv[1] == 'f':
        decoder = fib_archive.FibonacciArchiver(199460) # all_docs=199456
    else:  raise ValueError

    print 'query=',
    if sys.platform.startswith('win'):
        query = unicode(sys.stdin.readline(), 'cp866')
    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        query = unicode( sys.stdin.readline() )

    query_words = query.split()

    w_offsets = {}
    index_name = sys.argv[2] if len(sys.argv) > 2 else './data/index.txt'
    with codecs.open(index_name, 'r', encoding='utf-8') as f_index:
        for line in f_index.readlines():
            word, offset, size = line.strip().split()
            w_offsets[word] = (offset, size)

    answer = set()
    oper = ''
    backward_name = sys.argv[3] if len(sys.argv) > 3 else './data/backward.bin'
    with open(backward_name, 'rb') as f_backward:
        for q in query_words:
            if   q == 'AND' or q == 'OR'or q == 'NOT':
                oper = q
            else:
                offset, size = w_offsets[q]
                offset, size = int(offset), int(size)

                f_backward.seek(offset)
                coded = f_backward.read(size)
                decoded = set(decoder.decode(coded))
                # print decoded

                if      not answer : answer  = decoded
                elif oper == 'AND' : answer &= decoded
                elif oper == 'OR'  : answer |= decoded
                elif oper == 'NOT' : answer -= decoded
                else: break

    urls = []
    urls_name = sys.argv[4] if len(sys.argv) > 4 else urls_file
    with open(urls_name, 'r') as f_urls:
        for line in f_urls.readlines():
            id, url = line.strip().split()
            urls.append(url)

    # print answer
    print '\n', '\n'.join([ urls[i] for i in answer ]), '\n'
