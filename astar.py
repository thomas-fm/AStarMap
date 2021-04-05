import math
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


def aStar(graph, start, goal):
    #Inisialisasi open list dan closed list
    open_list = []
    closed_list = []

    #Tambahkan start node ke open list
    open_list.append(start)
    #Set nilai g(n) awal
    start.SetG(0)
    #Set nilai f(n) = h(n) = distance start ke goal
    start.SetF(graph.HaversineDistance(start, goal))

    #Jika tidak empty
    while (len(open_list)>0):
        current = open_list[0]

        #Cari nilai f yang terkecil
        for node in open_list:
            if node.f < current.f :
                current = node
        
        #Jika sudah start node = goal node
        if current == goal :
            current = goal
            while (current.GetParent()):
                current = current.GetParent()
            return True

        open_list.remove(current)
        closed_list.append(current)
        
        #Lakukan pengecekan terhadap tetangga dari current node
        result = []
        if len(goal.neighbours) != 0:
            for neighbour in current.neighbours:
                if neighbour in closed_list:
                    continue

                temp = current.g + graph.HaversineDistance(current, neighbour)
                if neighbour not in open_list:
                    open_list.append(neighbour)
                elif temp >= neighbour.g:
                    continue
                
                neighbour.SetParent(current)
                neighbour.SetG(temp)
                neighbour.SetF(temp+graph.HaversineDistance(neighbour, goal))

            result.append(current.name) #ini outputnya sampe node sebelum goal
            #atau
            #result.append(neighbour.name) #ini sampe goal cuma kurang yakin jadi masih labil antara yg atas atau yg ini
            print(result[0])
        else:
            print("Tidak bisa akses kesana")

g = Graph()
filename = "test.txt"
g.ReadFromFile(filename)
g.PrintGraph()
aStar(g, g.GetNode(0), g.GetNode(3))