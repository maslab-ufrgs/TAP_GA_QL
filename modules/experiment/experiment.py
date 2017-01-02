#!/usr/bin/env python
"""
    Use spaces instead of tabs, or configure your editor to transform tab to 4
    spaces.
"""
#Standard modules
import os
from time import localtime
import string
#Third-party module
from py_expression_eval import Parser
#Local modules
from modules.genetic_algorithm.genetic_algorithm import *
from modules.q_learning.q_learning import *
import modules.ksp.function as KSP


class Driver(object):
    '''
    Represents a driver in the network.

    Input:
    od: OD = instance of OD class

    >>> type(Driver(OD(1, 2, 8, 15)))
    <class '__main__.Driver'>
    '''

    def __init__(self, OD):
        """
        Class constructor.

        >>> isinstance(Driver(OD(1, 2, 8, 15)), Driver)
        True
        >>> isinstance(Driver(1), Driver)
        True
        >>> isinstance(Driver(OD(1, 2, 8, 15)).od, OD)
        True

        The class contructor needs to be more precise about its input.
        """
        self.od = OD

    def od_s(self):
        """
        String of OD pair of the Driver.
        Could be substituted by the __repr__ method.

        >>> Driver(1).od_s()
        Traceback (most recent call last):
        ...
        AttributeError: 'int' object has no attribute 'o'
        >>> Driver(OD(1, 2, 8, 15)).od_s()
        '12'
        """
        return "%s%s" % (self.od.o, self.od.d)

    def __repr__(self):
        """
        __repr__ method override.

        >>> Driver(OD(1, 2, 8, 15))
        '1|2'
        """
        return repr(str(self.od.o) + '|' + str(self.od.d))


class OD(object):
    """
    Represents an origin-destination pair, where:

    Inputs:
    origin: string = origin node
    destiny: string = destination node
    num_path: int = number of shortest paths to generate
    num_travels: int = number of travels

    Tests to verify the attributes:
    >>> isinstance(OD('A', 'B', 5, 100), OD)
    True
    >>> type(OD('A', 'B', 5, 100))
    <class '__main__.OD'>
    >>> isinstance(OD(1, 2, 3, 4).o, int)
    True
    >>> isinstance(OD('A', 'B', 5, 100).o, str)
    True

    Tests #3 and #4 sugests that self.o and self.d need to be more strictly
    controlled perhaps converting the O and the D to a string is a solution.

    ** OD notation: origin|destiny
    """

    def __init__(self, origin, destiny, num_paths, num_travels):
        """
        Class Constructor.

        >>> OD('A', 'B', 5, 100).o
        'A'
        >>> OD('A', 'B', 5, 100).d
        'B'
        >>> OD('A', 'B', 5, 100).numPaths
        5
        >>> OD('A', 'B', 5, 100).numTravels
        100
        >>> OD('A', 'B', 5, 100).paths
        """
        self.o = origin
        self.d = destiny
        self.numPaths = num_paths
        self.numTravels = num_travels
        self.paths = None

    def __str__(self):
        """
        __str__ method override.

        >>> print OD('A', 'B', 5, 100)
        Origin: A, Destination: B, Number of travels: 100, Number of shortest paths: 5
        """
        return "Origin: " + str(self.o) + ", Destination: " + str(self.d) + \
            ", Number of travels: " + str(self.numTravels) + ", Number of shortest paths: " \
            + str(self.numPaths)


class Node(object):
    '''
    Represents a node in the graph.

    Input:
    name: string = name of the node

    These are the tests to verify if the object is being instantiated as it should:
    >>> isinstance(Node('nome'), Node)
    True
    >>> isinstance(Node(1).name, int)
    True
    >>> isinstance(Node('nome').name, str)
    True
    >>> type(Node(1))
    <class '__main__.Node'>

    Tests #2 and #3 have the same observation as the tests #7 and #8 of the OD class.
    '''

    def __init__(self, name):
        """
        Class constructor.

        >>> Node('nome').name
        'nome'
        >>> Node('nome').dist
        1000000
        >>> Node('nome').prev
        >>> Node('nome').flag
        0
        """
        self.name = name
        self.dist = 1000000  # distance to this node from start node (?)
        self.prev = None     # previous node to this node
        self.flag = 0        # access flag

    def __repr__(self):
        """
        __repr__ method override.

        >>> Node(1)
        1
        >>> Node('nome')
        'nome'
        """
        return repr(self.name)


