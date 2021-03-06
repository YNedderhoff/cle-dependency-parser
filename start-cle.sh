#!/bin/bash


CORPORA="../dependency-parsing-files/data/english"
#CORPORA="../dependency-parsing-files/data/german"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="evaluations"

#train (on small set)
#python -u dependency-parser.py -train -i $CORPORA/train/wsj_train.first-5k.conll06 -m model -e 10

#train
python -u dependency-parser.py -train -i $CORPORA/train/wsj_train.conll06 -m $MODELS/model -e 2 -decrease-alpha

#test
python -u dependency-parser.py -test -i $CORPORA/dev/wsj_dev_without_head.conll06 -m model -o predicted.conll06

#evaluate sentence based
python -u dependency-parser.py -ev -i predicted.conll06 -g $CORPORA/dev/wsj_dev.conll06 -o evaluation.txt