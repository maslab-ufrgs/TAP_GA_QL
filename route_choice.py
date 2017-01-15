#!/usr/bin/env python
"""
Takes care of calling the config and handling arguments from the command line.
"""
import argparse
from os.path import basename, splitext
import modules.experiment.experiment as exp

def run_type(k, group_size, alpha, decay, crossover, mutation, interval, flow, epsilon):
    """
    Call the apropriate script to run the experiment based on experiment type
    """
    NETWORK_NAME = basename(FILE)
    NETWORK_NAME = splitext(NETWORK_NAME)[0]

    ex = exp.Experiment(k, FILE, group_size, NETWORK_NAME, PRINT_EDGES, flow=flow,
                        p_travel_time=P_TRAVEL_TIME, table_fill_file=TABLE_FILL_FILE,
                        p_drivers_link=P_DRIVERS_LINK, p_od_pair=P_OD_PAIR, epsilon=epsilon,
                        p_interval=P_INTERVAL, p_drivers_route=P_DRIVERS_ROUTE,
                        TABLE_INITIAL_STATE=QL_TABLE_STATE, MAXI=MAXI, MINI=MINI, fixed=FIXED,
                        action_selection=ACTION_SELECTION, temperature=TEMPERATURE)

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

def run_arg(args):
    """
    args: list of arguments
    """
    for arg in args:
        assert len(arg) == 9
        group_size, alpha, decay, crossover, mutation, k, interval, flow, epsilon = arg
        print(("Running the configuration:\n\tGrouping: %s\tAlpha: %s\n\tDecay: %s\tCrossover: %s"
               + "\n\tMutation: %s\tk: %s\n\tInterval: %s\tFlow: %s\n\tEpsilon: %s") % tuple(arg))
        for repetition in range(REPETITIONS):
            run_type(k, group_size, alpha, decay, crossover, mutation, interval, flow, epsilon)
            print(("Configuration complete:\n\tGrouping: %s\tAlpha: %s\n\tDecay: %s\tCrossover: %s"
                   + "\n\tMutation: %s\tk: %s\n\tInterval: %s\tFlow: %s\n\tEpsilon: %s") % tuple(arg))
            print("Repetition %s/%s" % (repetition+1, REPETITIONS))

def run():
    """
    Run the experiment.
    """
    args = build_args()
    run_arg(args)

