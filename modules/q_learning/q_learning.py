# -*- coding: utf-8 -*-
import random

class QL():
    def __init__(self, experiment, drivers, k, decay, alpha, tableFill, epsilon=1, iniTable="zero"
                 , MINI=0.0, MAX=0.0, fixed=0.0):
        self.experiment = experiment
        self.epsilon = epsilon
        self.alpha = alpha
        self.decay = decay
        self.k = k
        ##init qtable
        self.qtable = []
        self.ODtable = {}
        self.drivers = drivers
        self.tableFill = tableFill
        self.numdrivers=len(drivers)
        if iniTable == "zero":
            print "Generating Q-Table with zeros."
            for i in range(self.numdrivers):
                self.qtable.append([0.0]*k)
        elif iniTable == "coupling": #New way to fill the table
            print "Generating Q-Table with mean coupling."
            for d in drivers:
                string = []
                for r in range(len(d.od.paths)):
                    string.append((-1.0)*(self.tableFill[str(d.od.o)+"|"+str(d.od.d)][r]))
                self.qtable.append(string)
        elif iniTable == "random":
            print "Generating Q-Table with random values."
            for i in range(self.numdrivers):
                string = []
                for t in range(self.k):
                    string.append(random.uniform(MINI,MAX))
                self.qtable.append(string)
        elif iniTable == "fixed":
            print "Generating Q-Table with fixed values."
            for i in range(self.numdrivers):
                self.qtable.append([fixed]*k)
        #print self.qtable

    ##runs one episode of ql
    ##returns (instance,averagefitnessvalue)
    ##list of routes (one for each driver)
    def runEpisode(self):
        actions=[]
        #for each driver, select its list of actions in qtable
        for a in self.qtable:
            #selection according to epsilon-greedy
            randomnb = random.uniform(0,1)
            if randomnb < self.epsilon:
                # action is selected randomly
                curaction = random.randint(0,self.k-1)
            else:
                # action is selected greedly
                max_in_array = max(a)
                #print max_in_array
                array_of_pointers2max = []
                for na in range(len(a)): #for each action
                    if a[na] == max_in_array:
                        array_of_pointers2max.append(na)
                if len(array_of_pointers2max) == 0:##bloco estava identado
                     raise Exception("error: no max found in qtable for  " + str(a))
                else:
                     if len(array_of_pointers2max) == 1:
                          # this means only one action maximizes
                          curaction = array_of_pointers2max[0]
                     else:
                          # more than one action with max value
                          curaction = random.choice(array_of_pointers2max)
            actions.append(curaction)

        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates qtable. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            #print 'reward: '+str(reward)+"\n"
            self.qtable[drIndex][actions[drIndex]] = self.qtable[drIndex][actions[drIndex]] * (1-self.alpha) + self.alpha*reward

        #updates epsilon
        self.epsilon = self.epsilon * self.decay
        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions,average_tt_time)

    def runEpisodeWithAction(self,actions):
        traveltimes = self.experiment.calculateIndividualTravelTime(actions)

        #updates qtable. reward is the negative of the travel time
        for drIndex in range(self.numdrivers):
            reward = -traveltimes[drIndex]
            #print 'reward: '+str(reward)+"\n"
            self.qtable[drIndex][actions[drIndex]] = self.qtable[drIndex][actions[drIndex]] * (1-self.alpha) + self.alpha*reward

        #updates epsilon
        self.epsilon = self.epsilon * self.decay
        average_tt_time = sum(traveltimes)/self.numdrivers
        return (actions,average_tt_time)
