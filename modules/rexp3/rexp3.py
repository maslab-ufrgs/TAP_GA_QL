# -*- coding: utf-8 -*-
'''
This module implements the Rexp3 class implementing the Rexp3  algorithm as decribed
on the paper Stochastic Multi-Armed-Bandit Problem with Non-stationary Rewards by Gur, Yonatan
;Zeevi, Assaf;Besbes, Omar
'''

import math
import operator
import sys
import numpy.random

class Rexp3():
    def __init__(self, experiment, drivers, k, epoch_size, gamma):
        self.experiment = experiment
        self.k = k
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.episode = 0
        self.epoch_size = epoch_size
        self.current_batch = 1
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


    ##runs one episode of ucb
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self,num_episodes):
        self.episode += 1
        #update current_batch
        if self.current_batch <= math.ceil(self.episode/self.epoch_size):
            self.current_batch += 1
            for i in range(self.numdrivers):
                self.w[i] = [1.0] * self.k
            print "updated batch at episode %d to %d" %(self.episode-1, self.current_batch)



        actions=[]
        #for each driver, select its list of actions in qtable
        for inx, driver in enumerate(self.drivers):
            actions.append(self.__chooseActionDriver(inx))


        '''
        actionstaken = {}
        for inx in range(self.numdrivers):
            #sys.stderr.write(self.drivers[inx].od_s() + ':' + str(actions[inx]))
            odname = self.drivers[inx].od_s()
            if not actionstaken.has_key(odname):
                actionstaken[odname] = [0]*self.k
            actionstaken[odname][actions[inx]] += 1
        for odname in actionstaken.keys():
            sys.stderr.write("for od %s:   " % odname)
            for k in range(self.k):
                sys.stderr.write("%d: %f%% | " % (k, 100*float(actionstaken[odname][k])/sum(actionstaken[odname])))
            sys.stderr.write("\n")
        '''
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates the means. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
#            reward = 1.0/traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)

        average_tt_time = sum(traveltimes)/self.numdrivers
        print "avgtt=%f\n" % average_tt_time
        return (actions, average_tt_time)

