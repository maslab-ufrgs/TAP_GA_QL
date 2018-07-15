#!/usr/bin/env python
"""
Changelog:
    v1.0 - Changelog created. <08/03/2017>

Author: Arthur Zachow Coelho (arthur.zachow@gmail.com)

This module takes care of handling arguments from the command line.
"""
import argparse
from os.path import basename, splitext
import modules.experiment.experiment as exp


def run_type(k, group_size, alpha, decay, crossover, mutation, interval, epsilon, window_size,init_order,p_forget):
    """
    Call the apropriate script to run the experiment based on experiment type
    """
    network_name = basename(FILE)
    network_name = splitext(network_name)[0]

    ex = exp.Experiment(k, FILE, group_size, network_name, flow=FLOW,
                        p_travel_time=P_TRAVEL_TIME, table_fill_file=TABLE_FILL_FILE,
                        p_drivers_link=P_DRIVERS_LINK, p_od_pair=P_OD_PAIR, epsilon=epsilon,
                        p_interval=P_INTERVAL, p_drivers_route=P_DRIVERS_ROUTE,
                        TABLE_INITIAL_STATE=QL_TABLE_STATE, MAXI=MAXI, MINI=MINI, fixed=FIXED,
                        action_selection=ACTION_SELECTION, temperature=TEMPERATURE)
    if EXPERIMENT_TYPE == 1:  # QL only
        print("Parameters:\n\tAction sel.: {0}\tGenerations: {1}".format(ACTION_SELECTION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k))
        print("Running QL Only")
        ex.run_ql(GENERATIONS, alpha, decay)

    elif EXPERIMENT_TYPE == 2:  # GA only
        print("Parameters:\n\tPop.: {0}\tGenerations: {1}".format(POPULATION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k)
              + "\n\tMutation: {0}\tCrossover: {1}".format(mutation, crossover))
        print("Running GA Only")
        ex.run_ga_ql(False, False, GENERATIONS, POPULATION, crossover,
                     mutation, ELITE_SIZE, None, None, None)

    elif EXPERIMENT_TYPE == 3:  # GA<-QL
        print(
        "Parameters:\n\tAc. sel.: {0}\tGenerations: {1}\tPop.: {2}".format(ACTION_SELECTION, GENERATIONS, POPULATION)
        + "\n\tBase flow: {0}\tk: {1}\tMutation: {2}".format(FLOW, k, mutation))
        print("Running GA<-QL")
        ex.run_ga_ql(True, False, GENERATIONS, POPULATION, crossover,
                     mutation, ELITE_SIZE, alpha, decay, None)

    elif EXPERIMENT_TYPE == 4:  # GA<->QL
        print(
        "Parameters:\n\tAc. sel.: {0}\tGenerations: {1}\tPop.: {2}".format(ACTION_SELECTION, GENERATIONS, POPULATION)
        + "\n\tBase flow: {0}\tk: {1}\tMutation: {2}".format(FLOW, k, mutation))
        print("Running GA<->QL")
        ex.run_ga_ql(True, True, GENERATIONS, POPULATION, crossover,
                     mutation, ELITE_SIZE, alpha, decay, interval)

    elif EXPERIMENT_TYPE == 5:  # UCB1
        print("Parameters:\n\tAction sel.: {0}\tGenerations: {1}".format(ACTION_SELECTION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k))
        print("Running UCB1 Only")
        ex.run_UCB1(GENERATIONS, init_order)

    elif EXPERIMENT_TYPE == 6:  # Thompson
        print("Parameters:\n\tAction sel.: {0}\tGenerations: {1}".format(ACTION_SELECTION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k))
        print("Running Thompson  Only")
        ex.run_Thompson(GENERATIONS)

    elif EXPERIMENT_TYPE == 7:  # UCB1 Discount
        print("Parameters:\n\tAction sel.: {0}\tGenerations: {1}".format(ACTION_SELECTION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k))
        print("Running UCB1Discounted Only")
        ex.run_UCB1Discounted(GENERATIONS, decay,init_order)

    elif EXPERIMENT_TYPE == 8:  # UCB1 Sliding Window
        print("Parameters:\n\tAction sel.: {0}\tGenerations: {1}".format(ACTION_SELECTION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k))
        print("Running UCB1 Sliding Window only")
        ex.run_UCB1Window(GENERATIONS, decay, window_size, init_order)
    elif EXPERIMENT_TYPE == 9:  # Exp3
        print("Parameters:\n\tAction sel.: {0}\tGenerations: {1}".format(ACTION_SELECTION, GENERATIONS)
              + "\n\tBase flow: {0}\tk: {1}".format(FLOW, k))
        print("Running Rexp3 only")
        ex.run_Exp3(GENERATIONS, epsilon)



