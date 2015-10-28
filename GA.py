# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:50:56 2015

@author: thiago
"""

from pyevolve import G1DList, GSimpleGA, Selectors
from pyevolve import Initializators, Mutators, Consts, Interaction
from pyevolve import Statistics
from pyevolve import DBAdapters
from pyevolve import GAllele

class GA:
    def __init__(self,generations,population,crossover,mutation,elite,experiment,genCallBack
                ,evalFunc,drivers):
        self.experiment = experiment
        self.population = population
        self.crossoverProb = crossover
        self.elite = elite
        self.mutationProb = mutation
        self.generations = generations
        self.genCallBack = genCallBack
        self.evalFunc = evalFunc
        self.drivers = drivers
        
        ###########sets pyevolve
        
        #create alleles to make a GA model. each driver is represented as an allele
        #each driver can take k different routes which is modelled by the different
        #values each allele can take   
        driversAlleles = GAllele.GAlleles()    
        for dr in drivers:
            lst = GAllele.GAlleleList(range(dr.od.numPaths))
            driversAlleles.add(lst)
        ##define a genome with length = length of drivers
        genome = G1DList.G1DList(len(drivers))
        genome.setParams(allele=driversAlleles)
        genome.evaluator.set(self.evalFuncCallback)
        genome.initializator.set(self.initGenome)
        # Genetic Algorithm Instance
        self.ga = GSimpleGA.GSimpleGA(genome)
        self.ga.setMinimax(Consts.minimaxType["minimize"])
        self.ga.selector.set(Selectors.GRankSelector)
        self.ga.setGenerations(self.generations)
        self.ga.stepCallback.set(self.genCallBack)
        self.ga.setMutationRate(self.mutationProb)
        self.ga.setCrossoverRate(self.crossoverProb) #crossover rate is 0.9 per default
        self.ga.setPopulationSize(self.population)
        self.ga.terminationCriteria.set(GSimpleGA.RawStatsCriteria)#before it was GSimpleGA.ConvergenceCriteria
        self.ga.setElitism(True)
        self.ga.setElitismReplacement(self.elite)
        self.ga.setSortType(Consts.sortType["raw"])
    
    #initializes genome string
    def initGenome(self,genome,**args):
       driversAlleles = genome.getParam('allele')
       genome.clearList()
       for i in range(genome.genomeSize):
          genome.append(driversAlleles[i].getRandomAllele())    
    
    def evolve(self):
        self.ga.evolve(freq_stats=10)
        
    def evalFuncCallback(self,genome):
        genomeString = genome.getInternalList()
        return self.evalFunc(genomeString)
