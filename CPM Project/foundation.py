class Graph:

    def __init__(self, start):
        self.start = start
        self.end = None
        self.size = 0
        self.activities = [self.start]

    def addActivity(self, node):
        self.activities.append(node)
        self.size = len(self.activities)

    def addObjective(self, node):
        self.addActivity(node)
        self.end = self.activities[len(self.activities)-1]

    def printGraph(self):
        for i in self.activities:
            arr = [i.name]
            for j in i.neighbors:
                arr.append(j.name)
            print(arr)

    def getIncomingEdges(self, node):
        arr = []
        for i in self.activities:
            if node in i.neighbors:
                arr.append(i)
        return arr

    def reverseGraph(self):
        Q = []
        explored = []
        Q.append(self.end)
        incomingHash = {}
        for i in self.activities:
            incomingHash[i] = self.getIncomingEdges(i)


        while Q:
            currNode = Q.pop(0)
            explored.append(currNode)
            currNode.neighbors.clear()

            for i in incomingHash[currNode]:
                currNode.neighbors[i] = 1
                if i not in explored:
                    Q.append(i)

        oldStart = self.start
        self.start = self.end
        self.end = oldStart

    class Node:

        def __init__(self, name, duration):
            self.name = name
            self.duration = duration
            self.earlyStart = None
            self.earlyFinish = None
            self.lateStart = None
            self.lateFinish = None
            self.float = None
            self.neighbors = {}
            self.numActivities = 0

        def addEdge(self, node):
            self.neighbors[node] = 1
            self.numActivities = len(self.neighbors)

    def firstPass(self):
        Q = []
        Q.append(self.start)
        self.start.earlyStart = 0
        self.start.earlyFinish = self.start.earlyStart + self.start.duration

        while Q:
            currNode = Q.pop(0)
            for i in currNode.neighbors:
                if i.earlyStart:
                    i.earlyStart = max(i.earlyStart, currNode.earlyFinish)
                else:
                    i.earlyStart = currNode.earlyFinish
                i.earlyFinish = i.earlyStart + i.duration
                Q.append(i)

    def secondPass(self):
        self.reverseGraph()
        self.printGraph()

        Q = []
        Q.append(self.start)
        self.start.lateFinish = self.start.earlyFinish
        self.start.lateStart = self.start.lateFinish - self.start.duration

        while Q:
            currNode = Q.pop(0)
            for i in currNode.neighbors:
                if i.lateFinish:
                    i.lateFinish = min(i.lateFinish, currNode.lateStart)
                else:
                    i.lateFinish = currNode.lateStart
                i.lateStart = i.lateFinish - i.duration
                Q.append(i)

        self.reverseGraph()





A = Graph.Node("A", 3)
H = Graph.Node("H", 3)
graph = Graph(A)
graph.addObjective(H)

B = Graph.Node("B", 4)
C = Graph.Node("C", 2)
D = Graph.Node("D", 5)
E = Graph.Node("E", 1)
F = Graph.Node("F", 2)
G = Graph.Node("G", 4)

A.addEdge(B)
A.addEdge(C)
B.addEdge(D)
C.addEdge(E)
C.addEdge(F)
E.addEdge(G)
D.addEdge(G)
G.addEdge(graph.end)
F.addEdge(graph.end)

graph.addActivity(B)
graph.addActivity(C)
graph.addActivity(D)
graph.addActivity(E)
graph.addActivity(F)
graph.addActivity(G)

graph.firstPass()
#for i in graph.activities:

 #   arr = [i.name, i.earlyStart, i.duration, i.earlyFinish]
  #  print(arr)

graph.secondPass()
for i in graph.activities:
    arr = [i.name, i.earlyStart, i.earlyFinish, i.lateStart, i.duration, i.lateFinish]
    print(arr)








