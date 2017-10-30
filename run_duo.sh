#!/usr/bin/env bash

set -e

mkdir -p output

for N in {2..15}; do
    for l2wt in {0.01,0.1,1.0}; do
        for h_reg in {0.001,0.01,0.1,1.0}; do
            # 10GB ~ 24 Jobs per machine?
            sbatch --mem=65000 -o output/stdout_N${N}.h_reg-${h_reg}.l2wt-${l2wt}.txt ./run_duo_job.sh $N $l2wt $h_reg
        done
    done
done
