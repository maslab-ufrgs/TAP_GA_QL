# -*- coding: utf-8 -*-
"""
This file serves as a template for how to run a set of experiments

you may modify the cost function by modifying calculateEdgesCosts in
the class Experiment

To use this file, modify the parameters on line 71.
"""
#imports Experiment modules
from Experiment import Experiment 

##calls an experiment. You can modify the function inputs
##according to your needs
##ExperimentType
#1: QL only
#2: GA only
#3: GA<-QL
#4: GA<->QL

def call((experimentType,k, network, network_capacity, network_od, group_size,printLinkCosts, printDriversPerLink, generations, alpha, decay, crossover,mutation,elite,population,interval)):
    ##sets up an experience instance
    ex = Experiment(k,network,\
	    network_capacity, \
	    network_od, group_size, \
	    printLinkCosts=printLinkCosts, printDriversPerLink=printDriversPerLink)
       
    #whith the following parameters
    #k = number of k shortest paths
    #network file
    #link capacity file
    #od matrix file
    #size of groups. group size must be a integer divisor of every OD pair
    #printLinkCosts = whether to print the cost of each link in the output file
    #printDriversPerLink = whether to print the number of drivers in each link
       
    
    ##you can run the experiment with GA+QL, GA only or GA only

    ##FOR GA or GA+QL:
    #you must use the method:    
    #run_ga_ql(useQL,generations,population,crossover,elite_size,alpha,decay)

    #where
    # useQL = indicates whether to use QL or not with the GA
    # generations = number of generations
    # population = size of population 
    # crossover = crossover probability [0.0,1.0]
    # elite_size = size of elite
    # alpha = value of alpha
    # decay = value of decay
    #in case of not using QL you can input any value in alpha and decay.
   

    if(experimentType==2): #GA only
        ex.run_ga_ql(False,False,generations, population, crossover, mutation, elite, None, None,None)
    elif(experimentType==3):#GA<-QL
        ex.run_ga_ql(True,False,generations, population, crossover, mutation, elite, alpha, decay,None)
    elif(experimentType==4):#GA<->QL
        ex.run_ga_ql(True,True,generations, population, crossover, mutation, elite, alpha, decay,interval)
    ##FOR QL only use this method:
    elif(experimentType==1): # QL only
        ex.run_ql(generations,alpha, decay)

    
##you can speed up the process by executing experiments in parallel
from multiprocessing import Pool


#to allow for parallel execution of experiments, the multiprocessing
#module is used. the call function receives as input a tuple of the
#paramaters needed for the execution of a single experiment.

#Because we'll use the map function, we have to first build a list 
#of arguments for call() which are tuples.

#creates a list of different parameter combinations.

#######################################################################
##  SETUP EXPERIMENTS HERE ############################################


network = "networks/ortuzar.kspnet.txt"
network_capacity = None
network_od = "networks/ortuzar_od.txt"

printLinkCosts = False
printDriversPerLink = True
generations = 10
population = 100
repetitions = 1

##ExperimentType
#1: QL only
#2: GA only
#3: GA<-QL
#4: GA<->QL

experimentType = 1

elite_size = 5

##All combinations of the values below will be calculated. If your experiment
#does not require one of these values, None must be the only value of the 
#respective list. If there is more than one element, the same experiment will
#be repeated

group_sizes = [1]
alphas = [0.9]  
decays = [0.99] 
crossovers = [None]
mutations = [None]
ks = [8]
GA_QL_Interval = [None] #intervalo para GA->QL

#######################################################################
#######################################################################

args=[]
for repetition in range(repetitions):
    for group_size in group_sizes:
        for alpha in alphas:
            for decay in decays:
                for crossover in crossovers:
                    for mutation in mutations:
                        for k in ks:
                            for i in GA_QL_Interval: #Adicionei caso a Professora Ana queira mais de um intervalo.
                                call( (experimentType,k, network, network_capacity, network_od, group_size,printLinkCosts, printDriversPerLink, generations, alpha, decay, crossover,mutation,elite_size,population,i))
print args
p = Pool(5)
#here the arguments generated before are used for the parallel execution
p.map(call, args)    