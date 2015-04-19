# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

#
# ---------- THOUGHT PROCESS ----------
# Each edge is represented in the mit_map.txt.
# The edges are the distances between each building
# while the nodes are the buildings (represented by numbers)
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    # Create a map for all the values to go into.
    g = WeightedDigraph()
    with open(mapFilename) as inputFile:
        for eachLine in inputFile:
            # For each line in the file split it into a list of numbers.
            numbers = eachLine.split()
            # For the first two numbers add them as nodes.
            for i in range(2):
                new_node = Node(numbers[i])
                # Try to add the node, if it's already in the graph
                # then handle the valueError.
                try:
                    g.addNode(new_node)
                except ValueError:
                    pass
            # Add the edge with the attributes found in numbers.
            new_edge = WeightedEdge(g.getNode(numbers[0]), g.getNode(numbers[1]), numbers[2], numbers[3])
            g.addEdge(new_edge)
    # Give indication that the map is loaded.
    print "Map complete! \n"
    return g

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    # Get every single path
    allPaths = getAllPaths(digraph, start, end)
    shortest = []
    lenShortest = None
    # Look through every path and see which ones are shorter then the max distances
    for path in allPaths:
        totalDist, outdoorDist = lenPath(digraph, path)
        if totalDist <= maxTotalDist and outdoorDist <= maxDistOutdoors:
            # If the shortest length hasn't been set, set it!
            if lenShortest == None:
                shortest = path
                lenShortest = totalDist
                # print "lenShortest was None, now:", lenShortest
            # If the total distance for the path is shorted then the shortest length, change it!
            elif totalDist < lenShortest:
                shortest = path
                # print "this path is shorter! was: {0}, now: {1}".format(lenShortest, totalDist)
                lenShortest = totalDist

    for i in range(len(shortest)):
        temp = shortest[i].getName()
        shortest[i] = temp

    # In case there is no valid path
    if shortest == []:
        raise ValueError
    else:
        return shortest

def getAllPaths(graph, start, end, path = []):
    """
    Returns a list of all valid paths from the start to the end point.

    Parameters:
        graph: a instance of the class Digraph or its subclass
        start, end: start & end building numbers (strings)
        path: a list of the class Node (or subclass) instances

    Returns:
        A list of paths
    """
    # Convert start and end to Nodes
    start, end = Node(start), Node(end)
    # Append the starting node to path
    path = path + [start]
    # If start is equal to the end then return path
    if start == end:
        return [path]
    # Create a variable to store paths
    paths = []
    # For every child of the starting node:
    for child in graph.childrenOf(start):
        # Make sure the child has not already be visited
        if child not in path:
            # Add all valid paths to paths
            paths += getAllPaths(graph, child, end, path)
    return paths


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    shortest = findShortest(digraph, start, end, maxTotalDist, maxDistOutdoors)

    if shortest == None:
        raise ValueError
    else:
        for i in range(len(shortest)):
            temp = shortest[i].getName()
            shortest[i] = temp
        return shortest


def findShortest(graph, start, end, maxTotalDist, maxDistOutdoors, path = [], shortest = None):
    """
    Recursive helper function to directedDFS().
    Required as parameters for directedDFS() are not to be modified.
    For most applications path and shortest should be left to default.
    """
    # Convert start and end to Nodes
    start, end = Node(start), Node(end)
    # Append the starting node to path
    path = path + [start]
    # If start is equal to the end then return path
    if start == end:
        return path
    # For every child of the starting node:
    for child in graph.childrenOf(start):
        # Make sure the child has not already be visited
        if child not in path:
            # If the shortest hasn't been set
            if shortest == None:
                # Create a new path that goes down this arm
                newPath = findShortest(graph, child, end, maxTotalDist, maxDistOutdoors, path, shortest)
                # If the new path doesn't reach a dead end and it's smaller then the max distances
                if newPath != None and all([(x <= y) for x, y in zip(lenPath(graph, newPath), (maxTotalDist, maxDistOutdoors))]):
                    # Change the shortest to the new path
                    shortest = newPath

            # Else if the path is smaller then the shortest route
            elif lenPath(graph, path) < lenPath(graph, shortest):
                # Create a new path that goes down this arm
                newPath = findShortest(graph, child, end, maxTotalDist, maxDistOutdoors, path, shortest)
                # If the new path is not a dead end, is smaller then the max distances and shorter then the shortest so far
                if newPath != None and all([(x <= y) for x, y in zip(lenPath(graph, newPath), (maxTotalDist, maxDistOutdoors))]) and lenPath(graph, newPath) < lenPath(graph, shortest):
                    # Change the shortest to the new path
                    shortest = newPath

    return shortest

