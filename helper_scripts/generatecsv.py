# -*- coding: utf-8 -*-
"""

"""
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

#return list of filtered lines
def processFile(root_folder,file_name):
    mFile = open(root_folder+file_name)
    lines = [x for x in mFile.readlines() if x[0]!='#' and x[0]!='\n']

    filtered_lines = []
    for line in lines:
        line = line.replace("\t", " ").replace("\n",' ').replace(':','')
        tokens = [x for x in line.split(" ") if x!='']
        filtered_lines.append(tokens)
    return filtered_lines



##gets all files within path including in subdirectories
##returns list of tuples (folderpath, filepath)
def getFiles(path):
    ##only .txt files
    files = [ (path,f) for f in listdir(path) if isfile(join(path,f)) and f.endswith(".txt") ]
    ##folders
    directories = [ f for f in listdir(path) if not isfile(join(path,f))]
    
    for directory in directories:
        files = files + getFiles(path+directory+"/")
    return files


def generateCSVs(root_folder):
    outputFile = root_folder+"compiled_results.csv"
    processed_files = []
    experiment_files = getFiles(root_folder)
    for file_path, filename in experiment_files:
            processed_files.append((filename,processFile(file_path, filename)))
    
    csv_matrix_elements = [] ##addressed by [col][line]
    
    
    for pFile, lines_tokens in processed_files:
        print pFile
        column1 = [pFile,"'average travel time GA'"]
        column2 = ["-","'average travel time QL'"]
        print len(lines_tokens)
        for generation_tokens in lines_tokens:
            column1.append(generation_tokens[1])
            column2.append(generation_tokens[2])
        csv_matrix_elements.append(column1)
        csv_matrix_elements.append(column2)
    
    oFile = open(outputFile, 'w')
    ##calculates larges experiment in generations
    max_num_gens = 0
    for experimentInx in range(len(csv_matrix_elements)):    
        if(len(csv_matrix_elements[experimentInx])>max_num_gens):
            max_num_gens =len(csv_matrix_elements[experimentInx])
            
    
    for rowInx in range(max_num_gens):
        line_text = str(rowInx-2)
        for colInx in range(2*len(experiment_files)):
            if(colInx < len(csv_matrix_elements[colInx])):
                #print rowInx, colInx,len(csv_matrix_elements[colInx])
                if(len(csv_matrix_elements[colInx])<=rowInx):
                    info = "none"
                else:
                    info = csv_matrix_elements[colInx][rowInx]
                if(len(csv_matrix_elements[colInx])-1==rowInx):
                    print csv_matrix_elements[colInx][0],csv_matrix_elements[colInx][1], csv_matrix_elements[colInx][rowInx]
                    
                line_text+=","+ info
        oFile.write(line_text+"\n")
    oFile.close()        

#root_folder = '/home/thiago/Copy/Bolsa IC - IA/Genetic algorithms + reinforcement learning/GA_RL_KSP/results_gaql/_netsiouxfalls/decay0.990/alpha0.50/pm0.0010/nd360600/withQL/'
root_folder = '/home/gauss/tbfoliveira/Copy/Bolsa IC - IA/Genetic algorithms + reinforcement learning/GA_RL_KSP/NEW/results_gaql_grouped/GA_QL/_net_siouxfalls/pm0.0010/nd360600_groupsize1/'
generateCSVs(root_folder)


