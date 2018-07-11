# -*- coding: utf-8 -*-
'''
This module implements the Exp3 class implementing the Exp3  algorithm.
'''

import math
import operator
import sys
import numpy.random

class Exp3():
    def __init__(self, experiment, drivers, k, gamma):
        self.experiment = experiment
        self.k = k
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.episode = 0
        assert(type(gamma)==float)
        assert(gamma >= 0.0 and gamma <= 1.0)
        self.gamma = gamma
        self.w = {}
        self.p = {}
        for i in range(self.numdrivers):
            self.w[i] = [1.0]*self.k
            self.p[i] = [0.0]*self.k
    ##returns the route id the driver chose
    def __chooseActionDriver(self, dInx):

        wsum = sum(self.w[dInx])

        for kinx in range(self.k):
            self.p[dInx][kinx]= (1 - self.gamma) * (self.w[dInx][kinx]/wsum) + self.gamma/self.k
        return int(numpy.random.choice(range(self.k), 1, p=self.p[dInx])[0])


    def __set_reward(self, dInx, action, reward):
        for kinx in range(self.k):
            if(action == kinx):
                x = reward/self.p[dInx][action]
            else:
                x = 0.0
            self.w[dInx][kinx] *= math.exp((self.gamma*x)/self.k)


    ##runs one episode of the algorithm
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self,num_episodes):
        self.episode += 1
        actions=[]
        #for each driver, select its list of actions in qtable
        for inx, driver in enumerate(self.drivers):
            actions.append(self.__chooseActionDriver(inx))

        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates the means. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)

        average_tt_time = sum(traveltimes)/self.numdrivers
        print "avgtt=%f\n" % average_tt_time
        return (actions, average_tt_time)

