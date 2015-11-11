# -*- coding: utf-8 -*-
"""
whith the following parameters
network file
link capacity file
od matrix file
size of groups. group size must be a integer divisor of every OD pair
printLinkCosts = whether to print the cost of each link in the output file
printDriversPerLink = whether to print the number of drivers in each link

you can run the experiment with GA+QL, GA only or GA only

FOR GA or GA+QL:
you must use the method:
run_ga_ql(useQL,generations,population,crossover,elite_size,alpha,decay)

where
 useQL = indicates whether to use QL or not with the GA
 generations = number of generations
 population = size of population
 k = number of k shortest paths
 crossover = crossover probability [0.0,1.0]
 elite_size = size of elite
 alpha = value of alpha
 decay = value of decay
in case of not using QL you can input any value in alpha and decay.
"""
from Experiment import Experiment

class ExperimentConfig:

    network = "networks/ortuzar.kspnet.txt"
    network_od = "networks/ortuzar_od.txt"

    def __init__(self, printLinkCosts=False, printDriversPerLink=True,
                 generations=10, population=100, repetitions=1,
                 experimentType=1, elite_size=5, group_sizes=[1], alphas=[.9],
                 decays=[.99], crossovers=[None], mutations=[None], ks=[8],
                 interval=[None], outputtype="normal"):

        self.network_capacity = None
        self.printLinkCosts = printLinkCosts
        self.printDriversPerLink = printDriversPerLink
        self.outputtype = outputtype

        self.generations = generations
        self.population = population
        self.repetitions = repetitions

        ##ExperimentType
        #1: QL only
        #2: GA only
        #3: GA<-QL
        #4: GA<->QL

        self.experimentType = experimentType
        self.elite_size = elite_size
        self.group_sizes = group_sizes
        self.alphas = alphas
        self.decays = decays
        self.crossovers = crossovers
        self.mutations = mutations
        self.ks = ks
        self.GA_QL_Interval = interval #intervalo para GA->QL

    def runByType(self, experimentType,k, network, network_capacity, network_od,
              group_size,printLinkCosts, printDriversPerLink, generations,
              alpha, decay, crossover,mutation,elite,population,interval):

        ex = Experiment(k,network, network_capacity, network_od, group_size,
        printLinkCosts=printLinkCosts, printDriversPerLink=printDriversPerLink,
        outputtype=self.outputtype)

        if(experimentType==2): #GA only
            ex.run_ga_ql(False,False,generations, population, crossover,
                         mutation, elite, None, None,None)
        elif(experimentType==3):#GA<-QL
            ex.run_ga_ql(True,False,generations, population, crossover,
                         mutation, elite, alpha, decay,None)
        elif(experimentType==4):#GA<->QL
            ex.run_ga_ql(True,True,generations, population, crossover,
                         mutation, elite, alpha, decay,interval)
        ##FOR QL only use this method:
        elif(experimentType==1): # QL only
            ex.run_ql(generations,alpha, decay)

    def runConfig(self, r, g, a, d, c, m ,k, i):
        self.runByType(self.experimentType, k, self.network,
                       self.network_capacity, self.network_od, g,
                       self.printLinkCosts, self.printDriversPerLink, g, a,
                       d, c, m, self.elite_size, self.population, i)

    def run(self):
        for r in range(self.repetitions):
            print("Repetition %s" % r)
            for g in self.group_sizes:
                print("Group Size %s" % g)
                for a in self.alphas:
                    print("Alpha %s" % a)
                    for d in self.decays:
                        print("Decay %s" % d)
                        for c in self.crossovers:
                            print("Crossover %s" % c)
                            for m in self.mutations:
                                print("Mutation %s" % m)
                                for k in self.ks:
                                    print("K %s" % k)
                                    for i in self.GA_QL_Interval:
                                        print("Interval %s" % i)
                                        self.runConfig(r,g,a,d,c,m,k,i)
        print("Done")

if __name__ == '__main__':
    # Setup default?
    e = ExperimentConfig(generations=1000, population=100,
                         mutations=[0.001], crossovers=[0.2],
                         group_sizes=[1], ks=[8])
    e.run()
