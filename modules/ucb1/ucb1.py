# -*- coding: utf-8 -*-
'''
This module implements the UCB class implementing the UCB1 algorithm.
'''

import math
import operator

import random
class UCB1():
    def __init__(self, experiment, drivers, k):
        self.experiment = experiment
        self.k = k
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.number_plays = [[0]*k]*self.numdrivers
        self.means = [[0.0]*k]*self.numdrivers
        self.round = [0]*self.numdrivers

    ##returns the route id the driver choosed
    def __choseActionDriver(self, dInx):
        self.round[dInx] += 1
        if (self.round[dInx] <= self.k):
            ###plays one 'arm' once at the beginning
            self.number_plays[dInx][self.round[dInx]-1] += 1
            return self.round[dInx]-1
        else:  # regular case
            choice_value = [0.0] * self.k
            for i, u in enumerate(self.means[dInx]):
                choice_value[i] = u + math.sqrt((2 * math.log(self.round[dInx])) / self.number_plays[dInx][i])
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
#            reward = -traveltimes[drIndex]
            reward = 1.0/traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)

        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions, average_tt_time)

