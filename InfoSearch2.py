# -*- coding: utf-8 -*-

import pymorphy2
import codecs
import sys

import fib_archive
import s9_archive

"""
    Используя Hadoop MapReduce создать бинарный индекс сайта, и реализовать поиск по введенному запросу.

    Формат запроса:
        слово1 AND слово2 AND NOT слово3 OR слово4

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


if    sys.argv[1] == 's':
    decoder =  s9_archive.Simple9Archiver()
elif  sys.argv[1] == 'f':
    decoder = fib_archive.FibonacciArchiver( max(199460, 564550) )
    # all_docs= povarenok:199456, lenta:564548
else:  raise ValueError


class BooleanSearch(object):
    """ """
    def __init__(self, ndx_name, bin_name):
        self.bin_name = bin_name
        self.ndx_name = ndx_name
        self.w_offsets = {}
        with codecs.open(ndx_name, 'r', encoding='utf-8') as f_index:
            for line in f_index.readlines():
                word, offset, size = line.strip().split()
                self.w_offsets[word] = (offset, size)

    def search(self, query_words):
        """ """
        answer = set()
        oper = ''
    
        with open(self.bin_name, 'rb') as f_backward:
            for q in query_words:
                if   q == 'AND' or q == 'OR'or q == 'NOT':
                    oper = q
                else:
                    try:
                    # if 1:
                        offset, size = self.w_offsets[q.lower()]
                        offset, size = int(offset), int(size)
                    except:
                        # print q.lower().encode('cp866', 'ignore')
                        continue

                    f_backward.seek(offset)
                    coded = f_backward.read(size)
                    decoded = decoder.decode(coded[-1:])

                    for i in xrange(1, len(decoded)):
                        decoded[i] += decoded[i-1]

                    # print decoded
                    decoded = set(decoded)

                    if      not answer : answer  = decoded
                    elif oper == 'AND' : answer &= decoded
                    elif oper == 'OR'  : answer |= decoded
                    elif oper == 'NOT' : answer -= decoded
                    else: break

        return list(answer)


if __name__ == '__main__':
    
    bin_name = sys.argv[2] if len(sys.argv) > 2 else './data/backward.bin'
    ndx_name = sys.argv[3] if len(sys.argv) > 3 else './data/index.txt'
    url_name = sys.argv[4] if len(sys.argv) > 4 else 'C:\\data\\povarenok.ru\\all\\urls.txt'

    print 'query=',
    if sys.platform.startswith('win'):
        query = unicode(sys.stdin.readline(), 'cp866')
    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        query = unicode( sys.stdin.readline() )

    morph = pymorphy2.MorphAnalyzer()
    bs = BooleanSearch(ndx_name,bin_name)

    query_words = [ morph.parse(w)[0].normal_form for w in query.split() ]
    query_words = [ w for w in query_words if len(w) >= 2 ]
    answer = bs.search(query_words)

    # print answer
    urls = []
    with open(url_name, 'r') as f_urls:
        for line in f_urls.readlines():
            id, url = line.strip().split()
            urls.append(url)

    print '\n', '\n'.join([ urls[i] for i in answer ]), '\n'

