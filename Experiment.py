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
from GA import GA
from QL import QL
import KSP

SF_NETWORK_NAME = "SF"

"""
    This is a hardcoded coupling data for an specific experiment with k=5 and
    it is used when the flag --ql-table-initiation is initiated with
    "coupling".  In the future this is needed to be read from a file.
"""

TABLE_FILL = {"A|L":[36.84, 39.47, 23.68, 30.70, 31.58],
              "A|M":[31.58, 37.89, 32.63, 22.37, 35.53],
              "B|L":[27.37, 27.63, 32.46, 33.68, 21.05],
              "B|M":[21.05, 27.63, 20.00, 18.95, 28.42]}

class Driver:
    '''
    Represents a driver in the network.

    Input:
    od: OD = instance of OD class

    >>> isinstance(Driver(OD(1, 2, 8, 15)), Driver)
    True
    >>> isinstance(Driver(1), Driver)
    True
    >>> isinstance(Driver(OD(1, 2, 8, 15)).od, OD)
    True

    The class contructor needs to be more precise about its input.
    >>> Driver(1).od_s()
    Traceback (most recent call last):
    ...
    AttributeError: 'int' object has no attribute 'o'
    >>> Driver(OD(1, 2, 8, 15)).od_s()
    '12'
    '''

    def __init__(self, OD):
        self.od = OD

    def od_s(self):
        return "%s%s" % (self.od.o, self.od.d)

class OD:
    """
    Represents an origin-destination pair, where:

    Inputs:
    O: string = origin node
    D: string = destination node
    numPath: int = number of shortest paths to generate
    numTravels: int = number of travels

    Tests to verify the attributes:
    >>> isinstance(OD('A', 'B', 5, 100), OD)
    True
    >>> OD('A', 'B', 5, 100).o
    'A'
    >>> OD('A', 'B', 5, 100).d
    'B'
    >>> OD('A', 'B', 5, 100).numPaths
    5
    >>> OD('A', 'B', 5, 100).numTravels
    100
    >>> OD('A', 'B', 5, 100).paths
    >>> isinstance(OD(1, 2, 3, 4).o, int)
    True
    >>> isinstance(OD('A', 'B', 5, 100).o, str)
    True

    Tests #7 and #8 sugests that self.o and self.d need to be more strictly controlled, perhaps converting the O  and the D to a string.

    Test for the __str__ method:
    >>> print OD('A', 'B', 5, 100)
    Origin: A, Destination: B, Number of travels: 100, Number of shortest paths: 5
    """

    def __init__(self, O, D, numPaths, numTravels):
        self.o = O
        self.d = D
        self.numPaths = numPaths
        self.numTravels = numTravels
        self.paths = None

    def __str__(self):
        return "Origin: " + str(self.o) + ", Destination: "+str(self.d) + \
                ", Number of travels: " + str(self.numTravels) + ", Number of shortest paths: " \
                + str(self.numPaths)

class Node:
    '''
    Represents a node in the graph.

    Input:
    name: string = name of the node

    These are the tests to verify if the object is being instantiated as it should:
    >>> isinstance(Node('nome'), Node)
    True
    >>> Node('nome').name
    'nome'
    >>> Node('nome').dist
    1000000
    >>> Node('nome').prev
    >>> Node('nome').flag
    0
    >>> isinstance(Node(1).name, int)
    True
    >>> isinstance(Node('nome').name, str)
    True

    Tests #6 and #7 have the same observation as the tests #7 and #8 of the OD class.
    '''

    def __init__(self, name):
        self.name = name
        self.dist = 1000000	# distance to this node from start node (?)
        self.prev = None	# previous node to this node
        self.flag = 0		# access flag

