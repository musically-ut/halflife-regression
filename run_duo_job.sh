#!/bin/bash

set -e
mkdir -p output
source conda.sh

N=$1
l2wt=$2
h_reg=$3

python experiment.py /NL/spaced-repetition/work/experiments/data/raw/duolingo_reduced.csv -m "hlr-pw" -bins "duo_time_quantiles/${N}_bins" -h_reg ${h_reg} -l2wt ${l2wt}
