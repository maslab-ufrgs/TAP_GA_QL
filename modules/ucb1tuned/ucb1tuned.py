# -*- coding: utf-8 -*-
'''
This module implements the UCB class implementing the UCB1 algorithm.
'''

import math
import operator
import numpy as np
import random
import matplotlib.pyplot as plt
def calculate_avg_var(values):
    #from https://stackoverflow.com/a/2415343
    avg = np.average(values)
    var =np.average((values-avg)**2)
    return (avg, var)

class UCB1():
    def __init__(self, experiment, drivers, k,init_order):
        self.experiment = experiment
        self.k = k
        self.init_order = init_order
        self.ODtable = {}
        self.drivers = drivers
        self.numdrivers=len(drivers)
        self.number_plays = []
        self.observations = []

        for d in range(self.numdrivers):
            self.number_plays.append([0]*k)
            self.observations.append([])
            for ks in range(k):
                ##one list for each k of each driver
                self.observations[d].append([])
        self.episode = 0
        self.plot = True
        self.all_rewards_values = []
        self.all_rewards_rounds = []
        self.all_rewards_colors = []
        self.color_mapping_od ={}
        self.traveltimes = []

    def color_od(self,driver):
        origin = driver.od.o
        destination = driver.od.d
        if(origin not in self.color_mapping_od.keys()):
            self.color_mapping_od[origin] = {}
        if(destination not in self.color_mapping_od[origin].keys()):
            self.color_mapping_od[origin][destination] = np.random.rand()
        return self.color_mapping_od[origin][destination]

    ##returns the route id the driver choosed
    def __choseActionDriver(self, dInx):
        if (self.episode <= self.k):
            if(self.init_order == 1): ##random order init
                possible_actions = []
                for k in range(self.k):
                    if self.number_plays[dInx][k] == 0:
                        possible_actions.append(k)

                choice = random.choice(possible_actions)
                self.number_plays[dInx][choice] += 1
                return choice
            elif(self.init_order == 2): ##sequential order
                self.number_plays[dInx][self.episode - 1] += 1
                return self.episode - 1
            else:
                raise "invalid init order"

        else:  # regular case
            choice_value = [0.0] * self.k
            for k in range(self.k):
                avg , variance = calculate_avg_var(self.observations[dInx][k])
                v_value = variance + math.sqrt(2* math.log(self.episode)/float(self.number_plays[dInx][k]) )
                bonus =  math.sqrt((math.log(self.episode)) / float(self.number_plays[dInx][k]) * min(0.25, v_value)  )
                choice_value[k] = avg + bonus

            ##chooses action with highest value
            index, v = max(enumerate(choice_value), key=operator.itemgetter(1))
            self.number_plays[dInx][index] += 1  ## does not update mean
            return index

    ##updates the means os the specified agent with the reward of the last round
    def __set_reward(self, dInx, action, reward):
        plays = self.number_plays[dInx][action]
        self.observations[dInx][action].append(reward)

    ##runs one episode of ucb
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self):
        actions=[]
        #for each driver, select its list of actions in qtable
        self.episode +=1
        for inx, driver in enumerate(self.drivers):
            actions.append(self.__choseActionDriver(inx))
        #print actions
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates the means. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            #reward = 1.0-(traveltimes[drIndex]/120.0)
            #if(reward < 0 or reward > 100):
            #    print reward
            if self.plot:
                self.all_rewards_values.append(reward)
                self.all_rewards_rounds.append(self.episode)
                self.all_rewards_colors.append(self.color_od(self.drivers[drIndex]))
            self.__set_reward(drIndex, actions[drIndex], reward)
        average_tt_time = sum(traveltimes)/self.numdrivers
        self.traveltimes.append(average_tt_time)

        print average_tt_time

        if self.episode == 100:
            print average_tt_time
            if self.plot:
                plt.figure(1)
                plt.scatter(self.all_rewards_rounds, self.all_rewards_values, c= self.all_rewards_colors)
                plt.figure(2)
                plt.plot(self.traveltimes)
                plt.show()

        return (actions, average_tt_time)
