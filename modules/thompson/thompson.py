# -*- coding: utf-8 -*-
'''
This module implements the Thompson class implementing the Thompson Sampling algorithm.
'''


import numpy as np
import warnings
import random

class Thompson:
    def __init__(self, experiment, drivers, k):
        self.num_actions = k
        self.drivers = drivers
        self.experiment = experiment
        self.num_drivers = len(drivers)
        self.observations = [] # key: agent{ key:arm, value:[reward]}

        for i in range(self.num_drivers):
            self.observations.append([])
            for j in range(k):
                self.observations[i].append([])

        self.episode = 0
        self.parameter_update_interval = 20 ## interval between updates on the parameters for the distributions
        self.sd = [] #std deviation values for each agent's observations of each route
        self.av = [] #avg values for each agent's observations of each route

        for dInx in range(self.num_drivers):
            self.sd.append([0.0]*k)
            self.av.append([0.0]*k)

    def __chooseActionDrivers(self):
        warnings.simplefilter("error")
        if self.episode < self.num_actions * 2:
            actions = [ self.episode % self.num_actions]*self.num_drivers
            return actions

        else:
            epsilon = 0.0001
            actions = []
            #updates parameters every x episodes or at the first episode after initialization
            if (self.episode % self.parameter_update_interval == 0) or (self.episode == self.num_actions * 2):
                for dInx in range(self.num_drivers):
                    for i in range(self.num_actions):
                        self.sd[dInx][i] = np.std(self.observations[dInx][i],ddof=1) + epsilon
                        self.av[dInx][i] = np.average(self.observations[dInx][i])


            for dInx in range(self.num_drivers):
                thetas = []
                for i in range(self.num_actions):
                    vl = np.random.normal(self.av[dInx][i], self.sd[dInx][i])
                    thetas.append(vl)
                actions.append( int( np.argmax(thetas)))
            return actions
        '''
                thetas = []
                epsilon = 0.0001

                #updates parameters every x episodes or at the first episode after initialization
                if (self.episode % self.parameter_update_interval == 0) or (self.episode == self.num_actions * 2):
                    for i in range(self.num_actions):

                        self.sd[dInx][i] = np.std(self.observations[dInx][i],ddof=1) + epsilon
                        self.av[dInx][i] = np.average(self.observations[dInx][i])
                for i in range(self.num_actions):
                    vl = np.random.normal(self.av[dInx][i], self.sd[dInx][i])
                    thetas.append(vl)

                action = int( np.argmax(thetas))
                return action
        '''
    def runEpisode(self):

        actions = self.__chooseActionDrivers()

        assert(len(actions) == self.num_drivers)
        self.episode += 1
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        # updates the means. reward is the negative of the travel time
        for drIndex in range(self.num_drivers):
            reward = -traveltimes[drIndex]
            #reward = 1.0 / traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)
        average_tt_time = sum(traveltimes)/self.num_drivers
        print average_tt_time,'\n'
        return (actions, average_tt_time)

    def __set_reward(self, dInx, action, value):i
        self.observations[dInx][action].append(value)
