# -*- coding: utf-8 -*-
"""
Changelog:
    v1.0 - Changelog created. <08/03/2017>
    v1.1 - Corrections in the action selection for the Boltzmann method. <29/03/2017>

Maintainer: Arthur Zachow Coelho (arthur.zachow@gmail.com)

This module contains the QL class which runs the QL experiments.
"""
import random
import math

class QL():
    def __init__(self, experiment, drivers, k, decay, alpha, tableFill, epsilon=1, iniTable="zero"
                 , MINI=0.0, MAX=0.0, fixed=0.0, action_selection="epsilon", temperature=None):
        self.experiment = experiment
        self.epsilon = epsilon
        self.alpha = alpha
        self.decay = decay
        self.k = k
        self.action_selection = action_selection
        self.temperature = temperature
        self.qtable = []
        self.ODtable = {}
        self.drivers = drivers
        self.tableFill = tableFill
        self.numdrivers=len(drivers)
        if iniTable == "coupling":
            print "Generating Q-Table with mean coupling."
            for d in drivers:
                string = []
                for r in range(len(d.od.paths)):
                    string.append((-1.0)*(self.tableFill[str(d.od.o)+"|"+str(d.od.d)][r]))
                self.qtable.append(string)
        elif iniTable == "random":
            print "Generating Q-Table with random values."
            for i in range(self.numdrivers):
                string = []
                for t in range(self.k):
                    string.append(random.uniform(MINI,MAX))
                self.qtable.append(string)
        elif iniTable == "fixed":
            print "Generating Q-Table with fixed values."
            for i in range(self.numdrivers):
                self.qtable.append([fixed]*k)
        #print self.qtable

    ##runs one episode of ql
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self):
        actions=[]
        #for each driver, select its list of actions in qtable
        for a in self.qtable:
            if self.action_selection == "epsilon":
                #selection according to epsilon-greedy
                randomnb = random.uniform(0, 1)
                if randomnb < self.epsilon:
                    # action is selected randomly
                    if float('-inf') in a:
                        curaction = random.randint(0, self.k-2)
                    else:
                        curaction = random.randint(0, self.k-1)
                else:
                    # action is selected greedly
                    max_in_array = max(a)
                    #print max_in_array
                    array_of_pointers2max = []
                    for na in range(len(a)): #for each action
                        if a[na] == max_in_array:
                            array_of_pointers2max.append(na)

                    #Chooses one of the actions with maximum value
                    curaction = random.choice(array_of_pointers2max)

            elif self.action_selection == "boltzmann":
                #Updates the probability of each action
                list_tup = []
                total = 0.0
                index = 0
                for action in a:
                    total += math.exp(action/self.temperature)
                for action in a:
                    list_tup.append((index, math.exp(action/self.temperature)/total))
                    index += 1

                #Selects the action
                random_number = random.uniform(0, 1)
                total = 0.0
                index = 0

                list_tup = sorted(list_tup, key=lambda prob: prob[1])

                while total < random_number:
                    total += list_tup[index][1]
                    if random_number <= total:
                        curaction = list_tup[index][0]
                        break
                    index += 1

            actions.append(curaction)

        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates qtable. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            #print 'reward: '+str(reward)+"\n"
            self.qtable[drIndex][actions[drIndex]] = self.qtable[drIndex][actions[drIndex]] * (1-self.alpha) + self.alpha*reward

        if self.action_selection == "epsilon":
            #updates epsilon
            self.epsilon = self.epsilon * self.decay

        if self.action_selection == "boltzmann":
            self.temperature = self.temperature * self.decay

        #chinelagem
        def c_sum(l):
            r = 0
            for i in l:
                if i != float('inf'):
                    r += i
            return r

        average_tt_time = c_sum(traveltimes)/self.numdrivers
        return (actions, average_tt_time)

    def runEpisodeWithAction(self, actions):
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates qtable. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            #print 'reward: '+str(reward)+"\n"
            self.qtable[drIndex][actions[drIndex]] = self.qtable[drIndex][actions[drIndex]] * (1-self.alpha) + self.alpha*reward

        if self.action_selection == "epsilon":
            #updates epsilon
            self.epsilon = self.epsilon * self.decay

        if self.action_selection == "boltzmann":
            self.temperature = self.temperature * self.decay

        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions, average_tt_time)