def build_args():
    """
    returns: list with all the possible parameter configuration.
    each parameter configuration is a list on itself
    """
    print("Building the experiment configurations list..")
    args = []
    for g_size in GROUP_SIZES:
        for alpha in ALPHAS:
            for decay in DECAYS:
                for crossover in CROSSOVERS:
                    for mutation in MUTATIONS:
                        for k in KS:
                            for interval in GA_QL_INTERVAL:
                                for epsilon in EPSILON:
                                    for window_size in WINDOW_SIZE:
                                        for init_order in INIT_ORDER:
                                            for pf in P_FORGET:
                                                args.append([g_size, alpha, decay, crossover, mutation, k,
                                                     interval, epsilon, window_size, init_order,pf])
    return args


def run_arg(args):
    """
    args: list of arguments
    """
    for arg in args:
        assert len(arg) == 11
        group_size, alpha, decay, crossover, mutation, k, interval, epsilon, window_size, init_order,pf = arg
        for repetition in range(REPETITIONS):
            run_type(k, group_size, alpha, decay, crossover, mutation, interval, epsilon, window_size,init_order,pf)
            print("Repetition %s/%s\n" % (repetition + 1, REPETITIONS))


def run():
    """
    Run the experiment.
    """
    args = build_args()
    run_arg(args)


