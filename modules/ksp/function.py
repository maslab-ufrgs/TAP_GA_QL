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
