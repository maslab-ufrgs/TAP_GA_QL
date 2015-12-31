Script to run the simulation of drivers going from different points in the
OW10_1 and SF networks

Warning
=======

> The cost functions used for edge travel time avaliation are tied to the network being run (SF or OW10_1). If you are 
> going to use other networks, you most likely want to edit the calculateTravelTime function in the Experiment.py file.

Dependencies
============
 * python 2.7
 * [pyevolve](https://sourceforge.net/projects/pyevolve/)

Usage
=====

```sh
python traffic_simulation.py [OPTIONS]
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
  --net {OW10_1,SF}     Which network should be used (default: OW10_1)
  --experimentType {1,2,3,4}
                        1 - QL only 2 - GA only 3 - QL builds solution for GA
                        4 - GA and QL exchange solutions (default: 1)
  -e ELITE_SIZE, --elite_size ELITE_SIZE
                        How many elite individuals should be kept after each
                        generation (default: 5)
  --number-of-processes NUMBER_OF_PROCESSES
                        How many parallel processes should be used to run the
                        experiment configurations (default: 1)
```
