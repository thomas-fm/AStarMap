import math
from collections import deque
class Node:

    def __init__(self, name):
        self.name = name
        self.neighbours = []
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None
        self.x = 0
        self.y = 0
    def AddNeighbour(self, neighbour):
        self.neighbours.append(neighbour)
    def SetParent(self, parent):
        self.parent = parent
    def SetH(self, h):
        self.h = h
    def SetG(self, g):
        self.g = g
    def SetF(self, f):
        self.f = f
    def GetG(self, g):
        return self.g
    def GetH(self, h):
        return self.h
    def GetParent(self):
        return self.parent
    def GetNeighbour(self):
        return self.neighbours
    def FindF(self):
        return self.g + self.h

class Graph:

    def __init__(self):
        self.ListOfNode = []
        self.ListOFNodePosition = []
        self.AdjMatrix = []
        self.nNode = 0
    def InsertNode(self, node):
        self.ListOfNode.append(node)
    def GetNode(self, idx):
        try:
            return self.ListOfNode[idx]
        except:
            return None
    def GetNodeNeighbour(self, idx):
        return self.ListOfNode[idx].GetNeighbour()
    def ReadFromFile(self, filename):
        try:
            f = open("" + filename, "r")
        except:
            print("Salah memasukkan nama file")
            return

        #3
        #A 1,2
        #B 1,3
        #C 1,4
        #A,0,1,0
        #B,1,0,1
        #C,0,1,0
        i = 0
        lines = f.readlines()
        # Get n node
        self.nNode = int(lines[0].replace("\n", ""))
        # Get position
        for i in range (self.nNode):
            line = lines[i+1].replace("\n", "").split("|")
            # ["A", "2,3"]
            # versi 1
            node = Node(line[0])
            node.x = line[1].split(",")[0]
            node.y = line[1].split(",")[1]
            self.ListOfNode.append(node)
            # versi 2
            x = line[1].split(",")[0]
            y = line[1].split(",")[1]
            self.ListOFNodePosition.append((float(x), float(y)))
        # Get tetangga
        for i in range (self.nNode):
            line = lines[self.nNode+1+i].replace("\n", "").split(",")
            # Get Node
            node = self.ListOfNode[i]
            j = 0
            for adj in line[1:]:
                if adj == "1":
                    node.AddNeighbour(self.ListOfNode[j])
                j+=1
            self.ListOfNode[i] = node

    def PrintGraph(self):
        for node in self.ListOfNode:
            print(node.name, end =" ")
            for neighbour in node.neighbours:
                print(neighbour.name, end=" ")
            print("")

    def distance(self, node1, node2):
        if node1 == None or node2 == None:
            return 0
        return math.sqrt(pow((float)(node1.x)-(float)(node2.x),2) + pow((float)(node1.y)-(float)(node2.y),2))

    def HaversineDistance(self, node1, node2):
        R = 6378137
        dlat = self.rad((float)(node1.x) - (float)(node2.x))
        dlong = self.rad((float)(node1.y) - (float)(node2.y))
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(self.rad(node1.x))*math.cos(self.rad(node2.x))*math.sin(dlong/2)*math.sin(dlong/2)
        c = math.asin(math.sqrt(a))
        d = R *c
        return d
    
    def rad(self, x):
        return (float)(x)*math.pi/180

    def bobot(self, node_name1, node_name2):
        node1 = self.ListOfNode[self.GetNodeIdx(node_name1)]
        node2 = self.ListOfNode[self.GetNodeIdx(node_name2)]
        if node1.name in node2.neighbours:
            return self.distance(node1, node2)
        return 0
    
    def IsNodeInSet(self, node, list_node):
        for nodes in list_node:
            if node == nodes:
                return True
        return False

    def GetNodeIdx(self, node_name):
        i = 0
        for node in self.ListOfNode:
            if node.name == node_name:
                return i
            i+=1
            
    def GetListOfNode(self):
        return self.ListOfNode

    def getLowestF(self, openSet, fScore):
        lowest = float("inf")
        lowestNode = None
        for node in openSet:
            if fScore[node] < lowest:
                lowest = fScore[node]
                lowestNode = node
        return lowestNode
    
    def reconstructPath(self, cameFrom, goal):
        path = deque()
        node = goal
        path.appendleft(node)
        while node in cameFrom:
            node = cameFrom[node]
            path.appendleft(node)
        return path

def aStar(graph, start, goal):
    #Inisialisasi open list dan closed list
    cameFrom = {}
    openSet = set([start])
    closedSet = set()
    gScore = {} #untuk simpan nilai g
    fScore = {} #untuk simpan nilai f
    gScore[start] = 0 #set g score start node dengan 0
    fScore[start] = gScore[start]+graph.HaversineDistance(start,goal) #set f score start node 

    #iterasi selama openset tidak 0
    while (len(openSet) != 0):
        #set current node dengan node yang punya lowest f
        current = graph.getLowestF(openSet, fScore)
        #jika current node sama dengan yang dicari
        if current == goal:
            return graph.reconstructPath(cameFrom, goal)
        #remove current node dari openSet
        openSet.remove(current)
        #tambahkan current node ke closedSet
        closedSet.add(current)
        #lakukan pencarian nilai f ke semua tetangga dari current node
        if (len(goal.neighbours)!=0):
            for neighbour in current.neighbours:
                tentative_gScore = gScore[current] + graph.HaversineDistance(current, neighbour)
                if neighbour in closedSet and tentative_gScore >= gScore[neighbour]:
                    continue
                if neighbour not in closedSet or tentative_gScore < gScore[neighbour]:
                    cameFrom[neighbour] = current
                    gScore[neighbour] = tentative_gScore
                    fScore[neighbour] = gScore[neighbour] + graph.HaversineDistance(neighbour,goal)
                    if neighbour not in openSet:
                        openSet.add(neighbour)
            print(current.name) #outputnya sampai node sebelum goal
        else :
            print("Tidak bisa akses kesana")
        
    
    return 0

g = Graph()
filename = "test.txt"
g.ReadFromFile(filename)
g.PrintGraph()
aStar(g, g.GetNode(0), g.GetNode(3))