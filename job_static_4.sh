#!/bin/bash
#BSUB -J static4
#BSUB -q hpc
#BSUB -n 4
#BSUB -W 00:30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -o outputs/static4_%J.out
#BSUB -e errors/static4_%J.err

cd ~/simulate_proj

echo "Task 5: static scheduling, 10 buildings, 1 worker"
echo "Start: $(date)"
time python parallel_static.py 10 4
echo "End: $(date)"
