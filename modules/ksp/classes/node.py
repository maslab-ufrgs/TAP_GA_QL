class Node:
        """
        Represents a node in the graph
        """
	def __init__(self, name):
		self.name = name	# name of the node
		self.dist = 1000000	# distance to this node from start node
		self.prev = None	# previous node to this node
		self.flag = 0		# access flag

