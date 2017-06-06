# -*- coding: utf-8 -*-
'''
This module implements the UCB class implementing the UCB1 algorithm.
'''

import math
import operator

import random
class UCB1():
    def __init__(self, experiment, drivers, k,init_order):
        self.experiment = experiment
        self.k = k
        self.init_order = init_order
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.number_plays = []
        self.means = []
        for d in range(self.numdrivers):
            self.number_plays.append([0]*k)
            self.means.append([0.0]*k)

        self.round = [0]*self.numdrivers

    ##returns the route id the driver choosed
    def __choseActionDriver(self, dInx):
        self.round[dInx] += 1
        if (self.round[dInx] <= self.k):
            if(self.init_order == 1): ##random order init
                possible_actions = []
                for k in range(self.k):
                    if self.number_plays[dInx][k] == 0:
                        possible_actions.append(k)

                choice = random.choice(possible_actions)
                self.number_plays[dInx][choice] += 1
                return choice
            elif(self.init_order == 2): ##sequential order
                self.number_plays[dInx][self.round[dInx] - 1] += 1
                return self.round[dInx] - 1
            else:
                raise "invalid init order"

        else:  # regular case
            choice_value = [0.0] * self.k
            for i, u in enumerate(self.means[dInx]):
                choice_value[i] = u + math.sqrt((2.0 * math.log(self.round[dInx])) / self.number_plays[dInx][i])
            ##chooses action with highest value
            index, v = max(enumerate(choice_value), key=operator.itemgetter(1))
            self.number_plays[dInx][index] += 1  ## does not update mean
            return index

    ##updates the means os the specified agent with the reward of the last round
    def __set_reward(self, dInx, action, reward):
        plays = self.number_plays[dInx][action]
        self.means[dInx][action] = (self.means[dInx][action] * (plays - 1) + reward) / plays

    ##runs one episode of ucb
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self):
        actions=[]
        #for each driver, select its list of actions in qtable

        for inx, driver in enumerate(self.drivers):
            actions.append(self.__choseActionDriver(inx))
        #print actions
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates the means. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            #reward = 1.0/traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)

        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions, average_tt_time)

