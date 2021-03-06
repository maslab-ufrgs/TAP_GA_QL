# -*- coding: utf-8 -*-
'''
This module implements the UCB1Window class implementing the Sliding Window UCB1  algorithm as decribed
on the paper On Upper-Confidence Bound Policies for Non-Stationary Bandit Problems by Garivier and Moulines.
'''

import math
import operator
import random
import sys
class UCB1Window():
    def __init__(self, experiment, drivers, k, discount_factor, window_size,init_order):
        self.experiment = experiment
        self.k = k
        self.init_order = init_order
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.discount_factor = discount_factor
        self.window_size = window_size
        self.rewards = []
        self.rewardUpperBound = 1##upper bound on rewards. needed for algorithm
        self.xi = 2.0
        self.episode = 0
        self.rewards ={} #indexed by driver id. value is list of rewards ordered in chronological order
        self.actions = {} #same as above for actions taken

        for dinx in range(self.numdrivers):
            self.rewards[dinx] = []
            self.actions[dinx] = []


    ##returns the route id the driver chose
    def __choseActionDriver(self, dInx, log_size):
        if (len(self.actions[dInx]) < self.k):
            if self.init_order == 1:
                ##plays each arm once in a random order
                possible_actions = []
                for k in range(self.k):
                    if k not in self.actions[dInx]:
                        possible_actions.append(k)
                return random.choice(possible_actions)
            elif self.init_order == 2: #play arm sequentially
                return len(self.actions[dInx])
            else:
                raise "invalid init order"
        else:  # regular case

            Xs = [0.0]*self.k
            Ns = [0.0]*self.k

            begin_window = self.episode - min(self.window_size, self.episode-1)
            n = 0.0
            ##calculate X and N for every action by iterating over previous rewards
            for i in range(begin_window, self.episode):
                discountedFactor = math.pow(self.discount_factor, self.episode - i)
                Ns[self.actions[dInx][i-1]] += discountedFactor
                Xs[self.actions[dInx][i-1]] += discountedFactor * self.rewards[dInx][i-1]
                n += Ns[self.actions[dInx][i-1]]

            Cs = [0.0]*self.k
            choice_value = []
            for kinx in range(self.k):
                if Ns[kinx] <= 0:
                    Ns[kinx] += 0.001
                Xs[kinx] = Xs[kinx] / Ns[kinx]
                c = self.rewardUpperBound
                c *= math.sqrt(log_size/Ns[kinx])
                Cs[kinx] = c
                choice_value.append(Cs[kinx]+Xs[kinx])

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
        log_size = self.xi * math.log(min(self.window_size,self.episode))

        for inx, driver in enumerate(self.drivers):
            actions.append(self.__choseActionDriver(inx,log_size))
	
        #actionstaken = {}
        #for inx in range(self.numdrivers):
            #sys.stderr.write(self.drivers[inx].od_s() + ':' + str(actions[inx]))
        #    odname = self.drivers[inx].od_s()
        #    if not actionstaken.has_key(odname):
        #        actionstaken[odname] = [0]*self.k
        #    actionstaken[odname][actions[inx]] += 1
        #for odname in actionstaken.keys():
        #    sys.stderr.write("for od %s:   " % odname)
        #    for k in range(self.k):
        #        sys.stderr.write("%d: %f%% | " % (k, 100*float(actionstaken[odname][k])/sum(actionstaken[odname])))
        #    sys.stderr.write("\n")
	
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
        print "avgtt=%f\n" % average_tt_time
        return (actions, average_tt_time)

