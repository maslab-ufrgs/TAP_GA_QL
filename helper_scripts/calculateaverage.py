# -*- coding: utf-8 -*-
"""
reads files in the root folder (must not have the text 'averaged' as part of the path)
and for each group of experiments with the same attributes, calculates the average of
the first columns of each file. This results in a file in the averaged/subfolder where
the average for each line of the first columns is written.

HOW TO USE
set the root folder with the 'root' variable. Subfolders will be searched.
"""
from os import listdir
from os.path import isfile, join
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

##gets all files within path including in subdirectories
##returns list of tuples (folderpath, filepath)
def getFiles(path):
    ##only .txt files
    files = [ (path,f) for f in listdir(path) if isfile(join(path,f)) and f.endswith(".txt") and '/averaged/' not in f ]
    ##folders
    directories = [ f for f in listdir(path) if not isfile(join(path,f))]
    
    for directory in directories:
        files = files + getFiles(path+directory+"/")
    return files

##reads only first column
def readFile(filepath):
    mFile = open(filepath)
    y_values = []
    lines = [x for x in mFile.readlines() if x[0]!='#' and x[0]!='\n'and x!='']
    print filepath
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



#################################################

##SET ROOT HERE
root = "/home/gauss/otmbneto/Desktop/thibef-ga_ql_V3/results_gaql_grouped/QL/_net_siouxfalls/nd360600_groupsize1/decay0.990/"

attributes_files = {} #maps attributes to files: attribute -> [filepath]
for path, filename in getFiles(root):    
    attributes = str(readFilenameAttributes(filename))
    if attributes not in attributes_files.keys():
        attributes_files[attributes]=[]
    attributes_files[attributes].append(path+"/"+filename)

for attribute in attributes_files.keys():
    ##read one
    f = open(attributes_files[attribute][0],'r')
    header = "".join([l for l in f.readlines() if l[0]=='#'])
    f.close()
    name = attributes_files[attribute][0].split("/")[-1]
    path = "/".join(attributes_files[attribute][0].split("/")[:-1]) + "averaged/"
    if os.path.isdir(path)==False:
            os.makedirs(path)
    outFileName = path+"_".join(name.split("_")[:-1])+".txt"
    print outFileName
    results = []
    for filepath in attributes_files[attribute]:
        results.append(readFile(filepath))
    average = []

    for line in range(len(results[0])):
        sum_line = 0
        for inx,result in enumerate(results):
            sum_line += float(result[line])

        average.append(sum_line/len(results))
    f = open(outFileName,'w')
    f.write(header)
    for inx,line in enumerate(average):
        f.write(str(inx)+": "+str(line)+"\n")
    f.close()
