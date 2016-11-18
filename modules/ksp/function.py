# return a list with the K shortest paths for the given origin-destination pair,
# given a network file (this function was created to be called externally by
# another applications)
def getKRoutesNetFile(graph_file, origin, destination, K):

	lout = []

	# read graph from file
	N, E, _ = generateGraph(graph_file)

	# find K shortest paths for this specific OD-pair
	S = KShortestPaths(N, E, origin, destination, K)

	for path in S:
		# store the path (in list of strings format) and cost to the out list
		lout.append([pathToListOfString(path, E), calcPathCost(path, E)])

	return lout