def lenPath(graph, path):
    """
    Returns the distance along a given path as an integer.
    graph: a WeightedDigraph class
    path: a list of nodes
    """
    totalDist = 0
    totalOutdoor = 0

    for i in range(len(path)):
        if i == 0:
            continue
        else:
            # Make sure they are nodes
            path[i], path[i-1] = Node(str(path[i])), Node(str(path[i-1]))
            # For every node in the path, look at the one before and find the edge between the two
            edge = graph.findEdge(path[i - 1], path[i])
            # Get the two weights and add them to the totals
            totalDist += int(edge.getTotalDistance())
            totalOutdoor += int(edge.getOutdoorDistance())

    return totalDist, totalOutdoor


# Uncomment below when ready to test
### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    # Test cases
    mitMap = load_map("mit_map.txt")
    # print isinstance(mitMap, Digraph)
    # print isinstance(mitMap, WeightedDigraph)
    # print 'nodes', mitMap.nodes
    # print 'edges for node 32:', mitMap.edges[Node(str(32))]
    # print 'edges for node 56:', mitMap.edges[Node('56')]
    # print 'edges for node 32:', mitMap.edges[mitMap.getNode('32')]
    # validPaths = getAllPaths(mitMap, '32', '56')
    # for path in validPaths:
    #     print path
    # print "{0} valid paths found!".format(len(validPaths))


    LARGE_DIST = 1000000

    # ## Test case 1
    # print "---------------"
    # print "Test case 1:"
    # print "Find the shortest-path from Building 32 to 56"
    # expectedPath1 = ['32', '56']
    # brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    # dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    # print "Expected: ", expectedPath1
    # print "Brute-force: ", brutePath1
    # print "DFS: ", dfsPath1
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

    # ## Test case 2
    # print "---------------"
    # print "Test case 2:"
    # print "Find the shortest-path from Building 32 to 56 without going outdoors"
    # expectedPath2 = ['32', '36', '26', '16', '56']
    # brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    # dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    # print "Expected: ", expectedPath2
    # print "Brute-force: ", brutePath2
    # print "DFS: ", dfsPath2
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

    # ## Test case 3
    # print "---------------"
    # print "Test case 3:"
    # print "Find the shortest-path from Building 2 to 9"
    # expectedPath3 = ['2', '3', '7', '9']
    # brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    # dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    # print "Expected: ", expectedPath3
    # print "Brute-force: ", brutePath3
    # print "DFS: ", dfsPath3
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

    # ## Test case 4
    # print "---------------"
    # print "Test case 4:"
    # print "Find the shortest-path from Building 2 to 9 without going outdoors"
    # expectedPath4 = ['2', '4', '10', '13', '9']
    # brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    # dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    # print "Expected: ", expectedPath4
    # print "Brute-force: ", brutePath4
    # print "DFS: ", dfsPath4
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

    # ## Test case 5
    # print "---------------"
    # print "Test case 5:"
    # print "Find the shortest-path from Building 1 to 32"
    # expectedPath5 = ['1', '4', '12', '32']
    # brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    # dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    # print "Expected: ", expectedPath5
    # print "Brute-force: ", brutePath5
    # print "DFS: ", dfsPath5
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

    # ## Test case 6
    # print "---------------"
    # print "Test case 6:"
    # print "Find the shortest-path from Building 1 to 32 without going outdoors"
    # expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    # brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    # dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    # print "Expected: ", expectedPath6
    # print "Brute-force: ", brutePath6
    # print "DFS: ", dfsPath6
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

    ## Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # ## Test case 8
    # print "---------------"
    # print "Test case 8:"
    # print "Find the shortest-path from Building 10 to 32 without walking"
    # print "more than 100 meters in total"
    # bruteRaisedErr = 'No'
    # dfsRaisedErr = 'No'
    # try:
    #     bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    # except ValueError:
    #     bruteRaisedErr = 'Yes'
    
    # try:
    #     directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    # except ValueError:
    #     dfsRaisedErr = 'Yes'
    
    # print "Expected: No such path! Should throw a value error."
    # print "Did brute force search raise an error?", bruteRaisedErr
    # print "Did DFS search raise an error?", dfsRaisedErr
