import osmnx as ox
import geopandas
import pandas as pd
import heapq
from math import cos, asin, sqrt

#read requireced data from json files
nodesData = pd.read_json(path_or_buf="datasets/nodesData.json")
edgesData = pd.read_json(path_or_buf="datasets/edgesData.json")

def loadPunggol():
    #read whole of punggol
    punggol = geopandas.read_file('datasets/entire_punggol.geojson')
    G = ox.graph_from_polygon(punggol.geometry[0])
    return G

def loadEdges(G):
    """
    G - NetworkX Digraph
    Loads all possible edges within graph
    """
    #all possible edges within punggol 
    gdf_edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True) 
    edgesData = pd.DataFrame(gdf_edges[["u", "v", "osmid"]].values, columns=["U", "V", "Edges"])


def loadNodes(G):
    """
    G - NetworkX Digraph
    Loads all possible nodes within graph
    """
    #all possible nodes within punggol
    coords = [[node, data['x'], data['y']] for node, data in G.nodes(data=True)]
    nodesData = pd.DataFrame(coords, columns=['node', 'x', 'y'])

"""
Average walking speed = 5km/h
Average drive speed = 64km/h
"""

class Node:
    """
    parent - parent node of current node
    position - current position of node (Longitude, Latitude)
    g - cost from start to current node
    h - heuristics based estimated cost for current node to end node
    f - total cost of present node (f = g + h)
    """
    def __init__(self, position = None, parent = None):
        self.parent = parent
        self.position = position
        #position[0] = Longitutde
        #position[1] = Latitude
        self.f = 0
        self.g = 0
        self.h = 0
        if self.position is not None:
            self.ID = self.getID()
    #get methods
    def getLat(self):
        return self.position[1]
    def getLon(self):
        return self.position[0]
    #toString
    def __repr__(self):
        return f"{self.position} - parent: {type(self.parent)} g: {self.g} h: {self.h} f: {self.f} ID: {self.ID}"
    #test for lesser than
    def __lt__(self, other):
        return self.f < other.f
    #test for greater than
    def __gt__(self, other):
        return self.f > other.f
    #returns own OSMID/Node ID of node by searching position in nodesData
    def getID(self):
        if(self.position is not None):
            row = nodesData[(nodesData['X'] == self.position[0]) & (nodesData['Y'] == self.position[1])]
            self.ID = row.Node_ID.item()
            return row.Node_ID.item()
    #return a list of possible movement to that node's ID
    def possibleMoves(self):
        row = edgesData[edgesData["U"] == self.getID()]
        return row.V.values

#takes in return path and plots it within osmnx
def plotPath(path):
    G = loadPunggol()
    ox.plot_graph_route(G, path)

def returnPath(currentNode, output="coords"):
    """
    Returns the list of node ID or coords that can reach the end point
    output: "graph" - generate a graph, "ID" - return back list of Node IDs, "coords" - return back a list of coordinates towards end destination
    """
    path = []
    current = currentNode
    while current != None:
        #backtrack to first node via parent
        path.append(current.ID)
        current = current.parent
    if output == "ID":
        return path[::-1]
    if output == "graph":
        return plotPath(path[::-1])
    if output == "coords":
        #convert ID to coordindates
        Coords = []
        for node in path:
            converted = IDtoCoord(node)
            Coords.append(converted)
        return Coords[::-1]


def search(start, end, output="graph"):
    """
    start - Starting position tuple (Longitude, Latitude)
    end - Ending position tuple (Longitude, Latitude)
    Pass final node into returnPath() to determine best path
    """
    #initialize start, current and end nodes
    startNode = Node(position=start)
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(position=end)
    endNode.g = endNode.h = endNode.f = 0
    #initialize list used to track visited nodes
    traversedList = []
    untraversedList = []
    #set up heap queue
    heapq.heapify(untraversedList) 
    heapq.heappush(untraversedList, startNode)
    #conditions to avoid infinite loops 
    currentIterations = 0
    maxInterations = (len(edgesData) // 2)
    
    #begin searching
    while len(untraversedList) > 0:
        currentIterations += 1
        #could not find route within the limit
        if currentIterations > maxInterations:
            print("Too many iterations, giving up route search")
            return None
        #start moving
        currentNode = heapq.heappop(untraversedList)
        traversedList.append(currentNode)
        #found route to end node
        if ((currentNode.position[0] == endNode.position[0]) and (currentNode.position[1] == endNode.position[1])):
            return returnPath(currentNode, output)
        #generate children nodes
        children = []
        for i in currentNode.possibleMoves():
            newNode = Node(position=IDtoCoord(i), parent=currentNode)
            children.append(newNode)
        #consider possible paths generated from children
        for child in children:
            #child already visited, skip
            if skipNode(child, traversedList) == -1:
                continue
            child.g = currentNode.g + 1
            child.h = haversine(startNode.getLat(), startNode.getLon(), child.getLat(), child.getLon())
            child.f = child.g + child.h
            #child already noted, skip
            if skipNode(child, untraversedList) == -1:
                continue
            # Add the child to list to travel to
            heapq.heappush(untraversedList, child)
    #could not reach destination
    print("Unable to find route")
    return None

#Calculate distance between 2 lat and long points using the Haversine formula
def haversine(lat1, long1, lat2, long2):
    #p = pi/180
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((long2 - long1) * p)) / 2
    return 12742 * asin(sqrt(a))

#return a tuple of coordinates provided by the ID (Longitude, Latitude)
def IDtoCoord(ID):
    row = nodesData[(nodesData['Node_ID'] == ID)]
    return (row.X.item(), row.Y.item())

#checks for duplicate nodes within the listOfNodes
def skipNode(node, listOfNodes):
    for i in listOfNodes:
        if i.ID == node.ID:
            return -1
    return 0

"""
test parameters
"""
#test start - 98 punggol walk
tempstart = (103.8983854, 1.4012395)
#test end - punggol rd
tempend = (103.9057549, 1.401378)
print(search(tempstart, tempend))

