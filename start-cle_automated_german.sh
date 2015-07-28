#!/bin/bash

CORPORA="../dependency-parsing-files/data/german"

MODELS="models"
PREDICTIONS="predictions"
EVALUATIONS="evaluations"

#train
python -u dependency-parser.py -train -i ${CORPORA}/train/tiger-2.2.train.conll06 -m ${MODELS}/$2 -e $1 $5 $6

#test
python -u dependency-parser.py -test -i ${CORPORA}/dev/tiger-2.2.dev.conll06 -m ${MODELS}/$2 -o ${PREDICTIONS}/$3".conll06"

# sentence based evaluation
python -u dependency-parser.py -ev -i ${PREDICTIONS}/$3".conll06" -g ${CORPORA}/dev/tiger-2.2.dev.conll06 -o ${EVALUATIONS}/$4"_sentence".txt

#evaluate
./eval07.pl -g ${CORPORA}/dev/tiger-2.2.dev.conll06 -s ${PREDICTIONS}/$3".conll06" >> ${EVALUATIONS}/$4".txt" 2>&1