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
