"""
This module serves runs the configurations and arguments necessary to the experiments.
"""
from multiprocessing import Pool
import modules.experiment.experiment as exp

"""
These attributions need to be tested to see if they're really necessary.
"""
PRINT_EDGES = False
FLOW = 0
P_TRAVEL_TIME = False
P_DRIVERS_LINK = False
P_OD_PAIR = False
P_DRIVERS_ROUTE = False
P_INTERVAL = 1
QL_TABLE_STATE = "zero"
NETWORK_NAME = "OW"
GENERATIONS = 10
POPULATION = 100
REPETITIONS = 1

##ExperimentType
#1: QL only
#2: GA only
#3: GA<-QL
#4: GA<->QL

EXPERIMENT_TYPE = 1
ELITE_SIZE = 5
GROUP_SIZES = [1]
ALPHAS = [.9]
DECAYS = [.99]
CROSSOVERS = [.2]
MUTATIONS = [.001]
KS = [8]
GA_QL_INTERVAL = [10]
EPSILON = [1]

def run_type(k, group_size, alpha, decay, crossover, mutation, interval, flow, epsilon):
    """
    Call the apropriate script to run the experiment based on experiment type
    """
    network = "networks/" + str(NETWORK_NAME) + "/" + str(NETWORK_NAME) + ".net"

    ex = exp.Experiment(k, network, group_size, NETWORK_NAME, PRINT_EDGES, flow=flow, p_travel_time=P_TRAVEL_TIME,
                        p_drivers_link=P_DRIVERS_LINK, p_od_pair=P_OD_PAIR, epsilon=epsilon,
                        p_interval=P_INTERVAL, p_drivers_route=P_DRIVERS_ROUTE,
                        TABLE_INITIAL_STATE=QL_TABLE_STATE)

    if EXPERIMENT_TYPE == 1: # QL only
        print("Running QL Only")
        ex.run_ql(GENERATIONS, alpha, decay)

    elif EXPERIMENT_TYPE == 2: #GA only
        print("Running GA Only")
        print(mutation)
        ex.run_ga_ql(False, False, GENERATIONS, POPULATION, crossover,
                     mutation, ELITE_SIZE, None, None, None)

    elif EXPERIMENT_TYPE == 3:#GA<-QL
        print("Running GA<-QL")
        ex.run_ga_ql(True, False, GENERATIONS, POPULATION, crossover,
                     mutation, ELITE_SIZE, alpha, decay, None)

    elif EXPERIMENT_TYPE == 4:#GA<->QL
        print("Running GA<->QL")
        ex.run_ga_ql(True, True, GENERATIONS, POPULATION, crossover,
                     mutation, ELITE_SIZE, alpha, decay, interval)

def build_args():
    """
    returns: list with all the possible parameter configuration.
    each parameter configuration is a list on itself
    """
    print("Building the experiment configurations list..")
    args = []
    for g in GROUP_SIZES:
        for a in ALPHAS:
            for d in DECAYS:
                for c in CROSSOVERS:
                    for m in MUTATIONS:
                        for k in KS:
                            for i in GA_QL_INTERVAL:
                                for flw in FLOW:
                                    for en in EPSILON:
                                        args.append([g,a,d,c,m,k,i,flw,en])
    return args

def run_arg(*args):
    """
    args: list of arguments
    """
    arg_0 = args[0]
    assert len(arg_0) == 9
    group_size, alpha, decay, crossover, mutation, k, interval, flow, epsilon = arg_0
    print(("Running the configuration:\n\tGrouping: %s\tAlpha: %s\n\tDecay: %s\tCrossover: %s\n\tMutation: %s"\
            + "\tk: %s\n\tInterval: %s\tFlow: %s\n\tEpsilon: %s") % tuple(arg_0))
    for repetition in range(REPETITIONS):
        run_type(k, group_size, alpha, decay, crossover, mutation, interval, flow, epsilon)
        print(("Configuration complete:\n\tGrouping: %s\tAlpha: %s\n\tDecay: %s\tCrossover: %s\n\tMutation: %s"\
                + "\tk: %s\n\tInterval: %s\tFlow: %s\n\tEpsilon: %s") % tuple(arg_0))
        print("Repetition %s/%s" % (repetition+1, REPETITIONS))

def run(number_of_processes=4):
    print("Running experiment with %s processors.." % number_of_processes)
    pool = Pool(processes=number_of_processes)
    args = build_args()
    pool.map(run_arg, args)