if __name__ == "__main__":
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="""
                                  Traffic Assignment Problem
                                  Script to run the simulation of
                                  drivers going from different points in a given network""")
    prs.add_argument('-f', dest='file', required=True, help='The network file.\n')

    prs.add_argument("--action-selection", type=str, choices=["epsilon", "boltzmann"],
                     default="epsilon", help="How the agents should select their actions.\n")

    prs.add_argument("--experimentType", type=int, choices=[1, 2, 3, 4], default=1,
                     help="""
                     1 - QL only;
                     2 - GA only;
                     3 - QL builds solution for GA;
                     4 - GA and QL exchange solutions.\n
                     """)

    prs.add_argument("--repetitions", type=int, default=1,
                     help="How many times it should be repeated.\n")

    prs.add_argument("--ks", nargs="+", type=int, default=[8],
                     help="List of the 'K' hyperparameters for the KSP (K-ShortestPath) Algorithm.\n")

    prs.add_argument("-g", "--generations", type=int, default=100,
                     help="Generations\episodes in each configuration.\n")

    prs.add_argument("--grouping", nargs="+", type=int, default=[1],
                     help="List of group sizes for drivers in each configuration. This parameter is"
                     + " useful when the number of trips/drivers is huge; it sets how many drivers"
                     + " form a group; in a group all drivers/trips use the same OD pair, i.e., the"
                     + " granularity of the route choice can be individual based or group based.\n")

    prs.add_argument("--printTravelTime", action="store_true", default=False,
                     help="Print link's travel time at each iteration in the output file.\n")

    prs.add_argument("--printDriversPerRoute", action="store_true", default=False,
                     help="Print the amount of drivers per route for each OD pair(Warning:QL only!"
                     + " Also, note that the number of OD pairs can be very large!).\n")

    prs.add_argument("-d", "--printDriversPerLink", action="store_true", default=False,
                     help="Print the number of drivers in each link in the output file.\n")

    prs.add_argument("--printEdges", action="store_true", default=False,
                     help="Print the travel time per edge.\n")

    prs.add_argument("-o", "--printODpair", action="store_true", default=False,
                     help="Print the average travel time in the header in the output file.\n")

    prs.add_argument("-i", "--printInterval", type=int, default=1,
                     help="Interval by which the messages are written in the output file.\n")

    prs.add_argument("-e", "--elite_size", type=int, default=5,
                     help="How many elite individuals should be kept after each generation.\n")

    prs.add_argument("-p", "--population", type=int, default=100,
                     help="Size of population for the genetic algorithm.\n")

    prs.add_argument("-c", "--crossovers", nargs="+", type=float, default=[0.2],
                     help="List of rate of crossover in the population in each configuration.\n")

    prs.add_argument("-m", "--mutations", nargs="+", type=float, default=[0.001],
                     help="List of rate of mutations in each configuration.\n")

    prs.add_argument("--exchangeGAQL", nargs="+", type=int, default=[10],
                     help="Frequency with which the GA sends its best solution to the QL.\n")

    prs.add_argument('-tff', dest='table_fill_file', help="Table fill file.\n")

    prs.add_argument("--ql-table-initiation", type=str, choices=['coupling', 'random', 'fixed'], \
                     default='fixed', help="How to initiate the Q-Table.\n")

    prs.add_argument("--max", type=float, default=0.0, help="Maximum value for the random" \
                     + " initiation. Note that the random value(x) will be x <= max !\n")

    prs.add_argument("--min", type=float, default=0.0, help="Maximum value for the random" \
                     + " initiation. Note that the random value(x) will be min <= x !\n")

    prs.add_argument("--fixed", type=float, default=0.0, help="Fixed value for generating the" \
                     + " Q table.\n")

    prs.add_argument("-epl", "--epsilon", nargs="+", type=float, default=[1.0], \
                     help="List of epsilons(exploration/exploitation rate) for Q-Learning.\n")

    prs.add_argument("-a", "--alphas", nargs="+", type=float, default=[0.5],
                     help="List of learning rates in each configuration.\n")

    prs.add_argument("--decays", nargs="+", type=float, default=[0.99],
                     help="List of decays in each configuration; this sets the value by which epsilon"
                     + " is multiplied at each QL episode.\n")

    prs.add_argument("-t", "--temperature", type=float, help="Temperature for the" \
                     " Boltzmann action selection.\n")

    args = prs.parse_args()

    if(args.table_fill_file is None and 'coupling' == args.ql_table_initiation):
        prs.error("The 'coupling' argument requires a file to be read")

    if(args.action_selection == "boltzmann" and args.temperature == None):
        prs.error("The 'boltzmann' type of action selection requires a temperature.")

    MINI = args.min
    MAXI = args.max
    FIXED = args.fixed

    FILE = args.file
    P_TRAVEL_TIME = args.printTravelTime
    P_DRIVERS_LINK = args.printDriversPerLink
    P_OD_PAIR = args.printODpair
    P_INTERVAL = args.printInterval
    P_DRIVERS_ROUTE = args.printDriversPerRoute

    GENERATIONS = args.generations
    POPULATION = args.population
    REPETITIONS = args.repetitions

    EXPERIMENT_TYPE = args.experimentType
    ELITE_SIZE = args.elite_size
    GROUP_SIZES = args.grouping
    ALPHAS = args.alphas
    DECAYS = args.decays
    CROSSOVERS = args.crossovers
    MUTATIONS = args.mutations
    KS = args.ks
    GA_QL_INTERVAL = args.exchangeGAQL
    QL_TABLE_STATE = args.ql_table_initiation
    FLOW = [0] #args.flow
    PRINT_EDGES = args.printEdges
    EPSILON = args.epsilon
    TABLE_FILL_FILE = args.table_fill_file
    TEMPERATURE = args.temperature
    ACTION_SELECTION = args.action_selection

    run()
