from config import ExperimentConfig as cfg
import config
import argparse

p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                            description="""Script to run the simulation of
                            drivers going from different points in the ortuzar
                            and siouxfalls networks""")

p.add_argument("-c", "--printLinkCosts", action="store_true", default=False,
               help="Print link's costs at each iteration in the output file")

p.add_argument("-d", "--printDriversPerLink", action="store_true", default=False,
               help="Print the number of drivers in at each iteration in the output file")

p.add_argument("-p", "--printPairOD", action="store_true", default=False,
               help="Print the average travel time for in the header in the output file")

p.add_argument("-i", "--printInterval", type=int, default=1,
               help="Interval by which the messages are written in the output file")

p.add_argument("--generations", type=int, default=400,
               help="Maximum mumber of generations in each configuration")

p.add_argument("--population", type=int, default=100,
               help="Size of population for the genetic algorithm")

p.add_argument("--group_sizes", nargs="+", type=int, default=[100],
               help="List of group sizes for drivers in each configuration")

p.add_argument("--alphas", nargs="+", type=float, default=[.9],
               help="List of learning in each configuration")

p.add_argument("--decays", nargs="+", type=float, default=[.99],
               help="List of decays in each configuration")

p.add_argument("--crossovers", nargs="+", type=float, default=[0.2],
               help="List of rate of crossover in the population in each configuration")

p.add_argument("--mutations", nargs="+", type=float, default=[0.001],
               help="List of rate of mutations in each configuration")

p.add_argument("--ks", nargs="+", type=int, default=[8],
               help="<TODO WRITE HELP MESSAGE FOR THIS OPTION>")

p.add_argument("--intervals", nargs="+", type=int, default=[None],
               help="<TODO WRITE HELP MESSAGE FOR THIS OPTION>")

p.add_argument("--repetitions", type=int, default=1,
               help="How many times it should be repeated")

p.add_argument("--network", type=unicode, choices=['ortuzar', 'siouxfalls'], default='ortuzar',
               help="Which network should be used")

p.add_argument("--experimentType", type=int, choices=[1,2,3,4], default=1,
               help="""How many repetition for each configuration.
               1 - Use Q-Learn Only
               2 - Use Genetic Algorithm
               3 - The Genetic Algorithm receives information from the Q-learn algorithm
               4 - The Genetic Algorithm receives and updates information
                   from the Q-learn algorithm
               """)

p.add_argument("--elite_size", type=int, default=5,
               help="How many elite individuals should be kept after each generation")

a = p.parse_args()

networks = {
  'ortuzar': (config.ORTUZAR_NETWORK, config.ORTUZAR_NETWORK_OD),
  'siouxfalls': (config.SIOUXFALLS_NETWORK, config.SIOUXFALLS_NETWORK_OD)
}

configuration = cfg(printLinkCosts=a.printLinkCosts, printDriversPerLink=a.printDriversPerLink,
             printPairOD=a.printPairOD, generations=a.generations,
             population=a.population, repetitions=a.repetitions,
             experimentType=a.experimentType, elite_size=a.elite_size,
             group_sizes=a.group_sizes, alphas=a.alphas, decays=a.decays,
             crossovers=a.crossovers, mutations=a.mutations, ks=a.ks,
             interval=a.intervals, network_od=networks[a.network][1],
             network=networks[a.network][0])

configuration.run()

