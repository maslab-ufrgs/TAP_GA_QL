import string
import os
from modules.experiment.classes import *
from py_expression_eval import Parser
from ksp.KSP import *

def is_number(arg):
    '''
    This function try to convert whatever is its argument to a float number.

    Input:
    arg: anything = the object that it tries to convert to a number.

    Output:
    True if it converts successfully to a float.
    False if it can't, by getting a ValueError exception.

    >>> is_number(1)
    True
    >>> is_number(1e1000)
    True
    >>> is_number('5000')
    True
    >>> is_number(3.141598)
    True
    >>> is_number('a')
    False
    >>> is_number('hello')
    False
    >>> is_number(Node('a'))
    Traceback (most recent call last):
    ...
    TypeError: float() argument must be a string or a number
    '''
    try:
        float(arg)
        return True
    except ValueError:
        return False

def generate_table_fill(coupling_file):
    """
    Read the coupling file contents and create the table fill.

    In:
    coupling_file:string = path to coupling file.

    Out:
    table_fill:dictionary = table fill.
    """
    table_fill = {}
    for line in open(coupling_file, 'r'):
        if line.strip() != '':
            line = line.split()
            if '#' not in line[0]:
                list_values = []
                for value in line:
                    if value != line[0]:
                        list_values.append(float(value))
                table_fill[line[0]] = list_values

    return table_fill

def clean_od_table(ODL, k):
    """
    Zeroes the OD table.
    """
    TABLE_FILL = {}
    for od_pair in ODL:
        TABLE_FILL[str(od_pair)] = [0] * k

    return TABLE_FILL

def nodes_string(print_od_pair, print_travel_time, print_drivers_link, print_drivers_route,
        od_list, edge_names, od_header):
    """
    String of edges of the graph that will be printed or stored in the file.
    """
    nodes_string = ''
    if print_od_pair:
        for od in od_list:
            nodes_string += "tt_%s|%s " % (od.o, od.d)
    if print_travel_time:
        for edge in edge_names:
            nodes_string += 'tt_' + edge + ' '
    if print_drivers_link:
        for edge in edge_names:
            nodes_string += "nd_" + edge + ' '
    if print_drivers_route:
        nodes_string += od_header
    nodes_string = nodes_string.strip()
    return nodes_string

def nd(drivers, group_size):
    """
    Number of drivers.
    """
    return len(drivers) * group_size

def appendTag(filenamewithtag):
    """
        Test if there isn't already a file with the desired name,
        paralellization of experiments may result in filename conflict.
    """
    append_number = ''
    while(os.path.isfile(filenamewithtag + append_number + ".txt")):
        if(append_number == ''):
            append_number = "-1"
        else:
            append_number = "-" + str(int(append_number[1:]) + 1)
    filenamewithtag += append_number + ".txt"
    return filenamewithtag

def read_infos(graph_file, edges):
    """
    Read the edges and OD pairs from the file in this program format(with the functions of each).
    In:
        graph_file:String = Path to the network file.
        edges:Edge = List of edges returned by the generathGraph function.
    Out:
        new_edges:EdgeRC = List of edges in the correct form for this program.
    """
    functions = {}
    new_edges = []
    od_list = []

    for line in open(graph_file, 'r'):
        taglist = string.split(line)
        if taglist[0] == 'function':
            variables = []
            variables = taglist[2].replace('(','')
            variables = variables.replace(')','')
            variables = variables.split(',')
            functions[taglist[1]] = [taglist[3], variables]

        elif taglist[0] == 'dedge' or taglist[0] == 'edge':
            constants = []
            cost_formula = ""
            freeflow_cost = 0
            constant_acc = 0
            if len(taglist) > 5:
                i = 5
                while i <= (len(taglist) - 1):
                    constants.append(taglist[i])
                    i += 1
                parser = Parser()
                ##[4] is function name.[0] is expression
                exp = parser.parse(functions[taglist[4]][0])
                LV = exp.variables()
                buffer_LV = []
                for l in LV:
                    if l not in functions[taglist[4]][1]:
                        constant_acc += 1
                        buffer_LV.append(l)

                #check if the formula has any parameters(variables)
                flag = False
                for v in functions[taglist[4]][1]:
                    if v in LV:
                        flag = True

                buffer_dic = {}
                i = 0
                for index in range(constant_acc):
                    buffer_dic[buffer_LV[index]] = float(constants[index])
                    i = 1

                if not flag:
                    freeflow_cost = exp.evaluate(buffer_dic)
                    cost_formula = str(freeflow_cost)

                elif is_number(functions[taglist[4]][0]):
                    cost_fomula = functions[taglist[4]][0]

                else:
                    exp = exp.simplify(buffer_dic)
                    cost_formula = exp.toString()

                for edge in edges:
                    if edge.name == taglist[1] and (edge.start == taglist[2] or edge.start == taglist[3]) \
                    and (edge.end == taglist[2] or edge.end == taglist[3]):
                        new_edges.append(EdgeRC(edge.name, edge.start, edge.end, edge.cost,
                                                cost_formula))
                        if taglist[0] == 'edge':
                            new_edges.append(EdgeRC('%s-%s'%(edge.end, edge.start), edge.end, edge.start, edge.cost,
                                                    cost_formula))

            else:
                cost_formula = ""
                freeflow_cost = 0
                parser = Parser()
                if is_number(functions[taglist[4]][0]):
                    cost_formula = functions[taglist[4]][0]

                else:
                    exp = parser.parse(functions[taglist[4]][0])
                    cost_formula = exp.toString()

                for edge in edges:
                    if edge.name == taglist[1] and (edge.start == taglist[2] or edge.start == taglist[3]) \
                    and (edge.end == taglist[2] or edge.end == taglist[3]):
                        new_edges.append(EdgeRC(edge.name, edge.start, edge.end, edge.cost,
                                                cost_formula))
                        if taglist[0] == 'edge':
                            new_edges.append(EdgeRC(edge.name, edge.end, edge.start, edge.cost,
                                                    cost_formula))

        elif taglist[0] == 'od':
            od_list.append((taglist[2], taglist[3], float(taglist[4])))

    return new_edges, od_list

# main procedure for many OD-pairs
def runRC(graph_file, K, OD_pairs=None, flow=0.0):
    lout = []
    # read graph from file
    N, E, OD = generateGraph(graph_file, flow)
    # process the list of OD-pairs (if no OD pair was defined by the 
    # user, then all OD pairs from the network file are considered)
    if OD_pairs != None:
        OD = OD_pairs.split(';')
    for i in xrange(0,len(OD)):
        OD[i] = OD[i].split('|')
    # find K shortest paths of each OD-pair
    lastod = len(OD)-1
    for iod, (o, d) in enumerate(OD):
        # find K shortest paths for this specific OD-pair
        S = KShortestPaths(N, E, o, d, K)
        # print the result for this specific OD-pair
        last = len(S)-1
        for i, path in enumerate(S):
            lout.append([pathToListOfString(path, E), calcPathCost(path, E)])
    return lout
