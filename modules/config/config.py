"""
This module serves runs the configurations and arguments necessary to the experiments.
"""
from multiprocessing import Pool
import modules.experiment.experiment as exp

"""
These attributions need to be tested to see if they're really necessary.
"""
flow = 0
p_travel_time = False
p_drivers_link = False
p_pair_od = False
p_drivers_route = False
p_interval = 1
QL_TABLE_STATE = "zero"
network_name = "OW10_1"
generations = 10
population = 100
repetitions = 1

##ExperimentType
#1: QL only
#2: GA only
#3: GA<-QL
#4: GA<->QL

experiment_type = 1
elite_size = 5
group_sizes = [1]
alphas = [.9]
decays = [.99]
crossovers = [.2]
mutations = [.001]
ks = [8]
GA_QL_interval = [10]

def run_type(k, group_size, alpha, decay, crossover, mutation, interval):
    """
    Call the apropriate script to run the experiment based on experiment type
    """
    network = "networks/" + str(network_name) + "/" + str(network_name) + ".net"

    ex = exp.Experiment(k, network, group_size, network_name, p_travel_time=p_travel_time,
                        p_drivers_link=p_drivers_link, p_pair_od=p_pair_od,
                        p_interval=p_interval, p_drivers_route=p_drivers_route,
                        TABLE_INITIAL_STATE=QL_TABLE_STATE)

    if experiment_type == 1: # QL only
        print("Running QL Only")
        ex.run_ql(generations, alpha, decay)

    elif experiment_type == 2: #GA only
        print("Running GA Only")
        print(mutation)
        ex.run_ga_ql(False, False, generations, population, crossover,
                     mutation, elite_size, None, None, None)

    elif experiment_type == 3:#GA<-QL
        print("Running GA<-QL")
        ex.run_ga_ql(True, False, generations, population, crossover,
                     mutation, elite_size, alpha, decay, None)

    elif experiment_type == 4:#GA<->QL
        print("Running GA<->QL")
        ex.run_ga_ql(True, True, generations, population, crossover,
                     mutation, elite_size, alpha, decay, interval)

def build_args():
    """
    returns: list with all the possible parameter configuration.
    each parameter configuration is a list on itself
    """
    print("Building the experiment configurations list..")
    args = []
    for g in group_sizes:
        for a in alphas:
            for d in decays:
                for c in crossovers:
                    for m in mutations:
                        for k in ks:
                            for i in GA_QL_interval:
                                args.append([g,a,d,c,m,k,i])
    return args

def run_arg(*args):
    """
    args: list of arguments
    """
    arg_0 = args[0]
    assert len(arg_0) == 7
    group_size, alpha, decay, crossover, mutation, k, interval = arg_0
    print(("Running the configuration:\n\tGrouping: %s\tAlpha: %s\n\tDecay: %s\tCrossover: %s\n\tMutation: %s"\
          + "\tk: %s\n\tInterval: %s") % tuple(arg_0))
    for repetition in range(repetitions):
        run_type(k, group_size, alpha, decay, crossover, mutation, interval)
        print(("Configuration complete:\n\tGrouping: %s Alpha: %s\n\tDecay: %s Crossover: %s\n\tMutation: %s"\
              + " k: %s\n\tInterval: %s") % tuple(arg_0))
        print("Repetition %s/%s" % (repetition+1, repetitions))

def run(number_of_processes=4):
    print("Running experiment with %s processors.." % number_of_processes)
    pool = Pool(processes=number_of_processes)
    args = build_args()
    pool.map(run_arg, args)
