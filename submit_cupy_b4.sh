#!/bin/bash
#BSUB -J cupy_pt4
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=12GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 30
#BSUB -o cupy_pt4_%J.out
#BSUB -e cupy_pt4_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
time python simulate_cupy_batch.py 3429 4571