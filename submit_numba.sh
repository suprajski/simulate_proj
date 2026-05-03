#!/bin/bash
#BSUB -J sim_numba
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 15
#BSUB -o numba_%J.out
#BSUB -e numba_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

echo "Starting Numba Run (N=20)..."
time python simulate_numba.py 20
