# -*- coding: utf-8 -*-
'''
This module implements the Thompson class implementing the Thompson Sampling algorithm.
'''


import numpy as np
import warnings
import math
import random

def calculate_std_avg(values,weights):
    #from https://stackoverflow.com/a/2415343
    avg = np.average(values,weights=weights)
    std = math.sqrt(np.average((values-avg)**2, weights=weights))
    return (avg, std)


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
                self.observations[i].append([[],[]])# rewards

        self.episode = 0
        self.parameter_update_interval = 10 ## interval between updates on the parameters for the distributions

        self.sd = [] #std deviation values for each agent's observations of each route
        self.av = [] #avg values for each agent's observations of each route
        #self.initial_actions = []
        for dInx in range(self.num_drivers):
            self.sd.append([0.0]*k)
        #   act = list(range(k)) + list(range(k))
        #  random.shuffle(act)
            #print act

        #    self.initial_actions.append(act)
            self.av.append([0.0]*k)

    def __chooseActionDrivers(self):
        warnings.simplefilter("error")
        if self.episode < self.num_actions * 2:
            actions = [ self.episode % self.num_actions]*self.num_drivers
            #actions = []
            #for dInx in range(self.num_drivers):
            #    actions.append(self.initial_actions[dInx][self.episode])
            return actions
            #actions = []
            #for dInx in range(self.num_drivers):
            #    possible = []
            #    for k in range(self.num_actions):
            #        if len(self.observations[dInx][k]) < 2:
            #            possible.append(k)
            #    actions.append(random.choice(possible))
            #return actions
        else:
            epsilon = 0.0001
            actions = []
            #updates parameters every x episodes or at the first episode after initialization
            if (self.episode % self.parameter_update_interval == 0) or (self.episode == self.num_actions * 2):
                for dInx in range(self.num_drivers):
                    for i in range(self.num_actions):
                        self.sd[dInx][i] = np.std(self.observations[dInx][i],ddof=1) + epsilon
                        self.av[dInx][i] = np.average(self.observations[dInx][i])
                        if(dInx == 900):
                            print "sd",self.sd[dInx][i], " av",self.av[dInx][i]
                            print self.observations[dInx][i]



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
        self.episode += 1
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        # updates the means. reward is the negative of the travel time
        for drIndex in range(self.num_drivers):
            reward = -traveltimes[drIndex]
            self.__set_reward(drIndex, actions[drIndex], reward)
        average_tt_time = sum(traveltimes)/self.num_drivers
        print average_tt_time,'\n'
        return (actions, average_tt_time)

    def __set_reward(self, dInx, action, value):
        self.observations[dInx][action][0].append(value)
        self.observations[dInx][action][1].append(self.episode)
