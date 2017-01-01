#!/usr/bin/env python
"""
Takes care of calling the config and handling arguments from the command line.
"""
import argparse
from modules.config import config

prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                              description="""
                              Traffic Assignment Problem v6.3.4
                              Script to run the simulation of
                              drivers going from different points in a given network""")
prs.add_argument('-f', dest='file', required=True, help='The network file.\n')

prs.add_argument('-tff', dest='table_fill_file', help="Table fill file.\n")

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

prs.add_argument("-g", "--generations", type=int, default=100,
                 help="Generations\episodes in each configuration.\n")

prs.add_argument("-p", "--population", type=int, default=100,
                 help="Size of population for the genetic algorithm.\n")

prs.add_argument("--grouping", nargs="+", type=int, default=[1],
                 help="List of group sizes for drivers in each configuration. This parameter is"
                 + " useful when the number of trips/drivers is huge; it sets how many drivers"
                 + " form a group; in a group all drivers/trips use the same OD pair, i.e., the"
                 + " granularity of the route choice can be individual based or group based.\n")

prs.add_argument("-a", "--alphas", nargs="+", type=float, default=[0.5],
                 help="List of learning rates in each configuration.\n")

prs.add_argument("--decays", nargs="+", type=float, default=[0.99],
                 help="List of decays in each configuration; this sets the value by which epsilon"
                 + " is multiplied at each QL episode.\n")

prs.add_argument("-c", "--crossovers", nargs="+", type=float, default=[0.2],
                 help="List of rate of crossover in the population in each configuration.\n")

prs.add_argument("-m", "--mutations", nargs="+", type=float, default=[0.001],
                 help="List of rate of mutations in each configuration.\n")

prs.add_argument("--ks", nargs="+", type=int, default=[8],
                 help="List of the 'K' hyperparameters for the KSP (K-ShortestPath) Algorithm.\n")

prs.add_argument("--exchangeGAQL", nargs="+", type=int, default=[10],
                 help="Frequency with which the GA sends its best solution to the QL.\n")

prs.add_argument("--repetitions", type=int, default=1,
                 help="How many times it should be repeated.\n")

prs.add_argument("--experimentType", type=int, choices=[1, 2, 3, 4], default=1,
                 help="""
                 1 - QL only;
                 2 - GA only;
                 3 - QL builds solution for GA;
                 4 - GA and QL exchange solutions.\n
                 """)

prs.add_argument("-e", "--elite_size", type=int, default=5,
                 help="How many elite individuals should be kept after each generation.\n")

prs.add_argument("--number-of-processes", type=int, default=1,
                 help="How many parallel processes should be used to run the experiment configurations.\n")

prs.add_argument("--ql-table-initiation", type=str, choices=['zero', 'coupling', 'random'], \
                 default='zero', help="How to initiate the Q-Table.\n")

prs.add_argument("-n", "--flow", nargs="+", type=int, default=[0], \
                 help="List of numbers of drivers used to evaluate the link costs, when the KSP"
                 + " is computed\n")

prs.add_argument("-epl", "--epsilon", nargs="+", type=float, default=[1.0], \
                 help="List of epsilons(exploration/exploitation rate) for Q-Learning.\n")

args = prs.parse_args()

if(args.table_fill_file is None and 'coupling' == args.ql_table_initiation):
    prs.error("The 'coupling' argument requires a file to be read")

config.FILE = args.file
config.P_TRAVEL_TIME = args.printTravelTime
config.P_DRIVERS_LINK = args.printDriversPerLink
config.P_OD_PAIR = args.printODpair
config.P_INTERVAL = args.printInterval
config.P_DRIVERS_ROUTE = args.printDriversPerRoute

config.GENERATIONS = args.generations
config.POPULATION = args.population
config.REPETITIONS = args.repetitions

config.EXPERIMENT_TYPE = args.experimentType
config.ELITE_SIZE = args.elite_size
config.GROUP_SIZES = args.grouping
config.ALPHAS = args.alphas
config.DECAYS = args.decays
config.CROSSOVERS = args.crossovers
config.MUTATIONS = args.mutations
config.KS = args.ks
config.GA_QL_INTERVAL = args.exchangeGAQL
config.QL_TABLE_STATE = args.ql_table_initiation
config.FLOW = args.flow
config.PRINT_EDGES = args.printEdges
config.EPSILON = args.epsilon
config.TABLE_FILL_FILE = args.table_fill_file

config.run(number_of_processes=args.number_of_processes)
