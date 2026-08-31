#!/bin/bash
#SBATCH --nodes=1                      #Numero de Nos
#SBATCH --ntasks-per-node=24            #Numero de tarefas por No
#SBATCH --ntasks=24                     #Numero total de tarefas
#SBATCH -p sequana_cpu                    #Fila (partition) a ser utilizada
#SBATCH -J t207mev                  #Nome job
#SBATCH --exclusive                    #Utilização exclusiva dos nos durante a execucao do job
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gabrieli.trivelato@cnpem.br
#SBATCH --time=96:00:00             #Altera o tempo limite
#Exibe os nos alocados para o Job
echo $SLURM_JOB_NODELIST
nodeset -e $SLURM_JOB_NODELIST

cd $SLURM_SUBMIT_DIR

export FLUPRO=/petrobr/app_sequana/fluka/4.5.2-gfort8
module load fluka/4.5.2
srun --resv-ports --nodes 1 --ntasks=1 -c 24 bash "${PWD}/exec_fluka_N01.sh" &
wait
