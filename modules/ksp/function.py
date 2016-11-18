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
