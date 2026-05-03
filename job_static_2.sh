#!/bin/bash
#BSUB -J static2
#BSUB -q hpc
#BSUB -n 2
#BSUB -W 00:30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -o outputs/static2_%J.out
#BSUB -e errors/static2_%J.err

cd ~/simulate_proj

echo "Task 5: static scheduling, 10 buildings, 1 worker"
echo "Start: $(date)"
time python parallel_static.py 10 2
echo "End: $(date)"
