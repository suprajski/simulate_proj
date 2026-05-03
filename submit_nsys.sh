#!/bin/bash
#BSUB -J sim_nsys
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 15
#BSUB -o nsys_%J.out
#BSUB -e nsys_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

echo "Profiling SLOW CuPy Run..."
nsys profile --stats=true python simulate_cupy_slow.py 5