if __name__ == "__main__":
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="""
                                  Traffic Assignment Problem or
                                  Route Choice Problem.
                                  Script to run the simulation of
                                  drivers going from different points in a given network""")
    prs.add_argument("-f", dest="file", required=True, help="The network file.\n")

    prs.add_argument("-as", "--action-selection", type=str, choices=["epsilon", "boltzmann"],
                     default="epsilon", help="How the agents should select their actions.\n")

    prs.add_argument("-et", "--experimentType", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9], default=1,
                     help="""
                     1 - QL only;
                     2 - GA only;
                     3 - QL builds solution for GA;
                     4 - GA and QL exchange solutions.
                     5 - UCB1 only
                     6 - Thompson only
                     7 - UCB1 Discounted only
                     8 - UCB1 Sliding Window only
                     9 - Rexp3\n
                     """)

    prs.add_argument("-r", "--repetitions", type=int, default=1,
                     help="How many times it should be repeated.\n")

    prs.add_argument("-k", "--ks", nargs="+", type=int, default=[8],
                     help="List of the 'K' hyperparameters for the KSP (K-ShortestPath) Algorithm.\n")

    prs.add_argument("-g", "--generations", type=int, default=100,
                     help="Generations\episodes in each configuration.\n")

    prs.add_argument("-n", "--flow", type=int, default=0, help="Base flow in the network.\n")

    prs.add_argument("-group", "--grouping", nargs="+", type=int, default=[1],
                     help="List of group sizes for drivers in each configuration. This parameter is"
                          + " useful when the number of trips/drivers is huge; it sets how many drivers"
                          + " form a group; in a group all drivers/trips use the same OD pair, i.e., the"
                          + " granularity of the route choice can be individual based or group based.\n")

    prs.add_argument("--printTravelTime", action="store_true", default=False,
                     help="Print link's travel time at each iteration in the output file.\n")

    prs.add_argument("--printDriversPerRoute", action="store_true", default=False,
                     help="Print the amount of drivers per route for each OD pair(Warning:QL only!"
                          + " Also, note that the number of OD pairs can be very large!).\n")

    prs.add_argument("--printDriversPerLink", action="store_true", default=False,
                     help="Print the number of drivers in each link in the output file.\n")

    prs.add_argument("--printEdges", action="store_true", default=False,
                     help="Print the travel time per edge.\n")

    prs.add_argument("--printODpair", action="store_true", default=False,
                     help="Print the average travel time in the header in the output file.\n")

    prs.add_argument("--printInterval", type=int, default=1,
                     help="Interval by which the messages are written in the output file.\n")

    prs.add_argument("-e", "--elite_size", type=int, default=5,
                     help="How many elite individuals should be kept after each generation.\n")

    prs.add_argument("-p", "--population", type=int, default=100,
                     help="Size of population for the genetic algorithm.\n")

    prs.add_argument("-c", "--crossovers", nargs="+", type=float, default=[0.2],
                     help="List of rate of crossover in the population in each configuration.\n")

    prs.add_argument("-m", "--mutations", nargs="+", type=float, default=[0.001],
                     help="List of rate of mutations in each configuration.\n")

    prs.add_argument("-i", "--exchangeGAQL", nargs="+", type=int, default=[10],
                     help="Interval of generations in which the GA sends its best solution to the QL.\n")

    prs.add_argument("-tff", dest="table_fill_file", help="Table fill file.\n")

    prs.add_argument("-qti", "--ql-table-initiation", type=str, choices=['coupling', 'random', 'fixed'], \
                     default='fixed', help="How to initiate the Q-Table.\n")

    prs.add_argument("--max", type=float, default=0.0, help="Maximum value for the random" \
                                                            + " initiation. Note that the random value(x) will be x <= max !\n")

    prs.add_argument("--min", type=float, default=0.0, help="Maximum value for the random" \
                                                            + " initiation. Note that the random value(x) will be min <= x !\n")

    prs.add_argument("--fixed", type=float, default=0.0, help="Fixed value for generating the" \
                                                              + " Q table.\n")

    prs.add_argument("-epl", "--epsilon", nargs="+", type=float, default=[1.0], \
                     help="List of epsilons(exploration rate) for Q-Learning and Exp3.\n")

    prs.add_argument("-a", "--alphas", nargs="+", type=float, default=[0.5],
                     help="List of learning rates in each configuration.\n")

    prs.add_argument("-d", "--decays", nargs="+", type=float, default=[0.99],
                     help="List of decays in each configuration; this sets the value by which epsilon"
                          + " is multiplied at each QL episode. Also used as the discount factor on Discounted UCB and Sliding window UCB."
                          +  "\n")

    prs.add_argument("-t", "--temperature", type=float, help="Temperature for the" \
                                                             " Boltzmann action selection.\n")
    prs.add_argument("-ws", "--windowsize", nargs="+", type=int, default=[20],
                     help="Window size for Sliding Window UCB1\n")
    prs.add_argument("-io", "--initorder", nargs="+", type=int, default=[1],choices=[1, 2],
                     help="How UCB-based algorithms should be initiaded: 1-random order, 2-sequential order\n")
    prs.add_argument("-pf", "--probabilityforget", nargs="+", type=float, default=[1.0], \
                     help="List of probabilities of forgetting for the Rexp3MA algorithms.\n")


    args = prs.parse_args()

    if args.table_fill_file is None and args.ql_table_initiation == "coupling":
        prs.error("The 'coupling' argument requires a file to be read")

    if args.action_selection == "boltzmann" and args.temperature is None:
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

    if (args.experimentType == 3 or args.experimentType == 4) and (P_DRIVERS_ROUTE or P_OD_PAIR
                                                                   or P_DRIVERS_LINK or P_TRAVEL_TIME):
        prs.error("You can't use print-outs with experiment type 3 or 4.")

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
    FLOW = args.flow
    EPSILON = args.epsilon
    TABLE_FILL_FILE = args.table_fill_file
    TEMPERATURE = args.temperature
    ACTION_SELECTION = args.action_selection
    WINDOW_SIZE = args.windowsize
    INIT_ORDER = args.initorder
    P_FORGET = args.probabilityforget
    run()
