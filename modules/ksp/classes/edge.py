class Edge(object):
    """
    Represent an edge in the graph.
    """
    def __init__(self, name, u, v, cost):
        self.name = name
        self.start = u
        self.end = v
        self.cost = cost # represents the edge's cost under free flow

    def __repr__(self):
        return repr(str(str(self.start) + '-' + str(self.end)))
