Script to run the simulation of drivers going from different points in the
OW and SF networks

Can get other networks from
===========================
 * [Networks](https://github.com/maslab-ufrgs/network-files)
 
To add:

1. Download from the link above the desired network.
2. Run the validator.py script from the link above on the desired network.
3. If the file passes the test, then create a folder on the networks/ folder with the same name as the network file.
4. To run just use the --net NETWORK_NAME argument.

Note: The simulator currently only work with edges, it doesn't work with degdes.

Warning
=======

> The cost functions used for edge travel time avaliation are tied to the network being run (SF or OW10_1). If you are 
> going to use other networks, you most likely want to edit the calculateTravelTime function in the experiment.py module.

Dependencies
============
 * [Python 2.7](https://www.python.org/downloads/)
 * [Pyevolve](https://sourceforge.net/projects/pyevolve/)
 * [Python Mathematical Expression Evaluator](https://pypi.python.org/pypi/py_expression_eval)

Usage
=====

```sh
python traffic_simulation.py [OPTIONS]
```
Or:
```sh
./traffic_simulation.py [OPTIONS]
```

All the options have usable defaults so check them before running a experiment.

Use:

```sh
python traffic_simulation.py -h
```

To list all the options.

Checking the results
--------------------

After the execution is complete, a new file in the "results_gaql_grouped" folder
should be created.

The name of the file will contain the parameters used to run the experiment
and the local time when it happened.

Examples
--------

* Run an experiment with the *SF* network and prints the travel time
  for the each pair of Origin and Destination

```sh
python traffic_simulation.py --network "SF" --printPairOD
```

* Run an experiment with the *OW10_1* network printing the link's travel time at every
100 generations with the mutations of 0.003 and 0.03

```sh
python traffic_simulation.py --printTravelTime --printInterval 100 --mutations 0.003 0.03
```

* Run an experiment with the *SF* network using alphas 0.3 and 0.4,
decays 0.9 and 0.99 and 1000 generations.

```sh
python traffic_simulation.py --network "SF" --alphas 0.3 0.4 --decays 0.9 0.99 --generations 1000
```

* Run an QL experiment with the *OW10_1* network initiating the QL-table with random values.

```sh
python traffic_simulation.py --network "OW10_1" --experimentType 1 --ql-table-initiation random
```

Options
=======

```
optional arguments:
  -h, --help            show this help message and exit
  --printTravelTime     Print link's travel time at each iteration in the
                        output file (default: False)
  -d, --printDriversPerLink
                        Print the number of drivers in each link in the output
                        file (default: False)
  -o, --printPairOD     Print the average travel time for in the header in the
                        output file (default: False)
  --printDriversPerRoute     
                        Prints the amount of drivers per route of each OD pair(default:False)
  -i PRINTINTERVAL, --printInterval PRINTINTERVAL
                        Interval by which the messages are written in the
                        output file (default: 1)
  -g GENERATIONS, --generations GENERATIONS
                        Maximum mumber of generations in each configuration
                        (default: 400)
  -p POPULATION, --population POPULATION
                        Size of population for the genetic algorithm (default:
                        100)
  --grouping GROUPING [GROUPING ...]
                        List of group sizes for drivers in each configuration
                        (default: [100])
  -a ALPHAS [ALPHAS ...], --alphas ALPHAS [ALPHAS ...]
                        List of learning rates in each configuration (default:
                        [0.9])
  --decays DECAYS [DECAYS ...]
                        List of decays in each configuration (default: [0.99])
  -c CROSSOVERS [CROSSOVERS ...], --crossovers CROSSOVERS [CROSSOVERS ...]
                        List of rate of crossover in the population in each
                        configuration (default: [0.2])
  -m MUTATIONS [MUTATIONS ...], --mutations MUTATIONS [MUTATIONS ...]
                        List of rate of mutations in each configuration
                        (default: [0.001])
  --ks KS [KS ...]      List of the 'K' hyperparameters for the KSP
                        (K-ShortestPath) Algorithm (default: [8])
  --intervals INTERVALS [INTERVALS ...]
                        List of intervals that signal the frequency the QL
                        values are supposed to be fed into GA (default:
                        [None])
  --repetitions REPETITIONS
                        How many times it should be repeated (default: 1)
  --net [NETWORK_NAME]  Which network should be used (default: OW10_1)
  --experimentType {1,2,3,4}
                        1 - QL only 2 - GA only 3 - QL builds solution for GA
                        4 - GA and QL exchange solutions (default: 1)
  -e ELITE_SIZE, --elite_size ELITE_SIZE
                        How many elite individuals should be kept after each
                        generation (default: 5)
  --number-of-processes NUMBER_OF_PROCESSES
                        How many parallel processes should be used to run the
                        experiment configurations (default: 1)
  --ql-table-initiation {zero,coupling,random}
                        Defines what values the QL-table will be initiated with.(default: zero)
```
