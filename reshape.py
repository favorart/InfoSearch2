# -*- coding: utf-8 -*-

from base64 import b64decode
import codecs
import sys
import os


if   (sys.argv[1] == 'f'):
    import fib_archive
    archiver = fib_archive.FibonacciArchiver ( max(199460, 564550) ) # all_docs= povarenok:199456, lenta:564548
elif (sys.argv[1] == 's'):
    import  s9_archive
    archiver =  s9_archive.Simple9Archiver   ()
else: raise ValueError


def reshape(dat_name, ndx_name, bin_name, verbose=False):
    """ Create the two files:

        (word  offset  size)_concat-ed
        (backward_index)_bin_archived_concat-ed
    """
    with open(bin_name, 'wb') as f_bin:
        with codecs.open(ndx_name, 'w', encoding='utf-8') as f_index:

            sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
            # sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
            # sys.stdin codecs.open('.\data\mapped.txt', 'r', encoding='utf-8')
            # for word, group in groupby((line.strip().split('\t', 1) for line in sys.stdin), itemgetter(0)):
            for line in sys.stdin:
            # with codecs.open(dat_name, 'r', encoding='utf-8') as f_data:
                # for line in f_data:

                splt = line.strip().split()
                if len(splt) > 1:
                    word, coded = splt

                    data = b64decode(coded)
                    if verbose: print archiver.decode(data)

                    print >>f_index, u'%s\t%d\t%d' % (word, f_bin.tell(), len(data))
                    f_bin.write(data)


if __name__ == '__main__':

    if not os.path.exists('data'):
        os.makedirs('data')

    dat_name = sys.argv[2] if len(sys.argv) > 2 else './data/povarenok1000_s_reduced.txt' # 'povarenok' # 'reduced.txt'
    bin_name = sys.argv[3] if len(sys.argv) > 3 else './data/backward.bin'
    ndx_name = sys.argv[4] if len(sys.argv) > 4 else './data/index.txt'

    reshape(dat_name, ndx_name, bin_name) # , True)

