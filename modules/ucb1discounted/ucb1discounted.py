# -*- coding: utf-8 -*-
'''
This module implements the UCB1Discounted class implementing the Discounted UCB1  algorithm as decribed
on the paper On Upper-Confidence Bound Policies for Non-Stationary Bandit Problmes by Garivier and Moulines.
'''

import math
import operator
class UCB1Discounted():
    def __init__(self, experiment, drivers, k):
        self.experiment = experiment
        self.k = k
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.discount_factor = 0.01
        self.rewards = []
        self.rewardUpperBound = 1.0 ##upper bound on rewards. needed for algorithm
        self.episode = 0
        for dinx in range(self.numdrivers):
            di = {}
            for i in range(self.k):
                di[i] = []
            self.rewards.append(di)

    def __searchReward(self,rewardlist,episode, upperBound = None, lowerBound = None):
        ##list has format [(episode, reward)]
        
        if(upperBound == None or lowerBound == None):
            lowerBound = 0
            upperBound = len(rewardlist) - 1
              
        found = False
        while(not found):
            index = lowerBound +( upperBound - lowerBound)/2
            if(rewardlist[index][0]==episode):
                #found
                return rewardlist[index]
            if upperBound == lowerBound:
                #not found
                return None
            if(rewardlist[index][0] < episode):
                upperBound = upperBound
                lowerBound = index + 1
            if(rewardlist[index][0] > episode):
                upperBound = index - 1
                lowerBound = lowerBound 

    ##returns the route id the driver choosed
    def __choseActionDriver(self, dInx):

        if (self.episode <= self.k):
            ##plays one 'arm' once at the beginning
            return self.episode-1
        else:  # regular case

            Xs = [0.0]*self.k
            Ns = [0.0]*self.k

            #calculate N and X for every action
            for kinx in range(self.k):
                partialX = 0.0
                partialN = 0.0
                if(kinx in self.rewards[dInx].keys()):
                    for i in range(1,self.episode+1):
                        ##checks if played arm kinx at episode i
                        rewardTuple = self.__searchReward(self.rewards[dInx][kinx], i)
                        if(rewardTuple != None): ## has played arm                            
                            discountedFactor = math.pow(self.discount_factor, self.episode-i)
                            partialN += discountedFactor
                            partialX += discountedFactor * rewardTuple[1]
                Xs[kinx] = partialX/partialN
                Ns[kinx] = partialN
                
            n = sum(Ns)

            Cs = [0.0]*self.k

            for kinx in range(self.k):
                c = 2.0*self.rewardUpperBound
                c *= math.log(n)/Ns[kinx]
                Cs[kinx] = c

            choice_value = [f + l for f,l in zip(Cs,Xs)]

            ##chooses action with highest value
            index, v = max(enumerate(choice_value), key=operator.itemgetter(1))

            return index


    ##its important to make sure that the upper bound parameter is kept updated
    def __set_reward(self, dInx, action, reward):
        self.rewards[dInx][action].append((self.episode, reward))

    ##runs one episode of ucb
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self):
        actions=[]
        self.episode += 1
        #for each driver, select its list of actions in qtable
        for inx, driver in enumerate(self.drivers):
            actions.append(self.__choseActionDriver(inx))

        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates the means. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
#            reward = 1.0/traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)

        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions, average_tt_time)

