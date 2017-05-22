# -*- coding: utf-8 -*-
'''
This module implements the Thompson class implementing the Thompson Sampling algorithm.
'''


import numpy as np
import warnings

class Thompson:
    def __init__(self, experiment, drivers, k):
        self.num_actions = k
        self.drivers = drivers
        self.experiment = experiment
        self.num_drivers = len(drivers)
        self.observations = {} # key: agent{ key:arm, value:[reward]}
        for i in range(self.num_drivers):
            self.observations[i] = {}
            for j in range(k):
                self.observations[i][j] = []
        self.round = [0]*self.num_drivers

    def __chooseActionDriver(self,dInx):
        warnings.simplefilter("error")
        thetas = []
        epsilon = 0.0001


        if self.round[dInx] < self.num_actions * 2:
            inx = self.round[dInx] % self.num_actions
            self.round[dInx] += 1
            return inx
            ##plays one 'arm' twice at the beginning


        for i in range(self.num_actions):

            sd = np.std(self.observations[dInx][i],ddof=1) + epsilon
            av = np.average(self.observations[dInx][i])
            vl = np.random.normal(av, sd)
            thetas.append(vl)

        action = int( np.argmax(thetas))
        self.round[dInx] += 1
        return action

    def runEpisode(self):
        actions = []
        # for each driver, select its list of actions in qtable
        for inx, driver in enumerate(self.drivers):
            act = self.__chooseActionDriver(inx)
            actions.append(act)

        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        # updates the means. reward is the negative of the travel time
        for drIndex in range(self.num_drivers):
            reward = -traveltimes[drIndex]
            #reward = 1.0 / traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)
        average_tt_time = sum(traveltimes)/self.num_drivers
        return (actions, average_tt_time)

    def __set_reward(self, dInx, action, value):
        self.observations[dInx][action].append(value)