#!/bin/bash
#BSUB -J baseline20
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 00:30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -o outputs/baseline20_%J.out
#BSUB -e errors/baseline20_%J.err

cd ~/simulate_proj

echo "Task 2: baseline timing, 20 buildings"
echo "Start: $(date)"
time python simulate.py 20
echo "End: $(date)"
