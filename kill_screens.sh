#!/bin/bash

COUNTER=0
MAXIMUM=6

while [ "$COUNTER" -le "$MAXIMUM" ]; do

    screen -S "cle_"$COUNTER -X quit

    let COUNTER=COUNTER+1

done





