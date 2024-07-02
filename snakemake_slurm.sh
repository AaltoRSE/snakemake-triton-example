#!/bin/bash
#SBATCH --job-name=snakemake_slurm
#SBATCH --time=01:00:00            # Runtime needs to be longer than the time it takes to complete the workflow. Modify accordingly!
#SBATCH --cpus-per-task=2          # Generally enough cpus to run Snakemake
#SBATCH --mem=2G                   # Generally enough RAM to run Snakemake
#SBATCH --output=snakemake_slurm-%j.out
#SBATCH --error=snakemake_slurm-%j.err

module load mamba
source activate env/
snakemake --snakefile workflow/Snakefile --profile profiles/slurm/ --software-deployment-method conda --conda-frontend mamba --cores 2
