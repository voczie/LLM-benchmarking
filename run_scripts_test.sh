#!/bin/bash
#---------------Script SBATCH - NLHPC ----------------
#SBATCH -J LLM_simple
#SBATCH -p v100
#SBATCH --gres=gpu:1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem-per-cpu=3789
#SBATCH --mail-user=mbarborgess@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o LLM_simple_%j.err.out
#SBATCH -e LLM_simple_%j.err.out

#-----------------Toolchain---------------------------
# ----------------Modulos----------------------------
# ----------------Comando--------------------------
python3 test_all_models_with_instruction_prompt.py
python3 test_all_models_no_instruction_prompt.py