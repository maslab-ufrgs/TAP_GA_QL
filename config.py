"""
Module containing the ExperimentConfig class and some definitions
"""
from Experiment import Experiment
from multiprocessing import Pool

OW10_1_NETWORK = "networks/OW10_1.kspnet.txt"
OW10_1_NETWORK_OD = "networks/OW10_1.od.txt"
SF_NETWORK = "networks/SF.kspnet.txt"
SF_CAPACITY = "networks/SF.capacity.txt"
SF_NETWORK_OD = "networks/OW10_1_SF_alpha.txt"

DEBUG = True

def echo(msg):
  if DEBUG:
    print(msg)

class ExperimentConfig:

  def __init__(self, printTravelTime=False, printDriversPerLink=False,
               printPairOD=False, generations=10, population=100,
               repetitions=1, experimentType=1, elite_size=5,
               group_sizes=[100], alphas=[.9], decays=[.99], crossovers=[0.2],
               mutations=[0.001], ks=[8], interval=[None],
               network=OW10_1_NETWORK, network_od=OW10_1_NETWORK_OD,
               printInterval=1):

      self.network_capacity = SF_CAPACITY
      self.printTravelTime = printTravelTime
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
    printTravelTime=self.printTravelTime, printDriversPerLink=self.printDriversPerLink,
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
