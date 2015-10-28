This package implements genetic algorithms and Q-Learning for the 
traffic assignement problem. 

The main class is the Experiment and is implemented in the file with the same name.
If you wish to modify the cost function, this is the file that must be modified.

It is best to use execute the experiments using pypy instead of python due to its
better performance.

This package depends on pyevolve

the file intructions.txt provides and example and instructions to run experiments.

The directory structure is as follows:

helper_scripts/ some python scripts for processing the results e.g. generating plots
			they are somewhat crude
networks/ 	where information related to networks are stored e.g. network graph,
			od matrix, link capacity.
Experiment.py 	main file. Implements the Experiment class which is used for executing
			experiments
GA.py, QL.py 	implements the GA and QL part. Used by Experiment.py

KSP.py 		implements k-shortest path algorithm. 
			By Gabriel de Oliveira Ramos <goramos@inf.ufrgs.br>
runExperiment.py provides an example of usage

instructions.txt instructions of use
