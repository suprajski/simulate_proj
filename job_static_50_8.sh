#!/bin/bash
#BSUB -J static50x8
#BSUB -q hpc
#BSUB -n 8
#BSUB -W 00:30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -o outputs/static50x8_%J.out
#BSUB -e errors/static50x8_%J.err

cd ~/simulate_proj

echo "Task 6 comparison: static scheduling, 50 buildings, 8 workers"
echo "Start: $(date)"
time python parallel_static.py 50 8
echo "End: $(date)"
