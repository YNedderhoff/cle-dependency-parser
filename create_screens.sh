#!/bin/bash

screen -dmS "cle_1" ./start-cle_automated.sh 1 m_e-1 p_e-1 e_e-1
screen -dmS "cle_2" ./start-cle_automated.sh 10 m_e-10 p_e-10 e_e-10
screen -dmS "cle_3" ./start-cle_automated.sh 10 m_e-10_da p_e-10_da e_e-10_da -decrease-alpha
screen -dmS "cle_4" ./start-cle_automated.sh 10 m_e-10_ss p_e-10_ss e_e-10_ss -shuffle-sentences
screen -dmS "cle_5" ./start-cle_automated.sh 10 m_e-10_da_ss p_e-10_da_ss e_e-10_da_ss -decrease-alpha -shuffle-sentences