class Edge(object):
    """
    Represents an edge in the graph.

    Inputs:
    start: string = start node of the edge
    end: string = end node of the edge
    length: float = length of the edge
    cost_formula: string = cost formula of the edge
    var_value: float = value for the function to calculate the cost_formula

    >>> isinstance(Edge('a', 'b', 11, '12+5*t'), Edge)
    True
    >>> type(Edge('a', 'b', 11, '12+5*t'))
    <class '__main__.Edge'>

    ** Edge notation: origin-destiny
    """

    def __init__(self, start, end, length, cost_formula):
        """
        Class constructor.

        >>> Edge('a', 'b', 11, '12+5t').start
        'a'
        >>> Edge('a', 'b', 11, '12+5t').end
        'b'
        >>> Edge('a', 'b', 11, '12+5t').length
        11
        >>> Edge('a', 'b', 11, '12+5*t').cost_formula
        '12+5*t'
        """
        self.start = start
        self.end = end
        self.length = length  # FreeFlow of the edge (?)
        self.cost_formula = cost_formula

    def eval_cost(self, var_value):
        """
        The eval_cost method calculates the value of the cost formula for a given var_value:

        WARNING: the variable in the function MUST be f.
        >>> Edge(1, 2, 3, '5+5*f').eval_cost(5.0)
        30.0
        >>> Edge(1, 2, 3, '5+5*t').eval_cost(5.0)
        Traceback (most recent call last):
        ...
        Exception: undefined variable: t
        """
        parser = Parser()
        exp = parser.parse(self.cost_formula)
        #Hardcoded variable 'f'
        return exp.evaluate({'f': var_value})

    def __repr__(self):
        """
        __repr__ method override.

        >>> Edge('a','k', 11, '12+5*t')
        'a-k'
        >>> Edge(1,2,11,'12+5*t')
        '1-2'
        """
        return repr(str(str(self.start) + '-' + str(self.end)))


def is_number(arg):
    '''
    This function try to convert whatever is its argument to a float number.

    Input:
    arg: anything = the object that it tries to convert to a number.

    Output:
    True if it converts successfully to a float.
    False if it can't, by getting a ValueError exception.

    >>> is_number(1)
    True
    >>> is_number(1e1000)
    True
    >>> is_number('5000')
    True
    >>> is_number(3.141598)
    True
    >>> is_number('a')
    False
    >>> is_number('hello')
    False
    >>> is_number(Node('a'))
    Traceback (most recent call last):
    ...
    TypeError: float() argument must be a string or a number
    '''

    try:
        float(arg)
        return True
    except ValueError:
        return False

def generate_table_fill(coupling_file):
    """
    Read the coupling file contents and create the table fill.

    In:
    coupling_file:string = path to coupling file.

    Out:
    table_fill:dictionary = table fill.
    """
    table_fill = {}
    for line in open(coupling_file, 'r'):
        if line.strip() != '':
            line = line.split()
            if '#' not in line[0]:
                list_values = []
                for value in line:
                    if value != line[0]:
                        list_values.append(float(value))
                table_fill[line[0]] = list_values

    return table_fill


