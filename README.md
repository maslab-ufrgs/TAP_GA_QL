Script to run the simulation of drivers going from different points in the
OW and SF networks

Can get other networks from
===========================
 * [Networks](https://github.com/maslab-ufrgs/network-files)

Warning
=======

> The cost functions used for edge travel time avaliation are tied to the network being run (SF or OW10_1). If you are 
> going to use other networks, you most likely want to edit the calculateEdgesTravelTimesNew function in the experiment.py module.

Dependencies
============
 * [Python 2.7](https://www.python.org/downloads/)
 * [Pyevolve](https://sourceforge.net/projects/pyevolve/)
 * [Python Mathematical Expression Evaluator](https://pypi.python.org/pypi/py_expression_eval)
 * [matplotlib](http://matplotlib.org/)
 * [NumPy](http://www.numpy.org/)

Usage
=====

```sh
python route_choice.py [OPTIONS]
```
Or:
```sh
./route_choice.py [OPTIONS]
```

All the options have usable defaults so check them before running a experiment.

Use:

```sh
python route_choice.py -h
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
  
* First get the SF network file from the link above.

```sh
python route_choice.py -f /path/to/SF.net --printPairOD
```

* Run an experiment with the *OW* network printing the link's travel time at every
100 generations with the mutations of 0.003 and 0.03

* First get the OW network file from the link above.
```sh
python route_choice.py -f /path/to/OW.net --printTravelTime --printInterval 100 --mutations 0.003 0.03
```

* Run an experiment with the *SF* network using alphas 0.3 and 0.4,
decays 0.9 and 0.99 and 1000 generations.

```sh
python route_choice.py -f /path/to/SF.net --alphas 0.3 0.4 --decays 0.9 0.99 --generations 1000
```

* Run an QL experiment with the *OW* network initiating the QL-table with random values.

```sh
python route_choice.py -f /path/to/OW.net --experimentType 1 --ql-table-initiation random
```

Options
=======

```
optional arguments:
   -h, --help            show this help message and exit
  -f FILE               The network file. (default: None)
  --experimentType {1,2,3,4}
                        1 - QL only; 2 - GA only; 3 - QL builds solution for
                        GA; 4 - GA and QL exchange solutions. (default: 1)
  --repetitions REPETITIONS
                        How many times it should be repeated. (default: 1)
  --ks KS [KS ...]      List of the 'K' hyperparameters for the KSP
                        (K-ShortestPath) Algorithm. (default: [8])
  -g GENERATIONS, --generations GENERATIONS
                        Generations\episodes in each configuration. (default:
                        100)
  --grouping GROUPING [GROUPING ...]
                        List of group sizes for drivers in each configuration.
                        This parameter is useful when the number of
                        trips/drivers is huge; it sets how many drivers form a
                        group; in a group all drivers/trips use the same OD
                        pair, i.e., the granularity of the route choice can be
                        individual based or group based. (default: [1])
  --printTravelTime     Print link's travel time at each iteration in the
                        output file. (default: False)
  --printDriversPerRoute
                        Print the amount of drivers per route for each OD
                        pair(Warning:QL only! Also, note that the number of OD
                        pairs can be very large!). (default: False)
  -d, --printDriversPerLink
                        Print the number of drivers in each link in the output
                        file. (default: False)
  --printEdges          Print the travel time per edge. (default: False)
  -o, --printODpair     Print the average travel time in the header in the
                        output file. (default: False)
  -i PRINTINTERVAL, --printInterval PRINTINTERVAL
                        Interval by which the messages are written in the
                        output file. (default: 1)
  -e ELITE_SIZE, --elite_size ELITE_SIZE
                        How many elite individuals should be kept after each
                        generation. (default: 5)
  -p POPULATION, --population POPULATION
                        Size of population for the genetic algorithm.
                        (default: 100)
  -c CROSSOVERS [CROSSOVERS ...], --crossovers CROSSOVERS [CROSSOVERS ...]
                        List of rate of crossover in the population in each
                        configuration. (default: [0.2])
  -m MUTATIONS [MUTATIONS ...], --mutations MUTATIONS [MUTATIONS ...]
                        List of rate of mutations in each configuration.
                        (default: [0.001])
  --exchangeGAQL EXCHANGEGAQL [EXCHANGEGAQL ...]
                        Frequency with which the GA sends its best solution to
                        the QL. (default: [10])
  -tff TABLE_FILL_FILE  Table fill file. (default: None)
  --ql-table-initiation {zero,coupling,random,fixed}
                        How to initiate the Q-Table. (default: zero)
  --max MAX             Maximum value for the random initiation. Note that the
                        random value(x) will be x <= max ! (default: 0.0)
  --min MIN             Maximum value for the random initiation. Note that the
                        random value(x) will be min <= x ! (default: 0.0)
  --fixed FIXED         Fixed value for generating the Q table. (default: 0.0)
  -n FLOW [FLOW ...], --flow FLOW [FLOW ...]
                        List of numbers of drivers used to evaluate the link
                        costs, when the KSP is computed (default: [0])
  -epl EPSILON [EPSILON ...], --epsilon EPSILON [EPSILON ...]
                        List of epsilons(exploration/exploitation rate) for
                        Q-Learning. (default: [1.0])
  -a ALPHAS [ALPHAS ...], --alphas ALPHAS [ALPHAS ...]
                        List of learning rates in each configuration.
                        (default: [0.5])
  --decays DECAYS [DECAYS ...]
                        List of decays in each configuration; this sets the
                        value by which epsilon is multiplied at each QL
                        episode. (default: [0.99])
```
