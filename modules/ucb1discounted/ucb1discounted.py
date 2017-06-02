# -*- coding: utf-8 -*-
'''
This module implements the UCB1Discounted class implementing the Discounted UCB1  algorithm as decribed
on the paper On Upper-Confidence Bound Policies for Non-Stationary Bandit Problmes by Garivier and Moulines.
'''

import math
import operator
import random
import sys
class UCB1Discounted():
    def __init__(self, experiment, drivers, k, discount_factor):
        self.experiment = experiment
        self.k = k
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.discount_factor = discount_factor
        self.rewards = []
        self.rewardUpperBound = 1##upper bound on rewards. needed for algorithm
        self.episode = 0
        self.xi = 2.0
        self.rewards ={} #indexed by driver id. value is list of rewards ordered in chronological order
        self.actions = {} #same as above for actions taken

        for dinx in range(self.numdrivers):
            self.rewards[dinx] = []
            self.actions[dinx] = []


    ##returns the route id the driver choosed
    def __choseActionDriver(self, dInx):
        if (len(self.actions[dInx]) < self.k):
            ##plays each arm once in a random order
            possible_actions = []
            for k in range(self.k):
                if k not in self.actions[dInx]:
                    possible_actions.append(k)
            return random.choice(possible_actions)
            #return len(self.actions[dInx])
        else:  # regular case

            Xs = [0.0]*self.k
            Ns = [0.0]*self.k

            ##calculate X and N for every action by iterating over previous rewards
            for i in range(1, self.episode):
                discountedFactor = math.pow(self.discount_factor, self.episode - i)
                Ns[self.actions[dInx][i-1]] += discountedFactor
                Xs[self.actions[dInx][i-1]] += discountedFactor * self.rewards[dInx][i-1]

            for kinx in range(self.k):
                Xs[kinx] = Xs[kinx] / Ns[kinx]
            n = sum(Ns)

            Cs = [0.0]*self.k

            for kinx in range(self.k):
                c = 2.0*self.rewardUpperBound
                c *= math.sqrt(self.xi*math.log(n)/Ns[kinx])
                Cs[kinx] = c

            choice_value = [f + l for f,l in zip(Cs,Xs)]

            ##chooses action with highest value
            index, v = max(enumerate(choice_value), key=operator.itemgetter(1))

            return index


    ##its important to make sure that the upper bound parameter is kept updated
    def __set_reward(self, dInx, action, reward):
        #(self.episode, reward)

        self.rewards[dInx].append(reward)
        self.actions[dInx].append(action)
    ##runs one episode of ucb
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self):

        actions=[]
        self.episode += 1
        #for each driver, select its list of actions in qtable
        for inx, driver in enumerate(self.drivers):
            actions.append(self.__choseActionDriver(inx))

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

        #to print actions taken by each user to stderr
        #if self.episode == 100:
        #    for inx in range(self.numdrivers):
        #        sys.stderr.write(self.drivers[inx].od_s() + ':' + str(self.actions[inx][-10:]))

        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates the means. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
#            reward = 1.0/traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)

        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions, average_tt_time)

