#!/bin/bash

python -u dependency-parser.py -train -i ../dependency-parsing-files/data/english/train/wsj_train.conll06 -m model -e 10

python -u dependency-parser.py -test -i ../dependency-parsing-files/data/english/dev/wsj_dev.conll06 -m model -o predicted.col

#python -u dependency-parser.py -test -i ../dependency-parsing-files/data/english/train/wsj_train.conll06 -m model -o predicted.col
#python dependency-parser.py -i wsj_train.first-5k.conll06 -o featurebeispiel.txt

#echo 'Lenght of diff input output:'
#diff ../dependency-parsing-files/data/english/train/wsj_train.first-5k.conll06 out.txt | wc -l
