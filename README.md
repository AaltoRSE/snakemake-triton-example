# Using Snakemake on Aalto Triton

[Snakemake](https://snakemake.readthedocs.io/en/stable/) is a workflow management tool used to create reproducible and scalable data processing workflows.

This repo contains a small example project which can be cloned and run on the [Aalto Triton](https://scicomp.aalto.fi/triton/) cluster.

The project

1. follows the [recommended Snakemake project structure](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html),
2. uses conda environments for [integrated package management](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html),
3. uses the [Slurm executor plugin](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html) to submit the workflow steps as cluster jobs,
4. uses a [Snakefile](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html) for workflow logic and a [profile file](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles) for Slurm resource management, decoupling the two configurations.

You can use it as a starting point for your own workflow. 

## Setup and Run Snakemake on Aalto Triton

First, [connect to Triton using SSH](https://scicomp.aalto.fi/triton/tut/connecting/#connecting-via-ssh).

Change directory to your work directory 

```bash
cd $WRKDIR
```

Clone this repository and change directory

```bash
git clone git@github.com:AaltoRSE/snakemake-triton-example.git
cd snakemake-triton-example
```

Load `mamba` tool from a module and check that it works by printing its version number

```bash
module load mamba
mamba --version
```

Create a conda environment containing Snakemake and the Slurm executor plugin

```bash
mamba env create --file snakemake.yml --prefix env/
```

Submit the Snakemake workflow

```bash
sbatch snakemake_slurm.sh
```

The sbatch script `snakemake_slurm.sh` requests resources to run Snakemake itself:

```
#!/bin/bash
#SBATCH --job-name=snakemake_slurm
#SBATCH --time=01:00:00            # Runtime needs to be longer than the time it takes to complete the workflow, modify accordingly                            
#SBATCH --cpus-per-task=2          
#SBATCH --mem-per-cpu=2G
#SBATCH --output=snakemake_slurm-%j.out
#SBATCH --error=snakemake_slurm-%j.err

module load mamba
source activate env/
snakemake --snakefile workflow/Snakefile --profile profiles/slurm/ --software-deployment-method conda --conda-frontend mamba --cores 2
```

Note that the requested runtime needs to be longer than the time it takes to complete the workflow. In this example, we have set it to 1 hour. For real life use cases, you may need to set it much higher, e.g. a few days.

Meanwhile, 2 CPUs and 2G RAM is generally enough to run the Snakemake.

Here's a breakdown of the Snakemake command:

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


## Develop Snakemake workflow locally

It is often convenient to develop the workflow locally on your own laptop/desktop computer before moving onto Triton to run actual computation-intensive experiments.

To run the workflow locally, first clone the repository
```
git clone git@github.com:AaltoRSE/snakemake-triton-example.git
cd snakemake-triton-example
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

Since we now omitted the `--profile` option, all the computation will be run locally.

