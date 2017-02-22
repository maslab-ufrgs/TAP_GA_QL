import string
import os
from modules.experiment.classes import *

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

def eval_cost(edge, var_value):
    """
    Calculates the value of the cost formula for a given var_value.
    In:
        edge:Edge = Instance of the Edge class.
        var_value:Float = Variable value.

    Out:
        value:Float = Result of the calculation.
    """
    return edge.func_info[1].evaluate({edge.func_info[1]:var_value})
