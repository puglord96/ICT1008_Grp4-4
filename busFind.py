import osmnx as ox
import geopandas
import pandas as pd
import heapq
from math import cos, asin, sqrt

#read required data from csv files
nodesData = pd.read_csv("datasets/allBusNodes.csv")
edgesData = pd.read_csv("datasets/allBusEdges.csv")

#plot punggol on a graph
def loadPunggol():
    #read whole of punggol
    punggol = geopandas.read_file('datasets/entire_punggol.geojson')
    G = ox.graph_from_polygon(punggol.geometry[0])
    return G

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
        self.f = 0
        self.g = 0
        self.h = 0
        self.ID = self.getID()
        #list of possible buses to take
        self.services = self.possibleServices()
        if self.services is None:
            print("Error - Found a bus stop without services")
    #get methods
    def getLat(self):
        return self.position[1]
    def getLon(self):
        return self.position[0]
    #get bus stop id
    def getID(self):
        tempLat = self.position[1]
        tempLong = self.position[0]
        for idx in nodesData.values:
            #print("comparing " + str(tempLat) + " and " + str(idx[1]))
            if tempLat == idx[1] and tempLong == idx[0]:
                return idx[3]
        print(f"ID Error - Could not resolve position to ID for {self.position}")

    #return possible services from bus stop
    def possibleServices(self):
        for idx in nodesData.values:
            if self.ID == idx[3]:
                return idx[2]
        print(f"Error - No bus services found at bus stop ID: {self.ID}")

    #toString
    def __repr__(self):
        return f"{self.position} - parent: {type(self.parent)} g: {self.g} h: {self.h} f: {self.f} ID: {self.ID} Services: {self.services}"
    #test for lesser than
    def __lt__(self, other):
        return self.f < other.f
    #test for greater than
    def __gt__(self, other):
        return self.f > other.f
    #return a list of possible movement to that node's ID and possible services
    def possibleMoves(self):
        moves = []
        services = self.services.split(',')
        count = 0
        try:
            for row in edgesData.values:
                row = list(row)
                if count == len(services):
                    break
                if row[2] in services and row[0] == self.ID:
                    moves.append((services[count], row[1]))
                    count += 1
            return moves
        except ValueError:
            print("ID Error - No coordinates match within files")
            return None

def returnPath(currentNode, output="coords"):
    """
    Returns the list of node ID or coords that can reach the end point
    output: "ID" - return back list of Bus stop IDs, "coords" - return back a list of coordinates towards end destination
    """
    path = []
    current = currentNode
    busUsed = checkService(currentNode)
    while current != None:
        #backtrack to first node via parent
        path.append(current.ID)
        current = current.parent
    if output == "ID":
        #attach buses used and reverse array
        path = path[::-1]
        path.insert(0, busUsed)
        return path
    if output == "coords":
        #convert ID to coordindates
        Coords = []
        for place in path:
            converted = IDtoCoord(place)
            Coords.append(converted)
        #attach buses used and reverse array
        Coords = Coords[::-1]
        Coords.insert(0, busUsed)
        return Coords

def checkService(endNode):
    endServices = endNode.services
    final = []
    while endNode != None:
        endNode = endNode.parent
        #endNode becomes none once it hits the start point
        if endNode is None:
            break
        #get possible services
        arr = endNode.services.split(',')
        for service in arr:
            if service in endServices:
                if service not in final:
                    final.append(service)
    return final


def search(start, end, output="graph"):
    """
    start - Starting position tuple (Longitude, Latitude)
    end - Ending position tuple (Longitude, Latitude)
    Pass final node into returnPath() to determine best path
    """
    start = checkNodes(start)
    end = checkNodes(end)
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
            newNode = Node(position=IDtoCoord(i[1]), parent=currentNode)
            children.append(newNode)
        #consider possible paths generated from children
        for child in children:
            #bus service unavailable in final node, skip
            endServices = endNode.services.split(',')
            childServices = child.services.split(',')
            servicesCheck = list(set(endServices).intersection(childServices))
            if len(servicesCheck) <= 0:
                continue
            #child already visited, skip
            if skipNode(child, traversedList) == -1:
                continue
            child.g = currentNode.g + (1/28) # Average bus speed is 28km/h
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
    for row in nodesData.values:
        if ID == row[3]:
            return (row[0], row[1])

#checks for duplicate nodes within the listOfNodes
def skipNode(node, listOfNodes):
    for i in listOfNodes:
        if i.ID == node.ID:
            return -1
    return 0

#checks if the nodes exist within the walking dataset, if not, get the nearest node
def checkNodes(coords): 
    """
    coords - tuple of coordinates to get nearest nodes
    returns coordinates of nearest node within dataset
    """
    tempCoords = []
    tempHav = []
    for row in nodesData.values:
        tempHav.append(haversine(coords[1], coords[0], row[0], row[1]))
        tempCoords.append((row[1], row[0]))
    val, idx = min((val, idx) for (idx, val) in enumerate(tempHav))
    lat = tempCoords[idx][1]
    lon = tempCoords[idx][0]
    return (lat, lon)

"""
test parameters
"""
tempstart = (103.9022434, 1.403706299)
tempend = (103.9024832, 1.416083732) 
#print(search(tempstart, tempend, output="coords"))

