#!/bin/bash

#train (on small set)
#python -u dependency-parser.py -train -i ../dependency-parsing-files/data/english/train/wsj_train.first-5k.conll06 -m model -e 2 -decrease-alpha

#train
python -u dependency-parser.py -train -i ../dependency-parsing-files/data/english/train/wsj_train.conll06 -m model_decrease-alpha -e 10 -decrease-alpha

#test
python -u dependency-parser.py -test -i ../dependency-parsing-files/data/english/dev/wsj_dev.conll06 -m model_decrease-alpha -o predicted_decrease-alpha.conll06

#python -u dependency-parser.py -test -i ../dependency-parsing-files/data/english/train/wsj_train.conll06 -m model -o predicted.col
#python dependency-parser.py -i wsj_train.first-5k.conll06 -o featurebeispiel.txt

#echo 'Lenght of diff input output:'
#diff ../dependency-parsing-files/data/english/train/wsj_train.first-5k.conll06 out.txt | wc -l
