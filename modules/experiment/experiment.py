#!/usr/bin/env python
"""
Changelog:
    v1.0 - Changelog created. <08/03/2017>

Maintainer: Arthur Zachow Coelho (arthur.zachow@gmail.com)
Created (changelog): 08/03/2017

This module contains the Experiment class, which is the experiment or simulation itself.

Warning: Use spaces instead of tabs, or configure your editor to transform tab to 4 spaces.
"""

#Standard modules
import os
from time import localtime
import string
#Third-party module
from py_expression_eval import Parser
#Local modules
from modules.q_learning.q_learning import *

from modules.ucb1.ucb1 import *
from modules.ucb1discounted.ucb1discounted import *
from modules.ucb1window.ucb1window import *
from modules.thompson.thompson import *
from modules.exp3.exp3 import *
from modules.functions.functions import *
from modules.experiment.classes import *
from ksp.KSP import *


class Experiment(object):
    '''
        Sets up an experiment.
    '''
    def __init__(self, k, net_file, group_size, net_name, table_fill_file=None,
                 flow=0, p_travel_time=False, p_drivers_link=False, p_od_pair=False, p_interval=1,
                 epsilon=1.0, p_drivers_route=False, TABLE_INITIAL_STATE='fixed',
                 MINI=0.0, MAXI=0.0, fixed=0.0, action_selection="epsilon", temperature=0.0,
                 ):

        '''
            Construct the experiment.
        '''

        self.action_selection = action_selection
        self.temperature = temperature
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
        self.flow = flow
        self.TABLE_FILL = {}
        self.mini = MINI
        self.maxi = MAXI
        self.fixed = fixed
        self.ODlist = []
        self.ODL = []
        self.ODheader = ""

        self.Vo, self.Eo, odInputo = read_infos(net_file, flow=flow)

        for tup_od in odInputo:
            if round(tup_od[2]) % self.group_size != 0:
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
                        self.ODheader = self.ODheader + str(tup_od[0]) + "to" + str(tup_od[1]) \
                                      + "_" + str(i + 1)
                    else:
                        self.ODheader = self.ODheader + " " + str(tup_od[0]) + "to" \
                                      + str(tup_od[1]) + "_" + str(i + 1)

        #Get the k shortest routes
        for od_pair in self.ODlist:
            od_pair.paths = getKRoutes(self.Vo, self.Eo, od_pair.o, od_pair.d, od_pair.numPaths)

        ##get the value of each link - free flow travel time
        self.freeFlow = {}
        for edge in self.Eo:
            self.freeFlow[edge.name] = edge.cost

        self.edgeNames = sorted(self.freeFlow.keys())

        #creates different drivers according to the number of travels of each OD
        #instance
        self.drivers = []
        for od_pair in self.ODlist:
            for i in range(int(round(od_pair.numTravels))):
                self.drivers.append(Driver(od_pair))

        if TABLE_INITIAL_STATE == 'coupling':
            self.TABLE_FILL = generate_table_fill(table_fill_file)

    def __repr__(self):
        """
        __repr__ method override.

        >>> Experiment(8, './networks/OW10_1/OW10_1.net', 1, 'OW10_1')
        'Experiment: k = 8, net_name = OW10_1'
        """
        return repr(str('Experiment: k = ' + str(self.k) + ', net_name = ' + (self.network_name)))

    def genCallBack(self, ga_engine):
        """
        GA stuff. Not ready for it yet, assuming it is working as it should.
        """
        population = ga_engine.getPopulation()
        generation = ga_engine.getCurrentGeneration()
        if self.printDriversPerRoute:
            #Drivers per route
            for od in self.ODL:
                self.TABLE_FILL[str(od)] = [0] * self.k

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
                    self.outputFile.write(str(step_number) + " " + str(avgTT) + " ")
            else:
                self.outputFile.write(str(step_number) + " " + str(qlTT)+" ")

            if self.printODpair:
                ttByOD = self.travelTimeByOD(stepSolution)
                self.outputFile.write(self.build_od_pair_data(ttByOD))

            if self.printTravelTime:
                travel_times = ''
                edges = self.calculate_edges_travel_times(stepSolution)
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
                self.TABLE_FILL = clean_od_table(self.ODL, self.k)
                for s in range(len(stepSolution)):
                    self.TABLE_FILL[str(self.drivers[s].od.o)
                                    + str(self.drivers[s].od.d)][stepSolution[s]] += 1
                self.outputFile.write(" ")
                for keys in self.ODL:  # Now it prints in the correct order
                    for x in range(len(self.TABLE_FILL[keys])):
                        self.outputFile.write(str(self.TABLE_FILL[keys][x]) + " ")

            self.outputFile.write("\n")

    def createStringArgumentsQL(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_gaql_grouped/net_%s/QL/decay%4.3f/alpha%3.2f"
        path = fmt % (self.network_name, self.decay, self.alpha)

        filename = path + '/' + self.network_name + '_k' + str(self.k) + '_a' + str(self.alpha) \
                 + '_d' + str(self.decay) + '_' + str(localtime()[3]) + 'h' + str(localtime()[4]) \
                 + 'm' + str(localtime()[5]) + 's'

        headerstr = "#Parameters:" + "\n#\tAlpha=" + str(self.alpha)

        if self.action_selection == "epsilon":
            headerstr += "\tEpsilon=" + str(self.epsilon)
        elif self.action_selection == "boltzmann":
            headerstr += "\tTemperature=" + str(self.temperature)

        headerstr += "\n#\tDecay=" + str(self.decay) + "\tNumber of drivers=" \
                  + str(nd) + "\n#\tGroup size=" + str(self.group_size) + "\tQL Table init=" \
                  + str(self.TABLE_INITIAL_STATE) +  "\n#\tk=" + str(self.k)

        if self.TABLE_INITIAL_STATE == "fixed":
            headerstr += "\t\tFixed value=" + str(self.fixed)
        elif self.TABLE_INITIAL_STATE == "random":
            headerstr += "\t\tMax=" + str(self.maxi) + "\n#\tMin=" + str(self.mini)

        headerstr += "\n#Episode AVG_TT " + nodes_string(self.printODpair, self.printTravelTime,
                                                         self.printDriversPerLink,
                                                         self.printDriversPerRoute, self.ODlist,
                                                         self.edgeNames, self.ODheader)

        return filename, path, headerstr

    def createStringArgumentsUCB1(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_UCB_grouped/net_%s/UCB/"
        path = fmt % (self.network_name)

        filename = path + '/' + self.network_name + '_k' + str(self.k)

        if self.init_order == 1: #random order init
            filename += '_randomInit_'
        elif self.init_order == 2: #sequential
            filename += '_sequentialInit_'

        filename += str(localtime()[3]) + 'h' + str(localtime()[4]) \
                 + 'm' + str(localtime()[5]) + 's'

        headerstr = "#Parameters:"

        headerstr += "\tNumber of drivers=" \
                  + str(nd) + "\n#\tk=" + str(self.k)

        headerstr += "\n#Episode AVG_TT " + nodes_string(self.printODpair, self.printTravelTime,
                                                         self.printDriversPerLink,
                                                         self.printDriversPerRoute, self.ODlist,
                                                         self.edgeNames, self.ODheader)

        return filename, path, headerstr


    def createStringArgumentsUCB1Discounted(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_UCB1Discounted_grouped/net_%s/UCB1Discounted/"
        path = fmt % (self.network_name)

        filename = path + '/' + self.network_name + '_k' + str(self.k)  \
                 + '_discount' + str(self.discount_factor)

        if self.init_order == 1: #random order init
            filename += '_randomInit_'
        elif self.init_order == 2: #sequential
            filename += '_sequentialInit_'

        filename +=  str(localtime()[3]) + 'h' + str(localtime()[4]) \
                 + 'm' + str(localtime()[5]) + 's'

        headerstr = "#Parameters:"

        headerstr += "\tNumber of drivers=" \
                  + str(nd) + "\n#\tk=" + str(self.k)

        headerstr += "\n#Episode AVG_TT " + nodes_string(self.printODpair, self.printTravelTime,
                                                         self.printDriversPerLink,
                                                         self.printDriversPerRoute, self.ODlist,
                                                         self.edgeNames, self.ODheader)

        return filename, path, headerstr


    def createStringArgumentsUCB1Window(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_UCB1Window_grouped/net_%s/UCB1Windows/"
        path = fmt % (self.network_name)

        filename = path + '/' + self.network_name + '_k' + str(self.k)  \
                 + '_discount' + str(self.discount_factor) + '_window' + str(self.window_size)

        if self.init_order == 1: #random order init
            filename += '_randomInit_'
        elif self.init_order == 2: #sequential
            filename += '_sequentialInit_'


        filename += str(localtime()[3]) + 'h' + str(localtime()[4]) \
                 + 'm' + str(localtime()[5]) + 's'

        headerstr = "#Parameters:"

        headerstr += "\tNumber of drivers=" \
                  + str(nd) + "\n#\tk=" + str(self.k)

        headerstr += "\n#Episode AVG_TT " + nodes_string(self.printODpair, self.printTravelTime,
                                                         self.printDriversPerLink,
                                                         self.printDriversPerRoute, self.ODlist,
                                                         self.edgeNames, self.ODheader)

        return filename, path, headerstr

    def createStringArgumentsExp3(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_Exp3_grouped/net_%s/Exp3/"
        path = fmt % (self.network_name)

        filename = path + '/' + self.network_name + '_k' + str(self.k)  \
                 +  '_gamma'+ str(self.exp3gamma) \
                 +  '_' + str(localtime()[3]) + 'h' + str(localtime()[4]) \
                 + 'm' + str(localtime()[5]) + 's'

        headerstr = "#Parameters:"

        headerstr += "\tNumber of drivers=" \
                  + str(nd) + "\n#\tk=" + str(self.k)

        headerstr += "\n#Episode AVG_TT " + nodes_string(self.printODpair, self.printTravelTime,
                                                         self.printDriversPerLink,
                                                         self.printDriversPerRoute, self.ODlist,
                                                         self.edgeNames, self.ODheader)

        return filename, path, headerstr


    def createStringArgumentsThompson(self, nd):
        """
        Generate filename, generate the path to the file and generate the header infos for the file
        In:
            nd:int = number of drivers without groupsize
        Out:
            filename:string = filename
            path:string = path to file
            headerstr:string = parameters used in the experiment
        """
        fmt = "./results_Thompson_grouped/net_%s/Thompson/"
        path = fmt % (self.network_name)

        filename = path + '/' + self.network_name + '_k' + str(self.k)  \
                 +  '_' + str(localtime()[3]) + 'h' + str(localtime()[4]) \
                 + 'm' + str(localtime()[5]) + 's'

        headerstr = "#Parameters:"

        headerstr += "\tNumber of drivers=" \
                  + str(nd) + "\n#\tk=" + str(self.k)

        headerstr += "\n#Episode AVG_TT " + nodes_string(self.printODpair, self.printTravelTime,
                                                         self.printDriversPerLink,
                                                         self.printDriversPerRoute, self.ODlist,
                                                         self.edgeNames, self.ODheader)

        return filename, path, headerstr

    def createStringArguments(self, useQL, useInt):
        fmt = "./results_gaql_grouped/net_%s/GA/pm%4.4f/crossover_%.2f"
        path = fmt % (self.network_name, self.mutation, self.crossover)

        filename = '/net' + self.network_name + '_pm' + str(self.mutation) + '_c' \
                 + str(self.crossover) + '_e' + str(self.elite) + '_k' + str(self.k)

        headerstr = "#Parameters:" + "\n#\tGenerations=" + str(self.generations) + "\tPopulation=" \
                  + str(self.population) + "\n#\tMutation=" + str(self.mutation) + "\tCrossover=" \
                  + str(self.crossover) + "\n#\tElite=" + str(self.elite) + "\t\tGroup size=" \
                  + str(self.group_size) + "\n#\tk=" + str(self.k) + "\t\tNumber of drivers=" \
                  + str(nd(self.drivers, self.group_size))

        headerstr_ext = "\n#Generations AVG_TT "

        if useQL: #Experiment type 3
            fmt = "./results_gaql_grouped/net_%s/QLGA/pm%4.4f/crossover_%.2f/decay%4.3f/alpha%3.2f"
            path = fmt % (self.network_name, self.mutation, self.crossover, self.decay, self.alpha)

            filename += '_a' + str(self.alpha) + '_d' + str(self.decay)
            headerstr += "\n#\tAlpha=" + str(self.alpha) + "\tDecay=" + str(self.decay) \

            if self.action_selection == "epsilon":
                headerstr += "\n#\tEpsilon=" + str(self.epsilon)
            elif self.action_selection == "boltzmann":
                headerstr += "\n#\tTemperature=" + str(self.temperature)

            headerstr += "\tQL table init=" + str(self.TABLE_INITIAL_STATE)

            if self.TABLE_INITIAL_STATE == "fixed":
                headerstr += "\n#\tFixed value=" + str(self.fixed)
            elif self.TABLE_INITIAL_STATE == "random":
                headerstr += "\n#\tMax=" + str(self.maxi) + "\t\tMin=" + str(self.mini)


            headerstr_ext += " QL_AVG_TT"

            if useInt: #Experiment type 4
                fmt = "./results_gaql_grouped/net_%s/GAQL/" \
                       + "pm%4.4f/crossover_%.2f/decay%4.3f/alpha%3.2f"

                path = fmt % (self.network_name, self.mutation, self.crossover, self.decay, self.alpha)
                filename += '_interval'+ str(self.interval)
                headerstr += "\n#\tGA<->QL interval=" + str(self.interval)

        filename += '_' + str(localtime()[3]) + 'h' + str(localtime()[4]) + 'm' \
                 + str(localtime()[5]) + 's'

        filename = path + filename

        headerstr += headerstr_ext + nodes_string(self.printODpair, self.printTravelTime,
                                                  self.printDriversPerLink, self.printDriversPerRoute,
                                                  self.ODlist, self.edgeNames, self.ODheader)

        return filename, path, headerstr

    def run_UCB1Discounted(self, num_episodes, discount_factor,init_order):
        assert(type(discount_factor)== float )
        ucb1 = UCB1Discounted(self, self.drivers, self.k,discount_factor,init_order)
        self.useGA = False
        self.useQL = True
        self.discount_factor = discount_factor
        self.init_order = init_order

        filename, path, headerstr = self.createStringArgumentsUCB1Discounted(len(self.drivers))
        filename = appendTag(filename)

        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')
        print "num episodes %d", num_episodes
        for episode in range(num_episodes):
            print_progress(episode+1, num_episodes)
            (instance, value) = ucb1.runEpisode()
            self.__print_step(episode, instance, qlTT=value)
        print("Output file location: %s" % filename)
        self.outputFile.close()

    def run_UCB1Window(self, num_episodes,discount_factor, window_size,init_order):
        assert(type(discount_factor)== float )
        ucb1 = UCB1Window(self, self.drivers, self.k,discount_factor, window_size,init_order)
        self.useGA = False
        self.useQL = True
        self.discount_factor = discount_factor
        self.window_size = window_size
        self.init_order = init_order
        filename, path, headerstr = self.createStringArgumentsUCB1Window(len(self.drivers))
        filename = appendTag(filename)

        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')
        print "num episodes %d", num_episodes
        for episode in range(num_episodes):
            print_progress(episode+1, num_episodes)
            (instance, value) = ucb1.runEpisode()
            self.__print_step(episode, instance, qlTT=value)
        print("Output file location: %s" % filename)
        self.outputFile.close()


    def run_UCB1(self, num_episodes,init_order):
        ucb1 = UCB1(self, self.drivers, self.k,init_order)
        self.useGA = False
        self.useQL = True
        self.init_order = init_order
        filename, path, headerstr = self.createStringArgumentsUCB1(len(self.drivers))
        filename = appendTag(filename)

        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')
        print "num episodes %d", num_episodes
        for episode in range(num_episodes):
            print_progress(episode+1, num_episodes)
            (instance, value) = ucb1.runEpisode()
            self.__print_step(episode, instance, qlTT=value)
        print("Output file location: %s" % filename)
        self.outputFile.close()

    def run_Exp3(self, num_episodes,gamma):
        exp3 = Exp3(self, self.drivers, self.k, gamma)

        self.useGA = False
        self.useQL = True
        self.exp3gamma = gamma
        filename, path, headerstr = self.createStringArgumentsExp3(len(self.drivers))
        filename = appendTag(filename)

        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')
        print "num episodes %d", num_episodes
        for episode in range(num_episodes):
            print_progress(episode+1, num_episodes)
            (instance, value) = exp3.runEpisode(num_episodes)
            self.__print_step(episode, instance, qlTT=value)
        print("Output file location: %s" % filename)
        self.outputFile.close()

    def run_Thompson(self, num_episodes):
        th = Thompson(self, self.drivers, self.k)
        self.useGA = False
        self.useQL = True
        filename, path, headerstr = self.createStringArgumentsThompson(len(self.drivers))
        filename = appendTag(filename)

        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')

        for episode in range(num_episodes):
            print_progress(episode + 1, num_episodes)
            (instance, value) = th.runEpisode()

            self.__print_step(episode, instance, qlTT=value)
        print("Output file location: %s" % filename)
        self.outputFile.close()

    def run_ql(self, num_episodes, alpha, decay):
        self.useGA = False
        self.useQL = True
        self.alpha = alpha
        self.decay = decay
        self.ql = QL(self, self.drivers, self.k, self.decay, self.alpha, self.TABLE_FILL,
                     self.epsilon, self.TABLE_INITIAL_STATE, MINI=self.mini, MAX=self.maxi,
                     fixed=self.fixed, action_selection=self.action_selection,
                     temperature=self.temperature)

        filename, path, headerstr = self.createStringArgumentsQL(len(self.drivers))
        filename = appendTag(filename)

        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')

        for episode in range(num_episodes):
            (instance, value) = self.ql.runEpisode()
            self.__print_step(episode, instance, qlTT=value)
        ''' To print progress bar, uncomment this line.
            print_progress(episode+1, num_episodes)
        '''

        print("Output file location: %s" % filename)

        self.outputFile.close()

    def run_ga_ql(self, useQL, useInt, generations, population, crossover, mutation, elite, alpha,
                  decay, interval):
        from modules.genetic_algorithm.genetic_algorithm import *
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
            self.ql = QL(self, self.drivers, self.k, self.decay, self.alpha, self.TABLE_FILL,
                         self.epsilon, self.TABLE_INITIAL_STATE, MINI=self.mini, MAX=self.maxi,
                         fixed=self.fixed, action_selection=self.action_selection,
                         temperature=self.temperature)

        filename, path, headerstr = self.createStringArguments(useQL, useInt)
        filename = appendTag(filename)

        ##creates file
        if os.path.isdir(path) is False:
            os.makedirs(path)

        self.outputFile = open(filename, 'w')
        self.outputFile.write(headerstr + '\n')

        self.ga = GA(generations, population, crossover, mutation, elite, self,
                     self.genCallBack, self.calculateAverageTravelTime, self.drivers)
        self.ga.evolve()

        print("Output file location: %s" % filename)
        self.outputFile.close()

    def driversPerLink(self, driverString):
        """
        receives an array of ints stresenting the chosen path of each group
        the array is sorted in the same way as the alleles and the drivers
        list
        returns a dicionary where the keys are edges and the values are the
        amount of drivers on the edge
        """
        dicti = {}
        for inx, dr in enumerate(driverString):
            if(type(dr) != int):
                print('problema!', driverString, '\n')
                print type(dr)
            path = self.drivers[inx].od.paths[dr]
            for edge in path[0]:
                if edge in dicti.keys():
                    dicti[edge] += self.group_size
                else:
                    dicti[edge] = self.group_size
        for link in self.freeFlow.keys():
            if link not in dicti.keys():
                dicti[link] = 0
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

    def travelTimeByOD(self, string_actions):
        edgesTravelTimes = self.calculate_edges_travel_times(string_actions)
        odTravelTimeDict = self.initTravelTimeByODDict()
        for driverIdx, action in enumerate(string_actions):
            path = self.drivers[driverIdx].od.paths[action][0]
            traveltime = 0.0
            for edge in path:
                traveltime += edgesTravelTimes[edge]
            odTravelTimeDict[self.drivers[driverIdx].od_s()].append(traveltime)

        return odTravelTimeDict

    def calculateIndividualTravelTime(self, string_actions):
        #returns list of travel times for each driver
        edgesTravelTimes = self.calculate_edges_travel_times(string_actions)
        results = []
        for driverIdx, action in enumerate(string_actions):
            travel_times = self.evaluateActionTravelTime(driverIdx, action, edgesTravelTimes)
            results.append(travel_times)
        return results

    def calculate_edges_travel_times(self, string_actions):
        edges_travel_times = {}
        #Get the flow of that edge
        link_occupancy = self.driversPerLink(string_actions)
        #For each edge
        for edge in self.Eo:
            #Evaluates the cost of that edge with a given flow (i.e. edge.eval_cost(flow))
            edges_travel_times[edge.name] = edge.eval_cost(link_occupancy[edge.name])
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
