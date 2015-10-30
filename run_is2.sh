#!/bin/sh

# 1_10, 1_100, 1_1000
INPUT='/data/sites/povarenok.ru/1_1000/docs-000.txt'
# INPUT='/data/sites/povarenok.ru/all/docs-*.txt'

OUTPUT='infosearch2'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-D mapreduce.name='InfoSearch2' \
    -file map_is2.py red_is2.py fib_archive.py s9_archive.py bs123.zip \
    -mapper map_is2.py \
    -reducer red_is2.py \
	-numReduceTasks 1 \
    -input ${INPUT} \
    -output ${OUTPUT}

