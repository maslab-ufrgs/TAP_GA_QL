from py_expression_eval import Parser

class Driver(object):
    '''
    Represents a driver in the network.

    Input:
    od: OD = instance of OD class

    >>> type(Driver(OD(1, 2, 8, 15)))
    <class '__main__.Driver'>
    '''

    def __init__(self, OD):
        """
        Class constructor.

        >>> isinstance(Driver(OD(1, 2, 8, 15)), Driver)
        True
        >>> isinstance(Driver(1), Driver)
        True
        >>> isinstance(Driver(OD(1, 2, 8, 15)).od, OD)
        True

        The class contructor needs to be more precise about its input.
        """
        self.od = OD

    def od_s(self):
        """
        String of OD pair of the Driver.
        Could be substituted by the __repr__ method.

        >>> Driver(1).od_s()
        Traceback (most recent call last):
        ...
        AttributeError: 'int' object has no attribute 'o'
        >>> Driver(OD(1, 2, 8, 15)).od_s()
        '12'
        """
        return "%s%s" % (self.od.o, self.od.d)

    def __repr__(self):
        """
        __repr__ method override.

        >>> Driver(OD(1, 2, 8, 15))
        '1|2'
        """
        return repr(str(self.od.o) + '|' + str(self.od.d))


class OD(object):
    """
    Represents an origin-destination pair, where:

    Inputs:
    origin: string = origin node
    destiny: string = destination node
    num_path: int = number of shortest paths to generate
    num_travels: int = number of travels

    Tests to verify the attributes:
    >>> isinstance(OD('A', 'B', 5, 100), OD)
    True
    >>> type(OD('A', 'B', 5, 100))
    <class '__main__.OD'>
    >>> isinstance(OD(1, 2, 3, 4).o, int)
    True
    >>> isinstance(OD('A', 'B', 5, 100).o, str)
    True

    Tests #3 and #4 sugests that self.o and self.d need to be more strictly
    controlled perhaps converting the O and the D to a string is a solution.

    ** OD notation: origin|destiny
    """

    def __init__(self, origin, destiny, num_paths, num_travels):
        """
        Class Constructor.

        >>> OD('A', 'B', 5, 100).o
        'A'
        >>> OD('A', 'B', 5, 100).d
        'B'
        >>> OD('A', 'B', 5, 100).numPaths
        5
        >>> OD('A', 'B', 5, 100).numTravels
        100
        >>> OD('A', 'B', 5, 100).paths
        """
        self.o = origin
        self.d = destiny
        self.numPaths = num_paths
        self.numTravels = num_travels
        self.paths = None

    def __str__(self):
        """
        __str__ method override.

        >>> print OD('A', 'B', 5, 100)
        Origin: A, Destination: B, Number of travels: 100, Number of shortest paths: 5
        """
        return "Origin: " + str(self.o) + ", Destination: " + str(self.d) + \
            ", Number of travels: " + str(self.numTravels) + ", Number of shortest paths: " \
            + str(self.numPaths)


class Node(object):
    '''
    Represents a node in the graph.

    Input:
    name: string = name of the node

    These are the tests to verify if the object is being instantiated as it should:
    >>> isinstance(Node('nome'), Node)
    True
    >>> isinstance(Node(1).name, int)
    True
    >>> isinstance(Node('nome').name, str)
    True
    >>> type(Node(1))
    <class '__main__.Node'>

    Tests #2 and #3 have the same observation as the tests #7 and #8 of the OD class.
    '''

    def __init__(self, name):
        """
        Class constructor.

        >>> Node('nome').name
        'nome'
        >>> Node('nome').dist
        1000000
        >>> Node('nome').prev
        >>> Node('nome').flag
        0
        """
        self.name = name
        self.dist = 1000000  # distance to this node from start node (?)
        self.prev = None     # previous node to this node
        self.flag = 0        # access flag

    def __repr__(self):
        """
        __repr__ method override.

        >>> Node(1)
        1
        >>> Node('nome')
        'nome'
        """
        return repr(self.name)


class Edge(object):
    """
    Represents an edge in the graph.

    Inputs:
    start: string = start node of the edge
    end: string = end node of the edge
    length: float = length of the edge
    cost_formula: string = cost formula of the edge
    var_value: float = value for the function to calculate the cost_formula

    >>> isinstance(Edge('a', 'b', 11, '12+5*t'), Edge)
    True
    >>> type(Edge('a', 'b', 11, '12+5*t'))
    <class '__main__.Edge'>

    ** Edge notation: origin-destiny
    """

    def __init__(self, start, end, length, cost_formula):
        """
        Class constructor.

        >>> Edge('a', 'b', 11, '12+5t').start
        'a'
        >>> Edge('a', 'b', 11, '12+5t').end
        'b'
        >>> Edge('a', 'b', 11, '12+5t').length
        11
        >>> Edge('a', 'b', 11, '12+5*t').cost_formula
        '12+5*t'
        """
        self.start = start
        self.end = end
        self.length = length  # FreeFlow of the edge (?)
        self.cost_formula = cost_formula

    def eval_cost(self, var_value):
        """
        The eval_cost method calculates the value of the cost formula for a given var_value:

        WARNING: the variable in the function MUST be f.
        >>> Edge(1, 2, 3, '5+5*f').eval_cost(5.0)
        30.0
        >>> Edge(1, 2, 3, '5+5*t').eval_cost(5.0)
        Traceback (most recent call last):
        ...
        Exception: undefined variable: t
        """
        parser = Parser()
        exp = parser.parse(self.cost_formula)
        #Hardcoded variable 'f'
        return exp.evaluate({'f': var_value})

    def __repr__(self):
        """
        __repr__ method override.

        >>> Edge('a','k', 11, '12+5*t')
        'a-k'
        >>> Edge(1,2,11,'12+5*t')
        '1-2'
        """
        return repr(str(str(self.start) + '-' + str(self.end)))

