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

def generate_graph(graph_file, print_edges=False, flow=0):
    """
    Reads the .net file and return it's infos.
    The infos are:
        function(s)
        node(s)
        arc(s)
        edge(s)
        od(s)

    It should be following the specification from:
        https://wiki.inf.ufrgs.br/Network_files_specification

    It returns a list of vertices(V), a list of edges(E) and a list of OD(ODlist)

    Tests:
    """
    vertices = []
    edges = []
    functions = {}
    od_list = []

    for line in open(graph_file, 'r'):
        taglist = string.split(line)
        if taglist[0] == 'function':
            variables = []
            variables = taglist[2].replace("(", "")
            variables = variables.replace(")", "")
            variables = variables.split(",")
            functions[taglist[1]] = [taglist[3], variables]

        elif taglist[0] == 'node':
            vertices.append(Node(taglist[1]))

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
                    freeflow_cost = float(functions[taglist[4]][0])
                    cost_fomula = functions[taglist[4]][0]

                else:
                    exp = exp.simplify(buffer_dic)
                    cost_formula = exp.toString()
                    exp = Parser()
                    cost_formula2 = "(" + cost_formula + ") + flow"
                    exp = exp.parse(cost_formula2)
                    freeflow_cost = exp.evaluate({'f': 0, 'flow': flow})  # Hardcoded

                edges.append(Edge(taglist[2], taglist[3],
                                  freeflow_cost, cost_formula))
                if taglist[0] == 'edge':
                    edges.append(Edge(taglist[3], taglist[2],
                                      freeflow_cost, cost_formula))

            else:
                cost_formula = ""
                freeflow_cost = 0
                parser = Parser()
                if is_number(functions[taglist[4]][0]):
                    cost_formula = functions[taglist[4]][0]
                    freeflow_cost = float(functions[taglist[4]][0])

                else:
                    exp = parser.parse(functions[taglist[4]][0])
                    cost_formula = exp.toString()
                    cost_formula2 = "(" + cost_formula + ") + flow"
                    exp = exp.parse(cost_formula2)
                    freeflow_cost = exp.evaluate({'f': 0, 'flow': flow})  # hardcoded

                edges.append(Edge(taglist[2], taglist[3],
                                  freeflow_cost, cost_formula))
                edges.append(Edge(taglist[3], taglist[2],
                                  freeflow_cost, cost_formula))

        elif taglist[0] == 'od':
            od_list.append((taglist[2], taglist[3], int(taglist[4])))
    '''
    Print edges and their costs but there are too many lines to be printed!!
    '''
    if print_edges:
        for e in edges:
            print("Edge " + str(e.start) + "-"
                  + str(e.end) + " has length: " + str(e.length))


    return vertices, edges, od_list

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

# return a list with the K shortest paths for the given origin-destination pair,
# given the lists of nodes and edges (this function was created to be called
# externally by another applications)
def getKRoutes(N, E, origin, destination, K):

	lout = []

	# find K shortest paths for this specific OD-pair
	S = KShortestPaths(N, E, origin, destination, K)

	for path in S:
		# store the path (in list of strings format) and cost to the out list 
		lout.append([pathToListOfString(path), calcPathLength(path, E)])

	return lout

# Yen's K shortest loopless paths algorithm
def KShortestPaths(V, E, origin, destination, K):
	# the K shortest paths
	A = []

	# potential shortest paths
	B = []

	for k in xrange(1,K+1):
		try:
 			if not runKShortestPathsStep(V, E, origin, destination, k, A, B):
			 	break
		except:
 			print('Problem on generating more paths@ Only %d paths were found!' % (k-1))
 			break

	return A

def runKShortestPathsStep(V, E, origin, destination, k, A, B):
	# Step 0: iteration 1
	if k == 1:
		A.append(findShortestPath(V, E, origin, destination, []))

	# Step I: iterations 2 to K
	else:
		lastPath = A[-1]
		for i in range(0, len(lastPath)-1):
			# Step I(a)
			spurNode = lastPath[i]
			rootPath = lastPath[0:i+1]
			toIgnore = []

			for path in A:
				if path[0:i+1] == rootPath:
					ed = getEdge(E, spurNode.name, path[i+1].name)
					toIgnore.append(ed)

			# ignore the edges passing through nodes already in rootPath (except for the spurNode)
			for noder in rootPath[:-1]:
				edgesn = pickEdgesListAll(noder, E)
				for ee in edgesn:
					toIgnore.append(ee)

			# Step I(b)
			spurPath = findShortestPath(V, E, spurNode.name, destination, toIgnore)
			if spurPath[0] != spurNode:
				continue

			# Step I(c)
			totalPath = rootPath + spurPath[1:]
			B.append(totalPath)

		# handle the case where no spurs (new paths) are available
		if not B:
			return False

		# Step II
		bestInB = None
		bestInBlength = 999999999
		for path in B:
			length = calcPathLength(path, E)
			if length < bestInBlength:
				bestInBlength = length
				bestInB = path
		A.append(bestInB)
		while bestInB in B:
			B.remove(bestInB)

	return True

# Dijkstra's shortest path algorithm
def findShortestPath(N, E, origin, destination, ignoredEdges):

	# reset the graph (so as to discard information from previous runs)
	resetGraph(N, E)

	# set origin node distance to zero, and get destination node
	dest = None
	for node in N:
		if node.name == origin:
			node.dist = 0
		if node.name == destination:
			dest = node

	u = pickSmallestNode(N)
	while u != None:
		u.flag = 1
		uv = pickEdgesList(u, E)
		n = None
		for edge in uv:

			# avoid ignored edges
			if edge in ignoredEdges:
				continue

			# take the node n
			for node in N:
				if node.name == edge.end:
					n = node
					break
			if n.dist > u.dist + edge.length:
				n.dist = u.dist + edge.length
				n.prev = u

		u = pickSmallestNode(N)
		# stop when destination is reached
		if u == dest:
			break

	# generate the final path
	S = []
	u = dest
	while u.prev != None:
		S.insert(0,u)
		u = u.prev
	S.insert(0,u)

	return S

# reset graph's variables to default
def resetGraph(N, E):
	for node in N:
		node.dist = 1000000.0
		node.prev = None
		node.flag = 0

# returns the smallest node in N but not in S
def pickSmallestNode(N):
	minNode = None
	for node in N:
		if node.flag == 0:
			minNode = node
			break
	if minNode == None:
		return minNode
	for node in N:
		if node.flag == 0 and node.dist < minNode.dist:
			minNode = node
	return minNode

# returns the list of edges starting in node u
def pickEdgesList(u, E):
	uv = []
	for edge in E:
		if edge.start == u.name:
			uv.append(edge)
	return uv

# generate a list with the edges' names of a given route S
def pathToListOfString(S):
	lout = []
	for i in xrange(0,len(S)-1):
		lout.append(str(S[i].name) + '|' + str(S[i+1].name))
	return lout

# calculate path S's length
def calcPathLength(S, E):
	length = 0
	prev = None
	for node in S:
		if prev != None:
			length += getEdge(E, prev.name, node.name).length
		prev = node

	return length

# get the directed edge from u to v
def getEdge(E, u, v):
	for edge in E:
		if edge.start == u and edge.end == v:
			return edge
	return None

# returns the list of edges that start or end in node u
def pickEdgesListAll(u, E):
	uv = []
	for edge in E:
		if edge.start == u.name or edge.end == u.name:
			uv.append(edge)
	return uv
