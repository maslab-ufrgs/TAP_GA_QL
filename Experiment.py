# -*- coding: utf-8 -*-
"""
Implements GA+QL for traffic assignement problem
More information about use in runExperiment.py

Files GA.py and QL.py implements operations specific to each
algorithm

The genetic algorithm segment is implemented using pyevolve
"""
import os
from GA import GA
from QL import QL
from time import localtime
import KSP

class Driver():
    #od:OD = instance of OD class
    def __init__(self,OD):
        self.od = OD

    def od_s(self):
        return "%s%s" % (self.od.o, self.od.d)

class OD():
    #O:string = origin node
    #D:string = destination node
    #numPath: int = number of shortest paths to generate
    #numTravels: int = number of travels
    def __init__(self,O,D,numPaths,numTravels):
        self.o = O
        self.d = D
        self.numPaths = numPaths
        self.numTravels = numTravels
        self.paths = None

    def __str__(self):
        return "origin: " + str(self.o) + " destination: "+str(self.d) + \
                "number of travels: " + str(self.numTravels) + " number of shortest paths: " \
                + str(self.numPaths)

class Experiment:

    def __init__(self,k,networkFile, capacitiesFile, odFile, groupSize, printLinkCosts=False, printDriversPerLink=False,outputtype="normal"):
        self.printDriversPerLink = printDriversPerLink
        self.printLinkCosts = printLinkCosts
        self.networkSet = False
        self.edges = {}
        self.initializeNetworkData(k, networkFile, capacitiesFile, odFile, groupSize)
        self.outputtype= outputtype

    def initializeNetworkData(self, k, networkFile, capacitiesFile, odFile, groupSize):

        self.networkSet = True
        self.networkName ="Ortuzar"
        self.k = k
        self.groupsize = groupSize
        odInput = self.parseODfile(odFile)
        self.ODlist = []

        for tupOD in odInput:
            if(tupOD[2]%self.groupsize!=0):
                print(tupOD[2])
                raise Exception("Error: number of travels is not a multiple of the group size \
                        origin: "+str(tupOD[0])+" destination: "+ str(tupOD[1]))
            else:
                                #Origin,destination,number of paths, number of travels
                self.ODlist.append(OD(tupOD[0],tupOD[1],k,tupOD[2]/self.groupsize))

        #calculating k shortest routes for each OD pair
        for od in self.ODlist:
            od.paths = KSP.getKRoutes(networkFile,od.o, od.d, od.numPaths)

        ##get the value of each link - free flow travel time
        V,E = KSP.generateGraph(networkFile)
        self.freeFlow={}
        for edge in E:
            self.freeFlow[edge.start+edge.end]=edge.length

        self.edgeNames = sorted(self.freeFlow.keys())

        print(networkFile)
        self.edges = self.parseCapacityFile(networkFile)

        #creates different drivers according to the number of travels of each OD
        #instance
        self.drivers=[]
        for od in self.ODlist:
            for travel in range(od.numTravels):
                self.drivers.append(Driver(od))

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
                    links[items[1]+items[2]] = float(items[3])
        return links

    def genCallBack(self,ga_engine):
        population = ga_engine.getPopulation()
        generation = ga_engine.getCurrentGeneration()

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
                (qlind,avg_tt) = self.ql.runEpisodeWithAction(ga_engine.bestIndividual().getInternalList()) #GA<-QL
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

    def buildODPairData(self, ttByOD, ttByEdge):
        """
        returns the string of OD pair data
        """
        str_od = ''

        for k in ttByOD.keys():
            str_od += " %4.4f" % (sum(ttByOD[k])/len(ttByOD[k]))

        str_edge = ''

        for k in ttByEdge.keys():
            if len(ttByEdge[k]) > 0:
                str_edge += " %4.4f" % (sum(ttByEdge[k])/len(ttByEdge[k]))
            else:
                str_edge += " %4.4f" % 0.0

        return str_od + str_edge

    def __print_step(self, stepNumber, stepSolution, avgTT=None, qlTT=None):
        if(self.useGA):
            if(self.useQL):
                self.outputFile.write(str(stepNumber)+": "+str(avgTT) +" "+ str(qlTT))
            else:
                self.outputFile.write(str(stepNumber)+": "+str(avgTT))
        else:
            ##using ql
            self.outputFile.write(str(stepNumber)+": "+ str(qlTT))

        if(self.printLinkCosts):
            #print edges cost
            costs = ''
            ##calculates cost of each link
            edges = self.calculateEdgesCosts(stepSolution)
            for edge in self.edgeNames:
                costs += str(edges[edge]) + " "
            self.outputFile.write(costs.strip())
        if(self.printDriversPerLink):
            ##prints number of drivers at each link
            drivers = ''
            edges = self.driversPerLink(stepSolution)
            for edge in self.edgeNames:
                drivers += str(edges[edge]) + " "
            self.outputFile.write(drivers.strip())

        if(self.outputtype == "pairOD"):
            ttByOD, ttByEdge = self.travelTimeByEdgeAndOD(stepSolution)
            self.outputFile.write(self.buildODPairData(ttByOD, ttByEdge))

        self.outputFile.write("\n")

    def nodesString(self):
        ##string of edges in graph that will be printed
        nodesString = ''
        if(self.printLinkCosts):
            for edgeN in self.edgeNames:
                nodesString += 'cost_'+edgeN+' '
        if(self.printDriversPerLink):
            for edgeN in self.edgeNames:
                nodesString += "nDrv_"+edgeN+' '
        nodesString = nodesString.strip()
        return nodesString

    def nd(self):
        return len(self.drivers)*self.groupsize

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

        path2simulationfiles = './results_gaql_grouped/QL/' +'_net_'+self.networkName  \
                + '/nd'+ str(nd) +'_groupsize'+ str(self.groupsize)\
                + '/decay' + "%4.3f" % self.decay  + '/alpha' + "%3.2f" % self.alpha

        filename = path2simulationfiles +  '/'+self.networkName \
                + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                + '_nd'+ str(nd) + '_groupsize'+ str(self.groupsize) \
                + '_'+ str(localtime()[3])+'h'+ str(localtime()[4])+'m'+ str(localtime()[5])+'s-'\
                + str(localtime()[2])+"-"+str(localtime()[1]) +"-"\
                + str(localtime()[0])

        headerstr = '#parameters:' + ' k=' + str(self.k) + ' alpha=' + str(self.alpha) \
                + ' decay=' + str(self.decay) + ' number of drivers=' + str(nd) \
                + ' groupsize= '+ str(self.groupsize)\
                + '\n#generation avg_tt ql_avg_tt ' + self.nodesString()

        return filename, path2simulationfiles, headerstr

    def createStringArguments(self, useQL, useInt):
        if(useQL and useInt):
            path2simulationfiles = './results_gaql_grouped/GA<->QL/' +'_net_'+self.networkName  \
                    + '/pm' + "%4.4f" % self.mutation \
                    + '/nd'+ str(self.nd()) +'_groupsize'+ str(self.groupsize)\
                    + '/decay' + "%4.3f" % self.decay  + '/alpha' + "%3.2f" % self.alpha + '/QL<-GA_Interval' + str(self.interval)

            filenamewithtag = path2simulationfiles +  '/net'+self.networkName + '_pm'\
                    + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                    + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                    + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.groupsize) \
                    + '_interval'+ str(self.interval) + '_' + str(localtime()[3])+'h'+ str(localtime()[4]) \
                    +'m'+ str(localtime()[5])+'s-'\
                    + str(localtime()[2])+"-"+str(localtime()[1]) +"-"\
                    + str(localtime()[0])

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                    + str(self.population) + ' self.mutation=' + str(self.mutation) + ' crossover=' + str(self.crossover) \
                    + ' elit=' + str(self.elite) + ' k=' + str(self.k) + ' alpha=' + str(self.alpha) \
                    + ' decay=' + str(self.decay) + ' number of drivers=' + str(self.nd()) \
                    + ' groupsize= '+ str(self.groupsize) + ' GA->QL interval=' + str(self.interval)\
                    + '\n#generation avg_tt ql_avg_tt ' + self.nodesString()

        elif(useQL):
            path2simulationfiles = './results_gaql_grouped/GA<-QL/' +'_net_'+ self.networkName  \
                    + '/pm' + "%4.4f" % self.mutation \
                    + '/nd'+ str(self.nd()) + '_groupsize'+ str(self.groupsize)\
                    + '/decay' + "%4.3f" % self.decay  + '/alpha' + "%3.2f" % self.alpha

            filenamewithtag = path2simulationfiles +  '/net'+self.networkName + '_pm'\
                    + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                    + '_k' + str(self.k) + '_a' + str(self.alpha) + '_d' + str(self.decay)\
                    + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.groupsize) \
                    + '_'+ str(localtime()[3])+'h'+ str(localtime()[4])+'m'+ str(localtime()[5])+'s-'\
                    + str(localtime()[2])+"-"+str(localtime()[1]) +"-"\
                    + str(localtime()[0])

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                    + str(self.population) + ' mutation=' + str(self.mutation) + ' crossover=' + str(self.crossover) \
                    + ' elit=' + str(self.elite) + ' k=' + str(self.k) + ' alpha=' + str(self.alpha) \
                    + ' decay=' + str(self.decay) + ' number of drivers=' + str(self.nd()) \
                    + ' groupsize= '+ str(self.groupsize) \
                    + '\n#generation avg_tt ql_avg_tt ' + self.nodesString()
        else:
            path2simulationfiles = './results_gaql_grouped/GA/' +'_net_'+self.networkName  \
                    + '/pm' + "%4.4f" % self.mutation + '/nd'+ str(self.nd()) \
                    +'_groupsize' + str(self.groupsize)

            filenamewithtag = path2simulationfiles +  '/net'+self.networkName + '_pm'\
                    + str(self.mutation) + '_c' + str(self.crossover) + '_e' + str(self.elite) \
                    + '_k' + str(self.k) \
                    + '_nd'+ str(self.nd()) + '_groupsize'+ str(self.groupsize) \
                    + '_'+ str(localtime()[3])+'h'+ str(localtime()[4])+'m'+ str(localtime()[5])+'s-'\
                    + str(localtime()[2])+"-"+str(localtime()[1]) +"-"\
                    + str(localtime()[0])

            headerstr = '#parameters: generations=' + str(self.generations) + ' pop.size='\
                    + str(self.population) + ' mutation=' + str(self.mutation) + ' crossover=' + str(self.crossover) \
                    + ' groupsize= '+ str(self.groupsize) + " k= "+str(self.k) \
                    + '\n#generation avg_tt ' +  self.nodesString()

        headerstr = self.appendExtraODPairTimes(headerstr)

        return filenamewithtag, path2simulationfiles, headerstr

    def appendExtraODPairTimes(self, baseHeader):
        """
        Appends the list of OD pairs and the list of edges to the header
        """
        baseHeader += " #od_pairs"
        for od in self.ODlist:
            baseHeader += " %s%s" % (od.o, od.d)

        baseHeader += " #edges "
        baseHeader += ' '.join(sorted(self.edges.keys()))

        return baseHeader

    def run_ql(self, numEpisodes, alpha, decay):
        self.useGA = False
        self.useQL = True
        self.alpha = alpha
        self.decay = decay
        self.ql = QL(self, self.drivers, self.k, self.decay, self.alpha)

        filename, path2simulationfiles, headerstr = self.createStringArgumentsQL(len(self.drivers))
        filenamewithtag = self.appendTag(filename)

        if os.path.isdir(path2simulationfiles) == False:
            os.makedirs(path2simulationfiles)

        self.outputFile = open(filenamewithtag, 'w')
        self.outputFile.write(headerstr+'\n')

        for episode in range(numEpisodes):
            (instance, value) = self.ql.runEpisode()
            self.__print_step(episode,instance,qlTT=value)

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
            self.ql = QL(self,self.drivers, self.k, self.decay,self.alpha)

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
        global groupsize
        dicti = {}
        for inx,dr in enumerate(driverString):
            if(type(dr) != int):
                print('problema!',driverString,'\n')
            path = self.drivers[inx].od.paths[dr]
            for edge in path[0]:
                if edge in dicti.keys():
                    dicti[edge] +=self.groupsize
                else:
                    dicti[edge] = self.groupsize
        for link in self.freeFlow.keys():
            if link not in dicti.keys():
                dicti[link]=0
        return dicti

    def evaluateActionCost(self, driverIndex, action, edgesCosts):
        ##calculates cost for a driver
        traveltime = 0.0
        path = self.drivers[driverIndex].od.paths[action][0] ##list of nodes of path
        for edge in path:
            traveltime += edgesCosts[edge]
        return traveltime

    def initTravelTimeByODDict(self):
        d = {}
        for od in self.ODlist:
            d["%s%s" % (od.o, od.d)] = []
        return d

    def initTravelTimeByEdgeDict(self):
        d = {}
        for edges in self.edges.keys():
            d[edges[0]] = []
        return d

    def travelTimeByEdgeAndOD(self, stringOfActions):
        edgesCosts = self.calculateEdgesCosts(stringOfActions)
        odTravelTimeDict = self.initTravelTimeByODDict()
        edgeTravelTimeDict = self.initTravelTimeByEdgeDict()

        for driverIdx, action in enumerate(stringOfActions):
            path = self.drivers[driverIdx].od.paths[action][0]
            traveltime = 0.0
            for edge in path:
                traveltime += edgesCosts[edge]
                if edge in edgeTravelTimeDict.keys():
                    edgeTravelTimeDict[edge].append(edgesCosts[edge])
            odTravelTimeDict[self.drivers[driverIdx].od_s()].append(traveltime/len(path))

        return odTravelTimeDict, edgeTravelTimeDict

    def calculateIndividualTravelTime(self,stringOfActions):
        #returns list of travel times for each driver
        edgesCosts = self.calculateEdgesCosts(stringOfActions)
        results = []
        for driverIdx, action in enumerate(stringOfActions):
            costs = self.evaluateActionCost(driverIdx, action, edgesCosts)
            results.append(costs)
        return results

    def calculateEdgesCosts(self,stringOfActions):
        ###############################
        # COST FUNCTION               #
        ###############################
        ##VDF COST FUNCTION
        ##vdfAlpha = 0.15
        ##vdfBeta = 4
        #calculates cost of each edge
        edgesCosts = {}
        ##flow
        linkOccupancy = self.driversPerLink(stringOfActions)
        for edge in self.freeFlow.keys():
            edgesCosts[edge] = self.freeFlow[edge] + .02*linkOccupancy[edge]
        ##edgesCosts[edge] = self.freeFlow[edge]*(1+vdfAlpha *((linkOccupancy[edge]/self.capacities[edge])**vdfBeta))
        return edgesCosts

    def calculateAverageTravelTime(self,stringOfActions):
        return sum(self.calculateIndividualTravelTime(stringOfActions))/len(stringOfActions)