class Edge:
    '''
    Represents an edge in the graph.

    Inputs:
    u: string = start node of the edge
    v: string = end node of the edge
    length: float = length of the edge
    cost_formula: string = cost formula of the edge
    var_value: float = value for the function to calculate the cost_formula

    >>> isinstance(Edge('a', 'b', 11, '12+5*t'), Edge)
    True
    >>> Edge('a', 'b', 11, '12+5t').start
    'a'
    >>> Edge('a', 'b', 11, '12+5t').end
    'b'
    >>> Edge('a', 'b', 11, '12+5t').length
    11
    >>> Edge('a', 'b', 11, '12+5*t').cost_formula
    '12+5*t'

    The eval_cost method calculates the value of the cost formula for a given var_value:
    WARNING: the variable in the function MUST be f.
    >>> Edge(1, 2, 3, '5+5*f').eval_cost(5.0)
    30.0
    >>> Edge(1, 2, 3, '5+5*t').eval_cost(5.0)
    Traceback (most recent call last):
    ...
    Exception: undefined variable: t
    '''

    def __init__(self, u, v, length, cost_formula):
        self.start = u
        self.end = v
        self.length = length #FreeFlow of the edge (?)
        self.cost_formula = cost_formula

    def eval_cost(self, var_value):
        p = Parser()
        exp = p.parse(self.cost_formula)
        #Hardcoded variable 'f'
        return exp.evaluate({'f':var_value})

def is_number(s):
    '''
    This function try to convert whatever is its argument to a float number.

    Input:
    s: anything = the object that it tries to convert to a number.

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
    AttributeError: Node instance has no attribute '__float__'
    '''

    try:
        float(s)
        return True
    except ValueError:
        return False

