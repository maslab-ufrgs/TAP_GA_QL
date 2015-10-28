# -*- coding: utf-8 -*-

from Experiment import Experiment  


###initialization. Here you setup the number of k shortest paths,
#files of the network, the group size and output formatting

#Experiment(k,networkFile, capacitiesFile, odFile, groupSize, printLinkCosts=False,
#        printDriversPerLink=False)

ex = Experiment(8,"networks/siouxfalls.kspnet.txt",\
    "networks/siouxfalls.capacity.txt", \
	"networks/od_sioux_falls_alfa.txt", 100, \
	printLinkCosts=False, printDriversPerLink=False)

##running experiments

#############
## QL ONLY ##
#############
#to run QL only you must use this method with the following paramaters.
#ex.run_ql(numEpisodes,alpha, decay)
ex.run_ql(200,0.5,0.95)

#############
## GA + QL ##
#############
#to run an experiment with GA or GA+QL you will use the method:
#run_ga_ql(useQL,generations,population,crossover,elite_size,alpha,decay)

##For GA only
ex.run_ga_ql(False,500, 100, 0.2, 0.001, 5, None, None)

##For GA+QL only
ex.run_ga_ql(True,500, 100, 0.2, 0.001, 5, 0.5,0.95)
