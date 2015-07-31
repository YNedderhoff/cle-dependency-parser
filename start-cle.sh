#!/bin/bash


CORPORA="../dependency-parsing-files/data/english"
#CORPORA="../dependency-parsing-files/data/german"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="evaluations"

#train (on small set)
python -u dependency-parser.py -train -i $CORPORA/train/wsj_train.first-5k.conll06 -m model -e 1

#train
#python -u dependency-parser.py -train -i .$CORPORA//train/wsj_train.conll06 -m $MODELS/m_e-10_da_ss -e 2 -decrease-alpha -shuffle-sentences

#test
python -u dependency-parser.py -test -i $CORPORA/dev/wsj_dev_without_head.conll06 -m model -o predicted.conll06

#evaluate sentence based
python -u dependency-parser.py -ev -i predicted.conll06 -g $CORPORA/dev/wsj_dev.conll06 -o evaluation_sentence.txt

#evaluate arc based
./eval07.pl -g $CORPORA/dev/wsj_dev.conll06 -s  predicted.conll06 >> evaluation.txt 2>&1