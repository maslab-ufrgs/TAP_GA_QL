from Experiment import Experiment
from multiprocessing import Pool

DEBUG = True

def echo(msg):
  if DEBUG:
    print(msg)

printTravelTime = False
printDriversPerLink = False
printPairOD = False
printDriversPerRoute = False #new flag
printInterval = 1
QL_TABLE_STATE = "zero" ##How to initiate the Qtable
networkName = "OW10_1" ##Network name now will be an input
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
group_sizes = [1]
alphas = [.9]
decays = [.99]
crossovers = [.2]
mutations = [.001]
ks = [8]
GA_QL_Interval = [10] #intervalo para GA->QL

def runByType(k, group_size, alpha, decay, crossover, mutation, interval):
    """
    Call the apropriate script to run the experiment based on experiment type
    """
    network = "networks/"+str(networkName)+"/"+str(networkName)+".net"
    network_od = "networks/"+str(networkName)+"/"+str(networkName)+".od.txt"
    network_capacity = "networks/"+str(networkName)+"/"+str(networkName)+".capacity.txt"

    ex = Experiment(k, network, network_capacity, network_od, group_size,networkName,
    printTravelTime=printTravelTime, printDriversPerLink=printDriversPerLink,
    printPairOD=printPairOD, printInterval=printInterval,printDriversPerRoute=printDriversPerRoute,TABLE_INITIAL_STATE=QL_TABLE_STATE)
    if(experimentType==2): #GA only
        print("Running GA Only")
        print(mutation)
        ex.run_ga_ql(False,False, generations, population, crossover,
                      mutation, elite_size, None, None,None)
    elif(experimentType==3):#GA<-QL
        print("Running GA<-QL ")
        ex.run_ga_ql(True,False, generations, population, crossover,
                      mutation, elite_size, alpha, decay,None)
    elif(experimentType==4):#GA<->QL
        print("Running GA<->QL ")
        ex.run_ga_ql(True,True, generations, population, crossover,
                      mutation, elite_size, alpha, decay, interval)
    ##FOR QL only use this method:
    elif(experimentType==1): # QL only       
	print("Running QL Only ")
        ex.run_ql(generations, alpha, decay)
	

def buildArgs():
    """
    returns: list with all the possible parameter configuration.
    each parameter configuration is a list on itself
    """
    echo("Building the experiment configurations list..")
    args = []
    for g in group_sizes:
        for a in alphas:
            for d in decays:
                for c in crossovers:
                    for m in mutations:
                        for k in ks:
                            for i in GA_QL_Interval:
                                args.append([g,a,d,c,m,k,i])
    return args

def runArg(*args):
    """
    args: list of arguments
    """
    a = args[0]
    assert len(a) == 7
    group_size, alpha, decay, crossover, mutation, k, interval = a
    echo("Running the configuration: grouping: %s alpha: %s decay: %s crossover: %s mutation: %s k: %s interval: %s" % tuple(a))
    for r in range(repetitions):
        runByType(k, group_size, alpha, decay, crossover, mutation, interval)
        echo("Configuration complete: grouping: %s alpha: %s decay: %s crossover: %s mutation: %s k: %s interval: %s" % tuple(a))
        echo("Repetition %s/%s" % (r,repetitions))


def run(number_of_processes=4):
    echo("Running experiment with %s processors.." % number_of_processes)
    pool = Pool(processes=number_of_processes)
    args = buildArgs()
    pool.map(runArg, args)
