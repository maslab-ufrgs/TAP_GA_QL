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
