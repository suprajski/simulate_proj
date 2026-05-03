#!/bin/bash
#BSUB -J cupy_pt2
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 30
#BSUB -o cupy_pt2_%J.out
#BSUB -e cupy_pt2_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
time python simulate_cupy_batch.py 1523 3046