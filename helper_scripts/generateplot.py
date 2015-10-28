# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:12:07 2015

@author: thiago
"""
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

##gets all files within path including in subdirectories
##returns list of tuples (folderpath, filepath)
def getFiles(path):
    ##only .txt files
    files = [ (path,f) for f in listdir(path) if isfile(join(path,f)) and f.endswith(".txt")]
    ##folders
    directories = [ f for f in listdir(path) if not isfile(join(path,f))]
    
    for directory in directories:
        files = files + getFiles(path+directory+"/")
    return files


def readFile(filepath):
    mFile = open(filepath)
    y_values = []
    lines = [x for x in mFile.readlines() if x[0]!='#' and x[0]!='\n']
    for line in lines:
        line = line.replace("\t", " ").replace("\n",' ').replace(':','')
        tokens = [x for x in line.split(" ") if x!='']
        y_values.append(tokens[1])
    return y_values
    
def readFilenameAttributes(filename):

    attributes = {}    
    tokens = filename.split('_')
    ##first token is always network
    attributes['network'] = tokens[0]
    for token in tokens:
        if(token[0]=='c'):
            ##crossover
            attributes['crossover'] = token[1:]
        elif(token[0]=='e'):
            ##elite
            attributes['elite'] = token[1:]
        elif(token[0]=='k'):
            ##k
            attributes['k'] = token[1:]
        elif(token[0]=='a'):
            ##alpha
            attributes['alpha'] = token[1:]
        elif(token[0:2]=='pm'):
            ##mutation
            attributes['mutation'] = token[2:]
        elif(token[0]=='d'):
            ##mutation
            attributes['decay'] = token[1:]
    return attributes
##receives list of attributes dictionaries. returns list of keys 
##whose values are different between the different attributes
def calculateDifferentAttributes(attributeList):
    attributeKeys = set()
    for attribute in attributeList:
        attributeKeys = attributeKeys.union(attribute.keys())
    keys_different_values= set([])
    for key in attributeKeys:
        value = None
        for attribute in attributeList:
            if(value==None):
                value = attribute[key]
            else:
                if(value!=attribute[key]):
                    keys_different_values.add(key)
                    break
    return list(keys_different_values)
    
def constructLegend(attributes, keys):
    texts = []
    for key in keys:
        texts.append(key+" "+str(attributes[key]))
    return " ".join(texts)
    
##input plot_data = list of tuples [(legend, [data])]
def plotExperiment(plot_data, output):    
    y_values = [] ##list of lists contaigning y values (same order as input)
    
    legends = []
    max_y =0
    for leg, data in plot_data:
        y_values.append(data)
        legends.append(leg)
        max_y = max(max_y,len(data))

    line_styles = ['-','--']
    line_colors = ['r','c','g','b','m','y','k']
    
    fig = plt.figure()    

    for inx in range(len(y_values)):
        x = range(len(y_values[inx])+1)[1:]##ignores first position(value 0)
        line_style = line_styles[(inx / len(line_colors))%len(line_styles)]
        line_color = line_colors[inx % len(line_colors)]
        plt.plot(x, y_values[inx],linestyle=line_style,label=legends[inx],color=line_color)
        #plt.plot(x, y_values[inx],label=legends[inx])
    #plt.ylim([0,max_y+10])
    plt.ylim([20,100]) ##limits y axis display 
    plt.xlabel('generations')
    plt.ylabel('average travel time')
    plt.legend(loc='upper right',ncol=2)
    #plt.xscale("log")
    plt.savefig('teste.png')    
    plt.title('Fitness value of best solution')
    plt.savefig(output+"plot.png")
    plt.show()
    plt.close()
    
root = "/home/thiago/Copy/Bolsa IC - IA/Genetic algorithms + reinforcement learning/GA_RL_KSP_project/results_gaql_grouped/GA_QL/_net_siouxfalls/pm0.0010/nd360600_groupsize100/decay0.990/alpha0.90/averaged/"
files = [] #(filepath,attributes)
for path, filename in getFiles(root):    
    attributes = readFilenameAttributes(filename)
    files.append((path+"/"+filename,attributes))

files_to_plot = []
diffAttri = calculateDifferentAttributes([x[1] for x in files])
print diffAttri
for f in files:
    files_to_plot.append( (constructLegend(f[1],diffAttri),f[0]) )


files_to_plot = sorted(files_to_plot,key=lambda x: x[0])

data = []
for legend,f in files_to_plot:
    data.append((legend, readFile(f)))
plotExperiment(data,root)
