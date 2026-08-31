from shutil import copyfile
import os

filename = "t207mev"
email = "gabrieli.trivelato@cnpem.br"

queue = "sequana_cpu" 
nodes = 1
tasks_per_node = 24
tasks = int(nodes*tasks_per_node)

for i in range(tasks):
	copyfile(f"{filename}.inp", f"{filename}_{i+1:02d}.inp")

	f = open(f"{filename}_{i+1:02d}.inp","r")
	lines = f.readlines()
	f.close()
	
	with open(f"{filename}_{i+1:02d}.inp","w",newline='') as newfile:
		for line in lines:
			if not any(bad_word in line for bad_word in ['RANDOMIZ']):
				newfile.write(line)
			else:
				newfile.write(f"RANDOMIZ          1.     {i+1:4.0f}.\n")

sh = open(f"{filename}.sh","w",newline='')

sh.write(f"#!/bin/bash\n")
sh.write(f"#SBATCH --nodes={nodes}                      #Numero de Nos\n")
sh.write(f"#SBATCH --ntasks-per-node={tasks_per_node}            #Numero de tarefas por No\n")
sh.write(f"#SBATCH --ntasks={tasks}                     #Numero total de tarefas\n")
sh.write(f"#SBATCH -p {queue}                    #Fila (partition) a ser utilizada\n")
sh.write(f"#SBATCH -J {filename}                  #Nome job\n")
sh.write(f"#SBATCH --exclusive                    #Utilização exclusiva dos nos durante a execucao do job\n")
sh.write(f"#SBATCH --mail-type=ALL\n")
sh.write(f"#SBATCH --mail-user={email}\n")
sh.write(f"#SBATCH --time=96:00:00             #Altera o tempo limite")   # Dependendo da simulação e fila, é preciso mudar isso
sh.write(f"\n")
sh.write(f"#Exibe os nos alocados para o Job\n")
sh.write(f"echo $SLURM_JOB_NODELIST\n")
sh.write(f"nodeset -e $SLURM_JOB_NODELIST\n")
sh.write(f"\n")
sh.write(f"cd $SLURM_SUBMIT_DIR\n")
sh.write(f"\n")
sh.write(f"export FLUPRO=/petrobr/app_sequana/fluka/4.5.2-gfort8\n")
sh.write(f"module load fluka/4.5.2")
sh.write(f"\n")

for node in range(nodes):
	sh.write(f"srun --resv-ports --nodes 1 --ntasks=1 -c 24 bash \"${{PWD}}/exec_fluka_N{node+1:02d}.sh\" &\n")
	exe = open(f"exec_fluka_N{node+1:02d}.sh","w",newline='')
	exe.write(f"#!/bin/bash\n")
	exe.write(f"\n")
	for i in range(tasks_per_node):
		j = i + tasks_per_node*node
		exe.write(f"$FLUPRO/bin/rfluka -M 5 \"${{PWD}}/{filename}_{j+1:02d}.inp\" &\n")
	exe.write(f"wait\n")
sh.write(f"wait\n")