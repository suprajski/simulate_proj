#!/bin/bash
#BSUB -J dynamic50x8
#BSUB -q hpc
#BSUB -n 8
#BSUB -W 00:30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -o outputs/dynamic50x8_%J.out
#BSUB -e errors/dynamic50x8_%J.err

cd ~/simulate_proj

echo "Task 6 comparison: dynamic scheduling, 50 buildings, 8 workers"
echo "Start: $(date)"
time python parallel_dynamic.py 50 8
echo "End: $(date)"
