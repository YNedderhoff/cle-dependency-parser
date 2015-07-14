#!/bin/bash

python -u cle.py -i ../dependency-parsing-files/data/english/train/wsj_train.first-5k.conll06 -o out.txt
#python cle.py -i wsj_train.first-5k.conll06 -o featurebeispiel.txt

#echo 'Lenght of diff input output:'
#diff ../dependency-parsing-files/data/english/train/wsj_train.first-5k.conll06 out.txt | wc -l
