# -*- coding: utf-8 -*-
'''
This module implements the Rexp3 class implementing the Rexp3  algorithm as decribed
on the paper Stochastic Multi-Armed-Bandit Problem with Non-stationary Rewards by Gur, Yonatan
;Zeevi, Assaf;Besbes, Omar
'''

import math
import sys
import numpy.random
import random

class Rexp3MA():
    def __init__(self, experiment, drivers, k, gamma, p_forget, p_forget_decay):
        self.experiment = experiment
        self.k = k
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.episode = 0
        self.p_forget = p_forget ##probability of forgetting
        self.p_forget_decay = p_forget_decay
        assert(type(gamma)==float)
        assert(gamma >= 0.0 and gamma <= 1.0)
        self.gamma = gamma
        self.w = {}
        self.p = {}
        for i in range(self.numdrivers):
            self.w[i] = [1.0]*self.k
            self.p[i] = [0.0]*self.k
        self.actions = range(self.k)
        self.forgets = [0]*self.numdrivers
    ##returns the route id the driver chose
    def __chooseActionDriver(self, dInx):

        ##agent forgets with probability p_forget
        if random.uniform(0, 1) < self.p_forget:
            self.w[dInx] = [1.0]*self.k
            self.forgets[dInx] +=1

        wsum = sum(self.w[dInx])

        for kinx in range(self.k):
            self.p[dInx][kinx]= (1 - self.gamma) * (self.w[dInx][kinx]/wsum) + self.gamma/self.k
        return int(numpy.random.choice(self.actions, 1, p=self.p[dInx])[0])


    def __set_reward(self, dInx, action, reward):
        for kinx in range(self.k):
            if(action == kinx):
                x = reward/self.p[dInx][action]
            else:
                x = 0.0
            self.w[dInx][kinx] *= math.exp((self.gamma*x)/self.k)


    ##runs one episode of ucb
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
            assert(type(reward) == float)
            self.__set_reward(drIndex, actions[drIndex], reward)

        #updates p_forget with its decay rate
        self.p_forget *= self.p_forget_decay
        average_tt_time = sum(traveltimes)/self.numdrivers
        print "avgtt=%f\n" % average_tt_time
        print float(sum(self.forgets))/self.numdrivers
        return (actions, average_tt_time)

