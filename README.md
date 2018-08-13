IMPORTANT
=========
Need to initialize the KSP submodule, to do so use the following command:
```sh
git submodule init && git submodule update
```

Can get other networks from
===========================
 * [Networks](https://github.com/maslab-ufrgs/transportation_networks)

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
arguments:
  -h, --help            show this help message and exit
  -f FILE               The network file. (default: None)
  -as {epsilon,boltzmann}, --action-selection {epsilon,boltzmann}
                        How the agents should select their actions. (default:
                        epsilon)
  -et {1,2,3,4,5,6,7,8,9,10}, --experimentType {1,2,3,4,5,6,7,8,9,10}
                        1 - QL only; 2 - GA only; 3 - QL builds solution for
                        GA; 4 - GA and QL exchange solutions. 5 - UCB1 only 6
                        - Thompson only 7 - UCB1 Discounted only 8 - UCB1
                        Sliding Window only 9 - Rexp3 10- Rexp3MA (default: 1)
  -r REPETITIONS, --repetitions REPETITIONS
                        How many times it should be repeated. (default: 1)
  -k KS [KS ...], --ks KS [KS ...]
                        List of the 'K' hyperparameters for the KSP
                        (K-ShortestPath) Algorithm. (default: [8])
  -g GENERATIONS, --generations GENERATIONS
                        Generations\episodes in each configuration. (default:
                        100)
  -n FLOW, --flow FLOW  Base flow in the network. (default: 0)
  -group GROUPING [GROUPING ...], --grouping GROUPING [GROUPING ...]
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
  --printDriversPerLink
                        Print the number of drivers in each link in the output
                        file. (default: False)
  --printEdges          Print the travel time per edge. (default: False)
  --printODpair         Print the average travel time in the header in the
                        output file. (default: False)
  --printInterval PRINTINTERVAL
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
  -i EXCHANGEGAQL [EXCHANGEGAQL ...], --exchangeGAQL EXCHANGEGAQL [EXCHANGEGAQL ...]
                        Interval of generations in which the GA sends its best
                        solution to the QL. (default: [10])
  -tff TABLE_FILL_FILE  Table fill file. (default: None)
  -qti {coupling,random,fixed}, --ql-table-initiation {coupling,random,fixed}
                        How to initiate the Q-Table. (default: fixed)
  --max MAX             Maximum value for the random initiation. Note that the
                        random value(x) will be x <= max ! (default: 0.0)
  --min MIN             Maximum value for the random initiation. Note that the
                        random value(x) will be min <= x ! (default: 0.0)
  --fixed FIXED         Fixed value for generating the Q table. (default: 0.0)
  -epl EPSILON [EPSILON ...], --epsilon EPSILON [EPSILON ...]
                        List of epsilons(exploration rate) for Q-Learning,
                        Rexp3 and Rexp3MA. (default: [1.0])
  -a ALPHAS [ALPHAS ...], --alphas ALPHAS [ALPHAS ...]
                        List of learning rates in each configuration.
                        (default: [0.5])
  -d DECAYS [DECAYS ...], --decays DECAYS [DECAYS ...]
                        List of decays in each configuration; this sets the
                        value by which epsilon is multiplied at each QL
                        episode. Also used as the discount factor on
                        Discounted UCB and Sliding window UCB, and the decay
                        rate for the probability of forgetinf of the Rexp3MA
                        algorithm (default: [0.99])
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature for the Boltzmann action selection.
                        (default: None)
  -ws WINDOWSIZE [WINDOWSIZE ...], --windowsize WINDOWSIZE [WINDOWSIZE ...]
                        Window size for Sliding Window UCB1 (default: [20])
  -io {1,2} [{1,2} ...], --initorder {1,2} [{1,2} ...]
                        How UCB-based algorithms should be initiaded: 1-random
                        order, 2-sequential order (default: [1])
  -pf PROBABILITYFORGET [PROBABILITYFORGET ...], --probabilityforget PROBABILITYFORGET [PROBABILITYFORGET ...]
                        List of probabilities of forgetting for the Rexp3MA
                        algorithms. (default: [1.0])

```
