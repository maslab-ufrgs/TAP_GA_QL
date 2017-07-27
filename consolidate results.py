import os
import sys
import numpy
#gets all files in the subtree with path as root
def get_files_in_subtree(path):
    children = os.listdir(path)
    files = [(f, os.path.join(path,f)) for f in children if os.path.isfile(os.path.join(path, f))]

    folders = [os.path.join(path,f) for f in children if not os.path.isfile(os.path.join(path, f))]
    subfiles = map(get_files_in_subtree, folders)
    return sum(subfiles,[])+files


## filepaths: list of files to be used as input
def consolidate(filepaths):
    results = {}
    num_episodes = None
    for fn,fp in filepaths:
        results[fn] = []
        f = open(fp)
        for line in f.readlines():
            line = line.replace("\n","")
            if(len(line)>0 and line[0]!="#"):
                tokens = line.split(" ")
                results[fn].append(tokens[1])
        if(num_episodes == None):
            num_episodes = len(results[fn])
        elif num_episodes > len(results[fn]):
            num_episodes = len(results[fn])
        f.close()
    print "done reading\n"
    #writing output
    return results

####calculates average and standard deviation
def averageResults(results):
    headers = {}
    averagedresults = {}
    for fi in results.keys():
        header = "_".join(fi.split('_')[:-1])
        if header not in headers.keys():
            headers[header]=[ fi]
        else:
            headers[header].append(fi)

    for header in headers.keys():
        avgval = []
        stdval = []

        for episode in range(len(results[headers[header][0]])):
            values = []
            for fi in headers[header]: ##for each repetition
                values.append(float(results[fi][episode]))
            if(len(headers[header]) > 1):
                avg = numpy.mean(values)
                std = numpy.std(values, ddof=1)
            else:
                avg = values[0]
                std = 0.0

            avgval.append(str(avg))
            stdval.append(str(std))

        averagedresults[header] = (avgval, stdval)
    return averagedresults

def writeResults(outpath, results):
    episode = 0
    num_episodes = len(results[results.keys()[0]][0])
    outf = open(outpath, 'w')

    file_headers = []
    for hd in results.keys():
        file_headers.append(hd + "_avg")
        file_headers.append(hd + "_std")

    line = ';'.join(file_headers)+'\n'
    outf.write(line)
    while episode < num_episodes:

        values = []
        for fn in results:
            values.append(results[fn][0][episode])##avg
            values.append(results[fn][1][episode])#stddev
        line = ";".join(values)+'\n'
        outf.write(line)
        episode+=1
    outf.close()

if __name__=="__main__":
    if len(sys.argv) < 3:
        print "consolidateresutls.py subtreeroot outfile"
        sys.exit(1)
    results = consolidate(get_files_in_subtree(sys.argv[1]))
    avgres = averageResults(results)
    writeResults(sys.argv[2], avgres)
