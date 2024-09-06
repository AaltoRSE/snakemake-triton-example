# Using Snakemake on Aalto Triton: Multiple Input Files

In this example Snakemake workflow, we run a pipeline of two computational steps. The first step loops over multiple input data files and processes them in parallel. The subsequent second step collects the processing results and combines them.

The workflow can be cloned and run on the [Aalto Triton](https://scicomp.aalto.fi/triton/) cluster following the [instructions below](#how-to-adapt-the-project-for-your-own-workflow).

You can use it as a [starting point for your own workflow](#how-to-adapt-the-project-for-your-own-workflow).

## Setup and Run Snakemake on Aalto Triton

Instructions to setup and run Snakemake on Aalto Triton.

### Setup

First, [connect to Triton using SSH](https://scicomp.aalto.fi/triton/tut/connecting/#connecting-via-ssh).

Change directory to your work directory 

```bash
cd $WRKDIR
```

Clone this repository and change directory

```bash
git clone https://github.com/AaltoRSE/snakemake-triton-example.git
cd snakemake-triton-example/multiple-input-files
```

Load `mamba` tool from a module and check that it works by printing its version number

```bash
module load mamba
mamba --version
```

Use `mamba` to create a conda environment containing Snakemake and the Slurm executor plugin

```bash
mamba env create --file snakemake.yml --prefix env/
```

### Run

Submit the Slurm job which starts Snakemake with

```bash
sbatch snakemake_slurm.sh
```

The batch script `snakemake_slurm.sh` requests resources to run Snakemake itself. 

We start Snakemake via a batch script so that it runs non-interactively and we are free to close our connection to Triton while we are waiting for the actual workflow computations to finish.  

The contents of the batch script:

```
#!/bin/bash
#SBATCH --job-name=snakemake_slurm
#SBATCH --time=01:00:00            # Runtime needs to be longer than the time it takes to complete the workflow. Modify accordingly!
#SBATCH --cpus-per-task=2          # Generally enough CPUs to run Snakemake. No need to modify.
#SBATCH --mem=2G                   # Generally enough RAM to run Snakemake. Modify if Snakemake process runs out of memory.
#SBATCH --output=snakemake_slurm-%j.out
#SBATCH --error=snakemake_slurm-%j.err

module load mamba
source activate env/
snakemake --snakefile workflow/Snakefile --profile profiles/slurm/ --software-deployment-method conda --conda-frontend mamba --cores 2
```

Here's a breakdown of the Snakemake command (the final line):

1. `--snakefile workflow/Snakefile`

    Explicitly state which Snakefile to run. 

    If omitted, Snakemake will try to find a Snakefile in the project root folder or under the `workflow/` folder.

    Check `workflow/Snakefile` for details of the workflow logic.

2. `--profile profiles/slurm/`

    Explicitly state the folder from which Snakemake looks for the `config.yaml` file. 

    The config.yaml defines the cluster resources to request for rules in the Snakefile (cluster partition, number of CPUs and GPUs, RAM, runtime).

    Check `profiles/slurm/config.yaml` for details. 

3. `--software-deployment-method conda`

    Tell Snakemake to create and use the rule-specific conda environments defined in the Snakefile.

4. `--conda-frontend mamba` 

    Use `mamba` instead of `conda`.

5. `--cores 2`

    Tell Snakemake to use two CPUs to run itself.

The intermediate and final result files will be written to the project root folder under `results/`.


## How to adapt the project for your own workflow

In order to adapt the project to your own workflow, do the following:

1. Replace the data and scripts in folders `resources/` and `workflow/scripts` with your own, respectively.
2. Replace/modify the workflow in `workflow/Snakefile` with your own.
3. Add/modify the requested computational resources for the Snakefile jobs (rules) to the profile file in `profiles/slurm/config.yaml`.
4. Increase the runtime value in the batch script `snakemake_slurm.sh` so that it is longer than the time it takes to complete the workflow. (Start e.g. with 12 hours and increase if necessary.)



## Setup and Run Snakemake locally

Finally, it is often convenient to develop the workflow locally on your own laptop/desktop computer before moving onto Triton to run actual computation-intensive experiments.

To run the workflow locally, first clone the repository
```
git clone git@github.com:AaltoRSE/snakemake-triton-example.git
cd snakemake-triton-example/multiple-input-files
```

Create the conda environment and activate it

```
mamba env create --file snakemake.yml --prefix env/
mamba activate env/
```

Then, run Snakemake with 

```
snakemake --snakefile workflow/Snakefile --software-deployment-method conda --conda-frontend mamba --cores 1
```

Since we now omitted the `--profile` option which defined the Slurm resource configuration, all the computations will be run locally instead.



