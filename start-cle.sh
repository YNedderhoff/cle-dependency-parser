#!/bin/bash


#CORPORA="../dependency-parsing-files/data/english"
CORPORA="../dependency-parsing-files/data/german"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="evaluations"

#train (on small set)
#python -u dependency-parser.py -train -i $CORPORA/train/wsj_train.first-5k.conll06 -m model -e 20

#train
#python -u dependency-parser.py -train -i ../dependency-parsing-files/data/english/train/wsj_train.conll06 -m $MODELS/m_e-10_da_ss -e 2 -decrease-alpha -shuffle-sentences

#test
#python -u dependency-parser.py -test -i $CORPORA/dev/wsj_dev_without_head.conll06 -m model -o predicted.conll06
#python -u dependency-parser.py -test -i $CORPORA/dev/wsj_dev_without_head.conll06 -m $MODELS/english/m_e-1 -o $PREDICTIONS/english/predicted_e-1.conll06

#python -u dependency-parser.py -ev -i predicted.conll06 -g $CORPORA/dev/wsj_dev.conll06 -o evaluation_sentence.txt
python -u dependency-parser.py -ev -i $PREDICTIONS/german/p_e-1.conll06 -g $CORPORA/dev/tiger-2.2.dev.conll06 -o $EVALUATIONS/german/evaluation_sentence_e-1.txt


#evwaluate
#./eval07.pl -g $CORPORA/dev/wsj_dev.conll06 -s  predicted.conll06 >> evaluation.txt 2>&1
./eval07.pl -g $CORPORA/dev/tiger-2.2.dev.conll06 -s  $PREDICTIONS/german/p_e-1.conll06 >> $EVALUATIONS/german/evaluation_e-1.txt 2>&1

