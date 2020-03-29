from collections import defaultdict
import csv
from math import radians, cos, sin, asin, sqrt
import re

# This is to display only the Punggol area mrt lrt
def readMRTPunggol():
    newArea = []
    with open("datasets/mrtfaretime.csv", 'r') as f:
        next(f)
        data = list(csv.reader(f, delimiter=","))
    f.close()
    for row in data:
        row[0] = row[0].replace('\xa0', ' ').encode('utf-8')
        row[0] = re.sub(' {2,}', ' ', row[0])
        row[1] = row[1].replace('\xa0', ' ').encode('utf-8')
        row[1] = re.sub(' {2,}', ' ', row[1])
        row[8] = row[8].replace('\xa0', '').encode('utf-8')
        row[11] = row[11].replace('\xa0', '').encode('utf-8')

        # Check if the values are in row 8 and 11
        if "PE" in row[8] and "PE" in row[11]:
            newArea.append(row)
        if "PW" in row[8] and "PW" in row[11]:
            newArea.append(row)
        elif "PE" in row[8] and "PW" in row[11]:
            newArea.append(row)
        elif "PW" in row[8] and "PE" in row[11]:
            newArea.append(row)
        elif "PE" in row[8] and "NE17" in row[11]:
            newArea.append(row)
        elif "PW" in row[8] and "NE17" in row[11]:
            newArea.append(row)
        elif "NE17" in row[8] and "PE" in row[11]:
            newArea.append(row)
        elif "NE17" in row[8] and "PW" in row[11]:
            newArea.append(row)
    newArea = calculate_distance(newArea)
    return newArea


def calculate_distance(punggolMRT):
    for row in punggolMRT:
        x = distance(float(row[9]), float(row[12]), float(row[10]), float(row[13]))
        x = float("%.2f" % round(x, 2))
        row.insert(14, x)
    return punggolMRT


def add_edges_mrt(punggolMRT, edges):
    PW = ("NE17", "PW1", "PW3", "PW4", "PW5", "PW6", "PW7", "NE17")
    PE = ("NE17", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PE7", "NE17")
    i = 0
    j = 8
    k = 0
    l = 7
    for row in punggolMRT:
        if (row[8] == PE[i]) and (row[11] == PE[i + 1]):
            edges.append((row[0], row[1], row[14]))
            i += 1
        elif (row[8] == PE[j]) and (row[11] == PE[i - 1]):
            edges.append((row[0], row[1], row[14]))
            j -= 1
        elif (row[8] == PW[k]) and (row[11] == PW[k + 1]):
            edges.append((row[0], row[1], row[14]))
            k += 1
        elif (row[8] == PW[l]) and (row[11] == PW[l - 1]):
            edges.append((row[0], row[1], row[14]))
            l -= 1
    return edges


def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # The value of Radius of earth taken as 6371. Use 3956 for miles
    r = 6371
    return c * r

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

graph = Graph()
edges = [
    ("NE17 PTC Punggol", "bus 101 stop 1", 7),
    ("NE17 PTC Punggol", "bus 102 stop 1", 9),
    ("NE17 PTC Punggol", "bus 103 ", 14),
    ("bus 101 stop 1", "bus 102 stop 2", 10),
    ("bus 101 stop 1", "bus 101 stop2", 15),
    ("bus 102 stop 1", "bus 101 stop 2", 11),
    ("bus 102 stop 1", "f", 2),
    ("bus 101 stop 2", "SIT", 6),
]

dataPunggolMRT = readMRTPunggol()
edges = add_edges_mrt(dataPunggolMRT, edges)
for edge in edges:
    graph.add_edge(*edge)
print (dijsktra(graph, 'PW4 Samudera', 'SIT'))