class Experiment(object):
    '''
    Sets up an experiment.

    >>> isinstance(Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1'), Experiment)
    True
    >>> type(Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1'))
    <class '__main__.Experiment'>
    '''

    def __init__(self, k, net_file, group_size, net_name, print_edges, table_fill_file='',
                 flow=0, p_travel_time=False, p_drivers_link=False,
                 p_od_pair=False, p_interval=1, epsilon=1,
                 p_drivers_route=False, TABLE_INITIAL_STATE='zero'):

        """
        Construct the experiment.

        Inputs:
        k: integer =  List of the 'K' hyperparameters for the KSP (default: [8])
        net_file: file = .net file in the ./networks/ folder
        group_size: integer = List of group sizes for drivers in each configuration (default: [1])
        net_name: string = The name of the network to be used (default: OW10_1)
        p_travel_time: boolean = Print link's travel time of the iteration on the file
        p_drivers_link: boolean = Print the number of drivers in each link in the output file
        p_od_pair: boolean = Print the average travel time for in the header in the output file
        p_interval: integer = Interval by which the messages are written in the output file
        p_drivers_route: boolean = Print the amount of drivers per route of each OD pair
        TABLE_INITIAL_STATE: string = Table initial states can be 'zero', 'coupling' and 'random'

        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1').group_size
        1
        >>> Experiment(8, './networks/OW10_1/1.net', 1, 'OW10_1')
        Traceback (most recent call last):
        ...
        IOError: [Errno 2] No such file or directory: './networks/OW10_1/1.net'
        """

        self.k = k
        self.epsilon = epsilon
        self.group_size = group_size
        self.printDriversPerLink = p_drivers_link
        self.printTravelTime = p_travel_time
        self.printODpair = p_od_pair
        self.printInterval = p_interval
        self.printDriversPerRoute = p_drivers_route
        self.TABLE_INITIAL_STATE = TABLE_INITIAL_STATE
        self.network_name = net_name
        self.edges = {}
        self.flow = flow
        self.init_network_data(self.k, net_file, self.group_size, self.flow, print_edges)
        self.TABLE_FILL = {}
        if TABLE_INITIAL_STATE == 'coupling':
            self.TABLE_FILL = generate_table_fill(table_fill_file)

    def generate_graph(self, graph_file, print_edges = False, flow = 0.0):
        """
        Reads the .net file and return it's infos.
        The infos are:
            function(s)
            node(s)
            arc(s)
            edge(s)
            od(s)

        It should be following the specification from:
            https://wiki.inf.ufrgs.br/Network_files_specification

        It returns a list of vertices(V), a list of edges(E) and a list of OD(ODlist)

        Tests:
        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW').\
                generate_graph('./networks/OW10_1/OW10_1.net') #doctest:+NORMALIZE_WHITESPACE
        (['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'], ['A-B', 'B-A', 'A-C', \
         'C-A', 'A-D', 'D-A', 'B-D', 'D-B', 'B-E', 'E-B', 'C-D', 'D-C', 'C-F', 'F-C', 'C-G', 'G-C',\
         'D-E', 'E-D', 'D-G', 'G-D', 'D-H', 'H-D', 'E-H', 'H-E', 'F-G', 'G-F', 'F-I', 'I-F', 'G-H',\
         'H-G', 'G-J', 'J-G', 'G-K', 'K-G', 'H-K', 'K-H', 'I-J', 'J-I', 'I-L', 'L-I', 'J-K', 'K-J',\
         'J-L', 'L-J', 'J-M', 'M-J', 'K-M', 'M-K'], [('A', 'L', 600), ('A', 'M', 400),\
         ('B', 'L', 300), ('B', 'M', 400)])

        In order: The vertice list, edge list and the OD list.
        Vertices -> ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

        Edges -> ['A-B', 'B-A', 'A-C', 'C-A', 'A-D', 'D-A', 'B-D', 'D-B', 'B-E', 'E-B', 'C-D',
                  'D-C', 'C-F', 'F-C', 'C-G', 'G-C', 'D-E', 'E-D', 'D-G', 'G-D', 'D-H', 'H-D',
                  'E-H', 'H-E', 'F-G', 'G-F', 'F-I', 'I-F', 'G-H', 'H-G', 'G-J', 'J-G', 'G-K',
                  'K-G', 'H-K', 'K-H', 'I-J', 'J-I', 'I-L', 'L-I', 'J-K', 'K-J', 'J-L', 'L-J',
                  'J-M', 'M-J', 'K-M', 'M-K']

        OD -> [('A', 'L', 600), ('A', 'M', 400), ('B', 'L', 300), ('B', 'M', 400)]
        """
        vertices = []
        edges = []
        functions = {}
        od_list = []
        for line in open(graph_file, 'r'):
            taglist = string.split(line)
            if taglist[0] == 'function':
                variables = []
                variables = taglist[2].replace("(", "")
                variables = variables.replace(")", "")
                variables = variables.split(",")
                functions[taglist[1]] = [taglist[3], variables]

            elif taglist[0] == 'node':
                vertices.append(Node(taglist[1]))

            elif taglist[0] == 'dedge' or taglist[0] == 'edge':
                constants = []
                cost_formula = ""
                freeflow_cost = 0
                constant_acc = 0
                if len(taglist) > 5:
                    i = 5
                    while i <= (len(taglist) - 1):
                        constants.append(taglist[i])
                        i += 1
                    parser = Parser()
                    ##[4] is function name.[0] is expression
                    exp = parser.parse(functions[taglist[4]][0])
                    LV = exp.variables()
                    buffer_LV = []
                    for l in LV:
                        if l not in functions[taglist[4]][1]:
                            constant_acc += 1
                            buffer_LV.append(l)

                    #check if the formula has any parameters(variables)
                    flag = False
                    for v in functions[taglist[4]][1]:
                        if v in LV:
                            flag = True

                    buffer_dic = {}
                    i = 0
                    for index in range(constant_acc):
                        buffer_dic[buffer_LV[index]] = float(constants[index])
                        i = 1

                    if not flag:
                        freeflow_cost = exp.evaluate(buffer_dic)
                        cost_formula = str(freeflow_cost)

                    elif is_number(functions[taglist[4]][0]):
                        freeflow_cost = float(functions[taglist[4]][0])
                        cost_fomula = functions[taglist[4]][0]

                    else:
                        exp = exp.simplify(buffer_dic)
                        cost_formula = exp.toString()
                        exp = Parser()
                        cost_formula2 = "(" + cost_formula + ") + flow"
                        exp = exp.parse(cost_formula2)
                        freeflow_cost = exp.evaluate({'f': 0, 'flow': flow})  # Hardcoded

                    edges.append(Edge(taglist[2], taglist[3],
                                      freeflow_cost, cost_formula))
                    if taglist[0] == 'edge':
                        edges.append(Edge(taglist[3], taglist[2],
                                          freeflow_cost, cost_formula))

                else:
                    cost_formula = ""
                    freeflow_cost = 0
                    parser = Parser()
                    if is_number(functions[taglist[4]][0]):
                        cost_formula = functions[taglist[4]][0]
                        freeflow_cost = float(functions[taglist[4]][0])

                    else:
                        exp = parser.parse(functions[taglist[4]][0])
                        cost_formula = exp.toString()
                        cost_formula2 = "(" + cost_formula + ") + flow"
                        exp = exp.parse(cost_formula2)
                        freeflow_cost = exp.evaluate({'f': 0, 'flow': flow})  # hardcoded

                    edges.append(Edge(taglist[2], taglist[3],
                                      freeflow_cost, cost_formula))
                    edges.append(Edge(taglist[3], taglist[2],
                                      freeflow_cost, cost_formula))

            elif taglist[0] == 'od':
                od_list.append((taglist[2], taglist[3], int(taglist[4])))
        '''
        Print edges but there are too many lines to be printed!!
        '''
        if print_edges:
            for e in edges:
                print("Edge " + str(e.start) + "-"
                      + str(e.end) + " has length: " + str(e.length))


        return vertices, edges, od_list

    def init_network_data(self, k, network_file, group_size, flow, print_edges):
        """
        Initialize the network data.

        Inputs:
        k: integer = Number of KSP routes to generate
        network_file: file = .net file
        group_size: integer = Size of the grouping

        This method set some of the attributes of the experiment but doesn't help much because
        there are some attributes being set ''outside'' the class contructor method.
        Needs to be changed in the future.
        """
        self.ODlist = []
        self.ODL = []
        self.ODheader = ""
        self.ODtable = {}

        self.Vo, self.Eo, odInputo = self.generate_graph(network_file, print_edges = print_edges, flow = flow)

        for tup_od in odInputo:
            if tup_od[2] % self.group_size != 0:
                print tup_od[2]
                raise Exception("Error: number of travels is not a multiple \
                                 of the group size origin: " + str(tup_od[0])
                                + " destination: " + str(tup_od[1]))
            else:
                #Origin, destination, number of paths, number of travels
                self.ODlist.append(OD(tup_od[0], tup_od[1],
                                      k, tup_od[2] / self.group_size))
                self.ODL.append(str(tup_od[0]) + str(tup_od[1]))
                for i in range(k):
                    if len(self.ODheader) == 0:
                        self.ODheader = self.ODheader \
                            + str(tup_od[0]) + "to" + str(tup_od[1]) \
                            + "_" + str(i + 1)
                    else:
                        self.ODheader = self.ODheader + " " + str(tup_od[0]) \
                            + "to" + str(tup_od[1]) + "_" + str(i + 1)

        for od_pair in self.ODL:
            list_routes = []
            for i in range(self.k):
                list_routes.append(0)
            self.ODtable[str(od_pair)] = list_routes

        #Get the k shortest routes
        #print "getKRoutes"
        for od_pair in self.ODlist:
            od_pair.paths = KSP.getKRoutes(self.Vo, self.Eo, od_pair.o,
                                           od_pair.d, od_pair.numPaths)

        ##get the value of each link - free flow travel time
        self.freeFlow = {}
        for edge in self.Eo:
            self.freeFlow[edge.start + "|" + edge.end] = edge.length

        self.edgeNames = sorted(self.freeFlow.keys())

        #creates different drivers according to the number of travels of each OD
        #instance
        self.drivers = []
        for od_pair in self.ODlist:
            for i in range(od_pair.numTravels):
                self.drivers.append(Driver(od_pair))

    def __repr__(self):
        """
        __repr__ method override.

        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1')
        'Experiment: k = 8, net_name = OW10_1'
        """
        return repr(str('Experiment: k = ' + str(self.k) + ', net_name = ' + (self.network_name)))

    def __clean_od_table(self):
        """
        Zeroes the OD table.
        In the future, it needs to be changed when used in the program.

        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1') \
            .ODtable #doctest: +NORMALIZE_WHITESPACE
        {'BL': [0, 0, 0, 0, 0, 0, 0, 0], 'BM': [0, 0, 0, 0, 0, 0, 0, 0], \
         'AM': [0, 0, 0, 0, 0, 0, 0, 0], 'AL': [0, 0, 0, 0, 0, 0, 0, 0]}
        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1'). \
            _Experiment__clean_od_table() #doctest: +NORMALIZE_WHITESPACE
        {'BL': [0, 0, 0, 0, 0, 0, 0, 0], 'BM': [0, 0, 0, 0, 0, 0, 0, 0], \
         'AM': [0, 0, 0, 0, 0, 0, 0, 0], 'AL': [0, 0, 0, 0, 0, 0, 0, 0]}


        """
        for od_pair in self.ODL:
            self.ODtable[str(od_pair)] = [0] * self.k

        return self.ODtable

    def genCallBack(self, ga_engine):
        """
        GA stuff. Not ready for it yet, assuming it is working as it should.
        """
        population = ga_engine.getPopulation()
        generation = ga_engine.getCurrentGeneration()
        if self.printDriversPerRoute:
            #Drivers per route
            for od in self.ODL:
                self.ODtable[str(od)] = [0] * self.k

        #gets worst individual
        worstsol = population[len(population) - 1]

        if self.useQL:  # if using QL
            #check if the GA->QL interval is None
            if self.interval is None:
                isGeneration = 1
            else:
                isGeneration = (generation + 1) % self.interval

            #check if we are running the GA<->QL or GA<-QL experiment.
            if self.useInterval and (isGeneration == 0) and (generation != 0):
                (qlind, avg_tt) = \
                    self.ql.runEpisodeWithAction(ga_engine.bestIndividual().getInternalList())
                    #GA->QL
            else:
                (qlind, avg_tt) = self.ql.runEpisode()  # GA<-QL
                #qlind is a array of paths taken by each driver

            #for each driver
            for i in range(len(qlind)):
                worstsol.getInternalList()[i] = qlind[i]
            worstsol.evaluate()

            #if worstscore has a smaller average travel time than the
            #best individual, copies the ql solution (worstscore)
            #to the second best individual
            if worstsol.score < ga_engine.bestIndividual().score:
                print(">>>>> QL indiv. "+ str(worstsol.score), "turned better than best ind. "
                      + str(ga_engine.bestIndividual().score)+ "at generation "+ str(generation))
                #copies QL solution to 2nd best ind.
                worstsol.copy(ga_engine.getPopulation()[1])
                ga_engine.getPopulation()[1].evaluate()
            else:
                #copies QL solution to worst in population
                worstsol.copy(ga_engine.getPopulation()[1])
                ga_engine.getPopulation()[len(population) - 1].evaluate()

        self.__print_step(generation, ga_engine.bestIndividual().getInternalList(),
                          avgTT=ga_engine.bestIndividual().score, qlTT=worstsol.score)

    def build_od_pair_data(self, ttByOD):
        """
        Returns the string of OD pair data for each OD.
        Not tested yet, need to test QL module first.
        """
        str_od = ''
        for k in ttByOD.keys():
            if len(ttByOD[k]) == 0:
                str_od = '0'
            else:
                str_od += " %4.4f" % (sum(ttByOD[k]) / len(ttByOD[k]))

        return str_od + ' '

    def __print_step(self, step_number, stepSolution, avgTT=None, qlTT=None):
        """
        Write infos to the output file.
            step_number:int = episode/generation
            step_solution:QL = instance of QL class.
        """

        if step_number % self.printInterval == 0:
            if self.useGA:
                if self.useQL:
                    self.outputFile.write(str(step_number) + " " + str(avgTT) +" "+ str(qlTT))
                else:
                    self.outputFile.write(str(step_number) + " " + str(avgTT))
            else:
                self.outputFile.write(str(step_number) + " " + str(qlTT))

            if self.printODpair:
                ttByOD = self.travelTimeByOD(stepSolution)
                self.outputFile.write(self.build_od_pair_data(ttByOD))

            if self.printTravelTime:
                travel_times = ''
                edges = self.calculateEdgesTravelTimesNew(stepSolution)
                for edge in self.edgeNames:
                    travel_times += str(edges[edge]) + " "
                self.outputFile.write(travel_times.strip() + " ")

            if self.printDriversPerLink:
                drivers = ''
                edges = self.driversPerLink(stepSolution)
                for edge in self.edgeNames:
                    drivers += str(edges[edge]) + " "
                self.outputFile.write(drivers.strip())

            if self.printDriversPerRoute:
                self.__clean_od_table()
                for s in range(len(stepSolution)):
                    self.ODtable[str(self.drivers[s].od.o)
                                 + str(self.drivers[s].od.d)][stepSolution[s]] += 1
                    #print self.ODtable
                self.outputFile.write(" ")
                for keys in self.ODL:  # Now it prints in the correct order
                    for x in range(len(self.ODtable[keys])):
                        #string = string + str(ODtable[keys][x])
                        self.outputFile.write(str(self.ODtable[keys][x]) + " ")

            self.outputFile.write("\n")

    def nodes_string(self):
        """
            String of edges of the graph that will be printed or stored in the file.
        """
        nodes_string = ''
        if self.printODpair:
            for od in self.ODlist:
                nodes_string += "tt_%s|%s " % (od.o, od.d)
        if(self.printTravelTime):
            for edgeN in self.edgeNames:
                nodes_string += 'tt_' + edgeN + ' '
        if(self.printDriversPerLink):
            for edgeN in self.edgeNames:
                nodes_string += "nd_" + edgeN + ' '
        if(self.printDriversPerRoute):
            nodes_string += self.ODheader
        nodes_string = nodes_string.strip()
        return nodes_string

    def nd(self):
        """
        Number of drivers.
        """
        return len(self.drivers) * self.group_size

    def appendTag(self, filenamewithtag):
        """
            Test if there isn't already a file with the desired name,
            paralellization of experiments may result in filename conflict.
        """
        append_number = ''
        while(os.path.isfile(filenamewithtag + append_number + ".txt")):
            if(append_number == ''):
                append_number = "-1"
            else:
                append_number = "-" + str(int(append_number[1:]) + 1)
        filenamewithtag += append_number + ".txt"
        return filenamewithtag

    def createStringArgumentsQL(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path2simulationfiles:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_gaql_grouped/net_%s/QL/decay%4.3f/alpha%3.2f"
        path2simulationfiles = fmt % (self.network_name, self.decay, self.alpha)

        filename = path2simulationfiles + '/' + self.network_name \
            + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
            + '_'+ str(localtime()[3]) + 'h' + str(localtime()[4]) + 'm' + str(localtime()[5]) + 's'

        headerstr = '#Parameters:' + '\n\tk = ' + str(self.k) + '\t\tAlpha = ' + str(self.alpha) \
            + '\n\tDecay = ' + str(self.decay) + '\tNumber of drivers = ' + str(nd) \
            + '\n\tGroup size = ' + str(self.group_size) + '\tQL Table init = ' \
            + str(self.TABLE_INITIAL_STATE) + '\n\tEpsilon = ' + str(self.epsilon) \
            + '\n#Episode AVG_TT ' + self.nodes_string()

        return filename, path2simulationfiles, headerstr

    def createStringArguments(self, useQL, useInt):
        if(useQL and useInt):
            fmt = "./results_gaql_grouped/net_%s/GA<->QL/" \
                   + "pm%4.4f/decay%4.3f/alpha%3.2f/QL<-GA_Interval%s"
            path2simulationfiles = fmt % (self.network_name, self.mutation,
                                          self.decay, self.alpha, self.interval)

            filenamewithtag = path2simulationfiles + '/net' + self.network_name + '_pm'\
                + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.group_size) \
                + '_interval'+ str(self.interval) + '_' + str(localtime()[3]) + 'h' \
                + str(localtime()[4]) + 'm' + str(localtime()[5]) + 's'

            headerstr = "#Parameters:" "\n\tGen. = " + str(self.generations) + "\t\tPop. = " \
                + str(self.population) + "\n\tMutation = " + str(self.mutation) \
                + "\tCrossover = " + str(self.crossover) + "\n\tElite = " + str(self.elite) \
                + "\t\tk = " + str(self.k) + "\n\tAlpha = " + str(self.alpha) + "\t\tDecay = " \
                + str(self.decay) + "\n\tNumber of drivers = " + str(self.nd()) + "\tGroup size = "\
                + str(self.group_size) + "\n\tGA->QL interval=" + str(self.interval) \
                + "\t\tEpsilon = " + str(self.epsilon) + "\n\tQL Table init = " \
                + str(self.TABLE_INITIAL_STATE) + "\n#Generation avg_tt ql_avg_tt " \
                + self.nodes_string()

        elif(useQL):
            fmt = "./results_gaql_grouped/net_%s/GA<-QL/pm%4.4f/decay%4.3f/alpha%3.2f"
            path2simulationfiles = fmt % (self.network_name, self.mutation,
                                          self.decay, self.alpha)

            filenamewithtag = path2simulationfiles + '/net' + self.network_name + '_pm' \
                + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay) \
                + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.group_size) + '_' \
                + str(localtime()[3]) + 'h' + str(localtime()[4]) + 'm' + str(localtime()[5]) +'s'

            headerstr = "#Parameters:" + "\n\tGen. = " + str(self.generations) + "\t\tPop. = " \
                + str(self.population) + "\n\tMutation = " + str(self.mutation) \
                + "\tCrossover = " + str(self.crossover) + "\n\tElite = " + str(self.elite) \
                + "\t\tk = " + str(self.k) + "\n\tAlpha = " + str(self.alpha) + "\t\tDecay = " \
                + str(self.decay) + "\n\tNumber of drivers = " + str(self.nd()) + "\tGroup size = "\
                + str(self.group_size) + "\n\tEpsilon = " + str(self.epsilon) + "\t\tTable init = "\
                + str(self.TABLE_INITIAL_STATE) + "\n#Generation avg_tt ql_avg_tt " \
                + self.nodes_string()

        else:
            fmt = "./results_gaql_grouped/net_%s/GA/pm%4.4f"
            path2simulationfiles = fmt % (self.network_name, self.mutation)

            filenamewithtag = path2simulationfiles + '/net' + self.network_name + '_pm'\
                + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                + '_k' + str(self.k) + '_nd'+ str(self.nd()) + '_groupsize' \
                + str(self.group_size) + '_' + str(localtime()[3]) + 'h' \
                + str(localtime()[4]) + 'm' + str(localtime()[5]) + 's'

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                + str(self.population) + ' mutation=' + str(self.mutation)\
                + ' crossover=' + str(self.crossover) \
                + ' groupsize= '+ str(self.group_size) + " k= " + str(self.k) \
                + '\n#generation avg_tt ' + self.nodes_string()

        return filenamewithtag, path2simulationfiles, headerstr

    def run_ql(self, num_episodes, alpha, decay):
        self.useGA = False
        self.useQL = True
        self.alpha = alpha
        self.decay = decay
        self.ql = QL(self, self.drivers, self.k, self.decay, self.alpha, self.TABLE_FILL, self.epsilon,
                     self.TABLE_INITIAL_STATE)  # Change for "coupling" to use TABLE_FILL

        filename, path2simulationfiles, headerstr = self.createStringArgumentsQL(len(self.drivers))
        filenamewithtag = self.appendTag(filename)

        if os.path.isdir(path2simulationfiles) is False:
            os.makedirs(path2simulationfiles)

        self.outputFile = open(filenamewithtag, 'w')
        self.outputFile.write(headerstr + '\n')

        for episode in range(num_episodes):
            (instance, value) = self.ql.runEpisode()
            self.__print_step(episode, instance, qlTT=value)

        print("Output file location: %s" % filenamewithtag)

        self.outputFile.close()

    def run_ga_ql(self, useQL, useInt, generations, population, crossover, mutation, elite, alpha,
                  decay, interval):
        self.useGA = True
        self.useQL = useQL
        self.useInterval = useInt
        self.interval = interval
        self.generations = generations
        self.population = population
        self.crossover = crossover
        self.mutation = mutation
        self.elite = elite
        self.alpha = alpha
        self.decay = decay
        if(useQL):
            self.ql = QL(self, self.drivers, self.k, self.decay, self.alpha,
                         self.TABLE_FILL, self.epsilon, self.TABLE_INITIAL_STATE)

        filename, path2simulationfiles, headerstr = self.createStringArguments(useQL, useInt)
        filenamewithtag = self.appendTag(filename)

        ##creates file
        if os.path.isdir(path2simulationfiles) is False:
            os.makedirs(path2simulationfiles)

        self.outputFile = open(filenamewithtag, 'w')
        self.outputFile.write(headerstr + '\n')

        self.ga = GA(generations, population, crossover, mutation, elite, self,
                     self.genCallBack, self.calculateAverageTravelTime, self.drivers)
        self.ga.evolve()

        print("Output file location: %s" % filenamewithtag)
        self.outputFile.close()

    def driversPerLink(self, driverString):
        """
        receives an array of ints stresenting the chosen path of each group
        the array is sorted in the same way as the alleles and the drivers
        list
        returns a dicionary where the keys are edges and the values are the
        amount of drivers on the edge
        """
        global drivers
        global freeFlow
        global group_size
        dicti = {}
        for inx, dr in enumerate(driverString):
            if(type(dr) != int):
                print('problema!', driverString, '\n')
            path = self.drivers[inx].od.paths[dr]
            for edge in path[0]:
                if edge in dicti.keys():
                    dicti[edge] +=self.group_size
                else:
                    dicti[edge] = self.group_size
        for link in self.freeFlow.keys():
            if link not in dicti.keys():
                dicti[link]=0
        return dicti

    def evaluateActionTravelTime(self, driverIndex, action, edgesTravelTimes):
        #calculates travel times for a driver
        traveltime = 0.0
        path = self.drivers[driverIndex].od.paths[action][0]  # list of nodes of path
        for edge in path:
            traveltime += edgesTravelTimes[edge]
        return traveltime

    def initTravelTimeByODDict(self):
        d = {}
        for od in self.ODlist:
            d["%s%s" % (od.o, od.d)] = []
        return d

    def travelTimeByOD(self, stringOfActions):
        edgesTravelTimes = self.calculateEdgesTravelTimesNew(stringOfActions)
        odTravelTimeDict = self.initTravelTimeByODDict()
        for driverIdx, action in enumerate(stringOfActions):
            path = self.drivers[driverIdx].od.paths[action][0]
            traveltime = 0.0
            for edge in path:
                traveltime += edgesTravelTimes[edge]
            odTravelTimeDict[self.drivers[driverIdx].od_s()].append(traveltime)
        return odTravelTimeDict

    def calculateIndividualTravelTime(self, stringOfActions):
        #returns list of travel times for each driver
        edgesTravelTimes = self.calculateEdgesTravelTimesNew(stringOfActions)
        results = []
        for driverIdx, action in enumerate(stringOfActions):
            travel_times = self.evaluateActionTravelTime(driverIdx, action, edgesTravelTimes)
            results.append(travel_times)
        return results

    def calculateEdgesTravelTimesNew(self, stringOfActions):
        """
        New Version
        THIS IS THE NEW EVALUATE FUNCTION(THE ONE ABOVE IS NOT USED ANYMORE)
        EACH EDGE OF THE NETWORK HAS ITS OWN COST FUNCTION NOW.
        """
        edges_travel_times = {}
        #Get the flow of that edge
        linkOccupancy = self.driversPerLink(stringOfActions)
        #For each edge
        for edge in self.Eo:
            p = Parser()
            exp = p.parse(edge.cost_formula)
            #Evaluates the cost of that edge with a given flow (i.e. edge.eval_cost(flow))
            edges_travel_times[edge.start + "|" + edge.end] = \
                edge.eval_cost(linkOccupancy[edge.start + "|" + edge.end])
        return edges_travel_times

    def calculateAverageTravelTime(self, stringOfActions):
        return sum(self.calculateIndividualTravelTime(stringOfActions)) / len(stringOfActions)


if __name__ == '__main__':
    """"
    To run the tests you should call from the terminal: python Experiment.py

    If the tests succeed, nothing should happen.  Else it will show the error
    and where it is on the file.
    """
    import doctest
    doctest.testmod()
