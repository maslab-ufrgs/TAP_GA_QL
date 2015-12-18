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
from multiprocessing import Pool

ORTUZAR_NETWORK = "networks/ortuzar.kspnet.txt"
ORTUZAR_NETWORK_OD = "networks/ortuzar_od.txt"
SIOUXFALLS_NETWORK = "networks/siouxfalls.kspnet.txt"
SIOUXFALLS_CAPACITY = "networks/siouxfalls.capacity.txt"
SIOUXFALLS_NETWORK_OD = "networks/od_sioux_falls_alfa.txt"

DEBUG = True

def echo(msg):
  if DEBUG:
    print(msg)

class ExperimentConfig:

  def __init__(self, printLinkCosts=False, printDriversPerLink=False,
               printPairOD=False, generations=10, population=100,
               repetitions=1, experimentType=1, elite_size=5,
               group_sizes=[100], alphas=[.9], decays=[.99], crossovers=[0.2],
               mutations=[0.001], ks=[8], interval=[None],
               network=ORTUZAR_NETWORK, network_od=ORTUZAR_NETWORK_OD,
               printInterval=1):

      self.network_capacity = SIOUXFALLS_CAPACITY
      self.printLinkCosts = printLinkCosts
      self.printDriversPerLink = printDriversPerLink
      self.printPairOD = printPairOD
      self.printInterval = printInterval
      self.network = network
      self.network_od = network_od

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

  def runByType(self, k, group_size, alpha, decay, crossover, mutation,
                interval):
    """
    Call the apropriate script to run the experiment based on experiment type
    """

    ex = Experiment(k, self.network, self.network_capacity, self.network_od, group_size,
    printLinkCosts=self.printLinkCosts, printDriversPerLink=self.printDriversPerLink,
    printPairOD=self.printPairOD, printInterval=self.printInterval)

    if(self.experimentType==2): #GA only
        print("Running GA Only")
        print(mutation)
        ex.run_ga_ql(False,False, self.generations, self.population, crossover,
                      mutation, self.elite_size, None, None,None)
    elif(self.experimentType==3):#GA<-QL
        print("Running GA<-QL ")
        ex.run_ga_ql(True,False, self.generations, self.population, crossover,
                      mutation, self.elite_size, alpha, decay,None)
    elif(self.experimentType==4):#GA<->QL
        print("Running GA<->QL ")
        ex.run_ga_ql(True,True, self.generations, self.population, crossover,
                      mutation, self.elite_size, alpha, decay, interval)

    ##FOR QL only use this method:
    elif(self.experimentType==1): # QL only
        print("Running QL Only ")
        ex.run_ql(self.generations, alpha, decay)

  def buildParameters(self):
    """
    returns: list with all the possible parameter configuration.
    each parameter configuration is a list on itself
    """
    echo("Building arg list..")
    args = []
    for g in self.group_sizes:
        for a in self.alphas:
            for d in self.decays:
                for c in self.crossovers:
                    for m in self.mutations:
                        for k in self.ks:
                            for i in self.GA_QL_Interval:
                                args.append([g,a,d,c,m,k,i])
    return args

  def runArg(self, a):
    """
    a: list of arguments
    """
    assert len(a) == 7
    group_size, alpha, decay, crossover, mutation, k, interval = a
    echo("Running an arg %s" % a)
    for _ in range(self.repetitions):
      self.runByType(k, group_size, alpha, decay, crossover, mutation,
                     interval)
    echo("Arg ran.")

  def run(self, number_of_processes=4):
    """
    Typicaly the execution starts through here
    """
    echo("Running experiment with %s processors.." % number_of_processes)
    pool = Pool(processes=number_of_processes)
    args = self.buildParameters()
    for arg in args:
      self.runArg(arg)
    echo("All args ran.")

if __name__ == "__main__":
  e = ExperimentConfig(ks=[1,2,3,4])
  e.run()
