import os
import sys
#gets all files in the subtree with path as root
def get_files_in_subtree(path):
    children = os.listdir(path)
    files = [(f, os.path.join(path,f)) for f in children if os.path.isfile(os.path.join(path, f))]

    folders = [os.path.join(path,f) for f in children if not os.path.isfile(os.path.join(path, f))]
    subfiles = map(get_files_in_subtree, folders)
    return sum(subfiles,[])+files


## filepaths: list of files to be used as input
def consolidate(filepaths, outpath):
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
    episode = 0
    outf = open(outpath, 'w')
    line = ';'.join(zip(*filepaths)[0])+'\n'
    outf.write(line)
    while episode < num_episodes:
        values = []
        for fn,_ in filepaths:
            values.append(results[fn][episode])
        line = ";".join(values)+'\n'
        outf.write(line)
        episode+=1
    outf.close()

if __name__=="__main__":
    if len(sys.argv) < 3:
        print "consolidateresutls.py subtreeroot outfile"
        sys.exit(1)
    consolidate(get_files_in_subtree(sys.argv[1]), sys.argv[2])