class Experiment:
    '''
    Sets up an experiment.
    '''

    def __init__(self, k, networkFile, groupSize, networkName,
                 printTravelTime=False, printDriversPerLink=False,
                 printPairOD=False, printInterval=1,
                 printDriversPerRoute=False, TABLE_INITIAL_STATE='zero'):

        """
        Construct the experiment.

        Inputs:
        k: integer =  List of the 'K' hyperparameters for the KSP (default: [8])
        networkFile: file = .net file in the ./networks/ folder
        capacitiesFile: file = .capacity.txt file in the network folder
        odFile: file = .od.txt file in the network folder
        groupSize: integer = List of group sizes for drivers in each configuration (default: [1])
        networkName: string = The name of the network to be used (default: OW10_1)

        printTravelTime: boolean = Print link's travel time at each iteration in the output file (default: False)
        printDriversPerLink: boolean = Print the number of drivers in each link in the output file (default: False)
        printPairOD: boolean = Print the average travel time for in the header in the output file (default: False)
        printInterval: integer = Interval by which the messages are written in the output file (default: 1)
        printDriversPerRoute: boolean = Print the amount of drivers per route of each OD pair (Warning: QL only!) (default: False)

        TABLE_INITIAL_STATE: string = Table initial states can be 'zero', 'coupling' and 'random'

        """

        self.k = k
        self.groupSize = groupSize

        self.printDriversPerLink = printDriversPerLink
        self.printTravelTime = printTravelTime
        self.printPairOD= printPairOD
        self.printInterval = printInterval
        self.networkName = networkName
        self.networkSet = False
        self.edges = {}
        self.initializeNetworkData(self.k, networkFile, self.groupSize)
        self.printDriversPerRoute = printDriversPerRoute #New flag
        self.TABLE_INITIAL_STATE = TABLE_INITIAL_STATE

    #Read the new .net file
    def generateGraphNew(self, graph_file):
        V = []
        E = []
        F = {}
        ODlist = []
        fname = open(graph_file, "r")
        line = fname.readline()
        print line
        line = line[:-1]
        while line:
            taglist = string.split(line)
            if taglist[0] == 'function':
                variables = []
                variables = taglist[2].replace("(","")
                variables = variables.replace(")","")
                variables = variables.split(",")
                F[taglist[1]] = [taglist[3],variables]

            elif taglist[0] == 'node':
                V.append(Node(taglist[1]))

            elif taglist[0] == 'arc':
                constants = []
                cost_formula = ""
                freeflow_cost = 0
                constant_acc = 0
                if len(taglist) > 5:
                    i = 5
                    while i <= (len(taglist)-1):
                        constants.append(taglist[i])
                        i+=1

                    freeflow_index=0
                    p = Parser()
                    exp = p.parse(F[taglist[4]][0]) ##[4] is function name.[0] is expression
                    LV = exp.variables()
                    buffer_LV = []
                    for l in LV:
                        if l not in F[taglist[4]][1]:
                            constant_acc+=1
                            buffer_LV.append(l)

                    #check if the formula has any parameters(variables)
                    flag = False
                    for v in F[taglist[4]][1]:
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

                    elif is_number(F[taglist[4]][0]):
                        freeflow_cost = float(F[taglist[4]][0])
                        cost_fomula = F[taglist[4]][0]

                    else:
                        exp = exp.simplify(buffer_dic)
                        cost_formula = exp.toString()
                        exp = Parser()
                        exp = exp.parse(cost_formula)
                        freeflow_cost = exp.evaluate({'f':0}) #Hardcoded

                    E.append(Edge(taglist[2], taglist[3], cost_formula, freeflow_cost))

                else:
                    cost_formula = ""
                    freeflow_cost = 0
                    p = Parser()
                    if is_number(F[taglist[4]][0]):
                        cost_formula = F[taglist[4]][0]
                        freeflow_cost = float(F[taglist[4]][0])

                    else:
                        exp = p.parse(F[taglist[4]][0])
                        cost_formula = exp.toString()
                        freeflow_cost = exp.evaluate({'f':0})

                    E.append(Edge(taglist[2], taglist[3], freeflow_cost, cost_formula))

            elif taglist[0] == 'edge':
                constants = []
                cost_formula = ""
                freeflow_cost = 0
                constant_acc = 0
                if len(taglist) > 5:
                    i = 5
                    while i <= (len(taglist)-1):
                        constants.append(taglist[i])
                        i+=1
                    freeflow_index=0
                    p = Parser()
                    exp = p.parse(F[taglist[4]][0]) ##[4] is function name.[0] is expression
                    LV = exp.variables()
                    buffer_LV = []
                    for l in LV:
                        if l not in F[taglist[4]][1]:
                            constant_acc+=1
                            buffer_LV.append(l)

                    #check if the formula has any parameters(variables)
                    flag = False
                    for v in F[taglist[4]][1]:
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

                    elif is_number(F[taglist[4]][0]):
                        freeflow_cost = float(F[taglist[4]][0])
                        cost_fomula = F[taglist[4]][0]

                    else:
                        exp = exp.simplify(buffer_dic)
                        cost_formula = exp.toString()
                        exp = Parser()
                        exp = exp.parse(cost_formula)
                        freeflow_cost = exp.evaluate({'f':0}) #Hardcoded

                    E.append(Edge(taglist[2], taglist[3],freeflow_cost,cost_formula))
                    E.append(Edge(taglist[3], taglist[2],freeflow_cost,cost_formula))

                else:
                    cost_formula = ""
                    freeflow_cost = 0
                    p = Parser()
                    if is_number(F[taglist[4]][0]):
                        cost_formula = F[taglist[4]][0]
                        freeflow_cost = float(F[taglist[4]][0])

                    else:
                        exp = p.parse(F[taglist[4]][0])
                        cost_formula = exp.toString()
                        freeflow_cost = exp.evaluate({'f':0})#hardcoded

                    E.append(Edge(taglist[2], taglist[3],freeflow_cost,cost_formula))
                    E.append(Edge(taglist[3], taglist[2],freeflow_cost,cost_formula))

            elif taglist[0] == 'od':
                ODlist.append((taglist[2],taglist[3],int(taglist[4])))

            line = fname.readline()
            line = line[:-1]
        fname.close()

        for e in E:
            print "Edge " + str(e.start)+"-"+str(e.end)+" has length: " + str(e.length)

        return V, E, ODlist

    def initializeNetworkData(self, k, networkFile, groupSize):
        '''
        Initialize the network data.

        Inputs:
        k: integer = Number of KSP routes to generate
        networkFile: file = .net file
        groupSize: integer = Size of the grouping

       # >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1').initializeNetworkData(8, './networks/OW10_1/OW10_1.net', 1)
        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1').groupSize
        #type name formula variable
        ...
        1
        '''
        self.networkSet = True
        self.ODlist = []
        self.ODL = []
        self.ODheader = ""
        self.ODtable = {}

        """
        As for now it is not importing the capacities file
        if self.networkName == SF_NETWORK_NAME:
            print("Parsing capacity file: %s" % capacitiesFile)
            self.capacities = self.parseCapacityFile(capacitiesFile)
        """

        #This parses the new .net file
        #returns the vertices, the edges,the function cost(not used anymore) and the list of OD pairs
        #it doesn't return the cost function anymore
        self.Vo, self.Eo, odInputo = self.generateGraphNew(networkFile)

        for tupOD in odInputo:
            if(tupOD[2]%self.groupSize!=0):
                print(tupOD[2])
                raise Exception("Error: number of travels is not a multiple of the group size \
                        origin: "+str(tupOD[0])+" destination: "+ str(tupOD[1]))
            else:
                #Origin,destination,number of paths, number of travels
                self.ODlist.append(OD(tupOD[0],tupOD[1],k,tupOD[2]/self.groupSize))
                self.ODL.append(str(tupOD[0])+str(tupOD[1]))
                for i in range(k):
                    if len(self.ODheader) == 0:
                        self.ODheader = self.ODheader + str(tupOD[0])+"to"+str(tupOD[1]) + "_" + str(i+1)
                    else:
                        self.ODheader = self.ODheader + " " + str(tupOD[0])+"to"+str(tupOD[1]) + "_" + str(i+1)

        for od in self.ODL:
            listRoutes = []
            for r in range(self.k):
                listRoutes.append(0)
            self.ODtable[str(od)] = listRoutes

        #Get the k shortest routes
        print "getKRoutes"
        for od in self.ODlist:
            od.paths = KSP.getKRoutes(self.Vo, self.Eo, od.o, od.d, od.numPaths)

        ##get the value of each link - free flow travel time
        self.freeFlow={}
        for edge in self.Eo:
            self.freeFlow[edge.start+"|"+edge.end]=edge.length

        self.edgeNames = sorted(self.freeFlow.keys())

        #self.edges = self.parseCapacityFile(networkFile)

        #creates different drivers according to the number of travels of each OD
        #instance
        self.drivers=[]
        for od in self.ODlist:
            for travel in range(od.numTravels):
                self.drivers.append(Driver(od))

    def cleanODtable(self):
        for od in self.ODL:
            listRoutes = []
            for r in range(self.k):
                listRoutes.append(0)
            self.ODtable[str(od)] = listRoutes

    def parseODfile(self,path):
        with open(path) as odFILE:
            lines = odFILE.readlines()
        odList = []
        for line in lines:
            line = line.replace(' ', '').replace('\n','')
            items = line.split(',')
            if(len(items) == 3):
                odList.append((items[0],items[1],int(items[2])))
        return odList

    def parseCapacityFile(self, path):
        links = {}
        with open(path) as capFILE:
            lines = capFILE.readlines()
            for line in lines:
                line = line.replace('\n','')
                items = line.split(' ')
                if(len(items) == 4):
                    links[items[1]+"|"+items[2]] = float(items[3])
        return links

    def genCallBack(self,ga_engine):
        population = ga_engine.getPopulation()
        generation = ga_engine.getCurrentGeneration()
        if (self.printDriversPerRoute):
            #Drivers per route
            for od in self.ODL:
                listRoutes = []
                for r in range(self.k):
                    listRoutes.append(0)
                self.ODtable[str(od)] = listRoutes

        #gets worst individual
        worstsol = population[len(population)-1]

        if (self.useQL == True): ##if using QL
            #check if the GA->QL interval is None
            if (self.interval == None):
                isGeneration = 1
            else:
                isGeneration = (generation+1) % self.interval

            #check if we are running the GA<->QL or GA<-QL experiment.
            if((self.useInterval) and (isGeneration == 0) and (generation != 0)):
                (qlind,avg_tt) = self.ql.runEpisodeWithAction(ga_engine.bestIndividual().getInternalList()) #GA->QL
            else:
                (qlind,avg_tt) = self.ql.runEpisode() #GA<-QL
                #qlind is a array of paths taken by each driver

            #for each driver
            for i in range(len(qlind)):
                worstsol.getInternalList()[i] = qlind[i]
            worstsol.evaluate()

            #if worstscore has a smaller average travel time than the
            #best individual, copies the ql solution (worstscore)
            #to the second best individual
            if worstsol.score < ga_engine.bestIndividual().score:
                print(">>>>> QL indiv. "+ str(worstsol.score), "turned better than best ind. "+ str(ga_engine.bestIndividual().score)+ "at generation "+ str(generation))
                #copies QL solution to 2nd best ind.
                worstsol.copy(ga_engine.getPopulation()[1])
                ga_engine.getPopulation()[1].evaluate()
            else:
                #copies QL solution to worst in population
                worstsol.copy(ga_engine.getPopulation()[1])
                ga_engine.getPopulation()[len(population)-1].evaluate()

        self.__print_step(generation,ga_engine.bestIndividual().getInternalList(),avgTT=ga_engine.bestIndividual().score, qlTT=worstsol.score)

    def buildODPairData(self, ttByOD):
        """
        returns the string of OD pair data
        """
        str_od = ''
        for k in ttByOD.keys():
            if len(ttByOD[k]) == 0:
                str_od = '0'
            else:
                str_od += " %4.4f" % (sum(ttByOD[k])/len(ttByOD[k]))

        return str_od + ' '

    def __print_step(self, stepNumber, stepSolution, avgTT=None, qlTT=None):
        if stepNumber % self.printInterval == 0:
            if(self.useGA):
                if(self.useQL):
                    self.outputFile.write(str(stepNumber)+" "+str(avgTT) +" "+ str(qlTT))
                else:
                    self.outputFile.write(str(stepNumber)+" "+str(avgTT))
            else:
                self.outputFile.write(str(stepNumber)+" "+ str(qlTT))

            if(self.printPairOD):
                ttByOD = self.travelTimeByOD(stepSolution)
                self.outputFile.write(self.buildODPairData(ttByOD))

            if(self.printTravelTime):
                travel_times = ''
                edges = self.calculateEdgesTravelTimesnew(stepSolution)
                for edge in self.edgeNames:
                    travel_times += str(edges[edge]) + " "
                self.outputFile.write(travel_times.strip()+" ")

            if(self.printDriversPerLink):
                drivers = ''
                edges = self.driversPerLink(stepSolution)
                for edge in self.edgeNames:
                    drivers += str(edges[edge]) + " "
                self.outputFile.write(drivers.strip())

            if(self.printDriversPerRoute):
                self.cleanODtable()
                for s in range(len(stepSolution)):
                    self.ODtable[str(self.drivers[s].od.o) + str(self.drivers[s].od.d)][stepSolution[s]] += 1
                    #print self.ODtable
                self.outputFile.write(" ")
                for keys in self.ODL:##Now it prints in the correct order
                    for x in range(len(self.ODtable[keys])):
                        #string = string + str(ODtable[keys][x])
                        self.outputFile.write(str(self.ODtable[keys][x]) + " ")

            self.outputFile.write("\n")

    def nodesString(self):
        ##string of edges in graph that will be printed
        nodesString = ''
        if self.printPairOD:
            for od in self.ODlist:
                nodesString += "tt_%s|%s " % (od.o, od.d)
        if(self.printTravelTime):
            for edgeN in self.edgeNames:
                nodesString += 'tt_'+edgeN+' '
        if(self.printDriversPerLink):
            for edgeN in self.edgeNames:
                nodesString += "nd_"+edgeN+' '
        if(self.printDriversPerRoute):
            nodesString += self.ODheader
        nodesString = nodesString.strip()
        return nodesString

    def nd(self):
        return len(self.drivers)*self.groupSize

    def appendTag(self, filenamewithtag):
        #tests if there isn't already a file with the desired name
        #paralellization of experiments may result in filename conflit
        append_number = ''
        while(os.path.isfile(filenamewithtag+append_number+".txt")):
            if(append_number == ''):
                append_number = "-1"
            else:
                append_number = "-"+str(int(append_number[1:])+1)
        filenamewithtag += append_number + ".txt"
        return filenamewithtag

    def createStringArgumentsQL(self, nd):
        """
        nd: number of drivers without groupsize
        """
        fmt = './results_gaql_grouped/net_%s/QL/decay%4.3f/alpha%3.2f'
        path2simulationfiles = fmt % (self.networkName, self.decay, self.alpha)

        filename = path2simulationfiles +  '/'+self.networkName \
                + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                + '_'+ str(localtime()[3])+'h'+ str(localtime()[4])+'m'+ str(localtime()[5])+'s'

        headerstr = '#parameters:' + ' k=' + str(self.k) + ' alpha=' + str(self.alpha) \
                + ' decay=' + str(self.decay) + ' number of drivers=' + str(nd) \
                + ' groupsize= '+ str(self.groupSize)\
                + '\n#episode avg_tt ' + self.nodesString()

        return filename, path2simulationfiles, headerstr

    def createStringArguments(self, useQL, useInt):
        if(useQL and useInt):
            fmt = './results_gaql_grouped/net_%s/GA<->QL/pm%4.4f/decay%4.3f/alpha%3.2f/QL<-GA_Interval%s'
            path2simulationfiles = fmt % (self.networkName, self.mutation,
                                          self.decay, self.alpha, self.interval)

            filenamewithtag = path2simulationfiles +  '/net'+self.networkName + '_pm'\
                    + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                    + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                    + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.groupSize) \
                    + '_interval'+ str(self.interval) + '_' + str(localtime()[3])+'h'+ str(localtime()[4]) \
                    +'m'+ str(localtime()[5])+'s'

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                    + str(self.population) + ' self.mutation=' + str(self.mutation) + ' crossover=' + str(self.crossover) \
                    + ' elit=' + str(self.elite) + ' k=' + str(self.k) + ' alpha=' + str(self.alpha) \
                    + ' decay=' + str(self.decay) + ' number of drivers=' + str(self.nd()) \
                    + ' groupsize= '+ str(self.groupSize) + ' GA->QL interval=' + str(self.interval)\
                    + '\n#generation avg_tt ql_avg_tt ' + self.nodesString()

        elif(useQL):
            fmt = './results_gaql_grouped/net_%s/GA<-QL/pm%4.4f/decay%4.3f/alpha%3.2f'
            path2simulationfiles = fmt % (self.networkName, self.mutation,
                                          self.decay, self.alpha)

            filenamewithtag = path2simulationfiles +  '/net'+self.networkName + '_pm'\
                    + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                    + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                    + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.groupSize) \
                    + '_'+ str(localtime()[3])+'h'+ str(localtime()[4])+'m'+ str(localtime()[5])+'s'

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                    + str(self.population) + ' mutation=' + str(self.mutation) + ' crossover=' + str(self.crossover) \
                    + ' elit=' + str(self.elite) + ' k=' + str(self.k) + ' alpha=' + str(self.alpha) \
                    + ' decay=' + str(self.decay) + ' number of drivers=' + str(self.nd()) \
                    + ' groupsize= '+ str(self.groupSize) \
                    + '\n#generation avg_tt ql_avg_tt ' + self.nodesString()
        else:
            fmt = './results_gaql_grouped/net_%s/GA/pm%4.4f'
            path2simulationfiles = fmt % (self.networkName, self.mutation)

            filenamewithtag = path2simulationfiles +  '/net'+self.networkName + '_pm'\
                    + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                    + '_k' + str(self.k) \
                    + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.groupSize) \
                    + '_'+ str(localtime()[3])+'h'+ str(localtime()[4])+'m'+ str(localtime()[5])+'s'

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                    + str(self.population) + ' mutation=' + str(self.mutation) + ' crossover=' + str(self.crossover) \
                    + ' groupsize= '+ str(self.groupSize) + " k= "+str(self.k) \
                    + '\n#generation avg_tt ' +  self.nodesString()

        return filenamewithtag, path2simulationfiles, headerstr

    def run_ql(self, numEpisodes, alpha, decay):
        self.useGA = False
        self.useQL = True
        self.alpha = alpha
        self.decay = decay
        self.ql = QL(self, self.drivers, self.k, self.decay, self.alpha,TABLE_FILL,self.TABLE_INITIAL_STATE) #Change for "coupling" to use TABLE_FILL

        filename, path2simulationfiles, headerstr = self.createStringArgumentsQL(len(self.drivers))
        filenamewithtag = self.appendTag(filename)

        if os.path.isdir(path2simulationfiles) == False:
            os.makedirs(path2simulationfiles)

        self.outputFile = open(filenamewithtag, 'w')
        self.outputFile.write(headerstr+'\n')

        for episode in range(numEpisodes):
            print "episode " +str(episode)
            (instance, value) = self.ql.runEpisode()
            self.__print_step(episode,instance,qlTT=value)

        print("Output file location: %s" % filenamewithtag)

        self.outputFile.close()

    def run_ga_ql(self,useQL,useInt,generations, population, crossover, mutation, elite, alpha, decay,interval):
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
            self.ql = QL(self,self.drivers, self.k, self.decay,self.alpha,TABLE_FILL,self.TABLE_INITIAL_STATE)

        filename, path2simulationfiles, headerstr = self.createStringArguments(useQL, useInt)
        filenamewithtag = self.appendTag(filename)

        ##creates file
        if os.path.isdir(path2simulationfiles)==False:
            os.makedirs(path2simulationfiles)

        self.outputFile = open(filenamewithtag, 'w')
        self.outputFile.write(headerstr+'\n')

        self.ga = GA(generations, population, crossover, mutation, elite, self,
                     self.genCallBack, self.calculateAverageTravelTime,self.drivers)
        self.ga.evolve()

        print("Output file location: %s" % filenamewithtag)
        self.outputFile.close()

    def driversPerLink(self,driverString):
        """
        receives an array of ints stresenting the chosen path of each group
        the array is sorted in the same way as the alleles and the drivers
        list
        returns a dicionary where the keys are edges and the values are the
        amount of drivers on the edge
        """
        global drivers
        global freeFlow
        global groupSize
        dicti = {}
        for inx,dr in enumerate(driverString):
            if(type(dr) != int):
                print('problema!',driverString,'\n')
            path = self.drivers[inx].od.paths[dr]
            for edge in path[0]:
                if edge in dicti.keys():
                    dicti[edge] +=self.groupSize
                else:
                    dicti[edge] = self.groupSize
        for link in self.freeFlow.keys():
            if link not in dicti.keys():
                dicti[link]=0
        return dicti

    def evaluateActionTravelTime(self, driverIndex, action, edgesTravelTimes):
        #calculates travel times for a driver
        traveltime = 0.0
        path = self.drivers[driverIndex].od.paths[action][0] ##list of nodes of path
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

    def calculateEdgesTravelTimes(self, stringOfActions):
        ###############################
        # TRAVEL TIME FUNCTION        #
        ###############################
        ##VDF TRAVEL TIME FUNCTION
        vdfAlpha = 0.15
        vdfBeta = 4
        #calculates travel time each edge
        edges_travel_times = {}
        ##flow
        linkOccupancy = self.driversPerLink(stringOfActions)
        for edge in self.freeFlow.keys():
          if self.networkName == SF_NETWORK_NAME:
              edges_travel_times[edge] = self.freeFlow[edge]*(1+vdfAlpha *((linkOccupancy[edge]/self.capacities[edge])**vdfBeta))
          else:
              edges_travel_times[edge] = self.freeFlow[edge] + .02*linkOccupancy[edge]
        return edges_travel_times

    def calculateEdgesTravelTimesNew(self, stringOfActions): #New Version
        #THIS IS THE NEW EVALUATE FUNCTION(THE ONE ABOVE IS NOT USED ANYMORE)
        #EACH EDGE OF THE NETWORK HAS ITS OWN COST FUNCTION NOW.
        edges_travel_times = {}
        #Get the flow of that edge
        linkOccupancy = self.driversPerLink(stringOfActions)
        #For each edge
        for edge in self.Eo:
            p = Parser()
            exp = p.parse(edge.cost_formula)
            #Evaluates the cost of that edge with a given flow (i.e. edge.eval_cost(flow))
            edges_travel_times[edge.start+"|"+edge.end] = edge.eval_cost(linkOccupancy[edge.start+"|"+edge.end])
        return edges_travel_times

    def calculateAverageTravelTime(self,stringOfActions):
        return sum(self.calculateIndividualTravelTime(stringOfActions))/len(stringOfActions)

""""
    To run the tests you should call from the terminal: python Experiment.py

    If the tests succeed, nothing should happen.  Else it will show the error
    and where it is on the file.
"""
if __name__ == '__main__':
    import doctest
    doctest.testmod()
