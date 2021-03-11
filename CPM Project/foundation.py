import sys

welcomeMessage = """Welcome to the Critical Path Program! This program will help you solve all
of your project management needs. To get started, please follow the instructions below.""" + '\n'

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

    def setObjective(self):
        self.end = self.activities[len(self.activities)-1]

    def getNode(self, name):
        for i in self.activities:
            if i.name == name:
                return i

    #DFS
    def cycleDetection(self):
        Stack = []
        explored = []
        Stack.append(self.activities[0])
        while Stack:
            currNode = Stack.pop()
            if currNode in explored:
                return True
            explored.append(currNode)
            print(currNode.name)
            if currNode.neighbors:
                for key in currNode.neighbors:
                    Stack.append(key)
        return False


    def printGraphSym(self):
        for i in self.activities:
            newStr = str(i.name) + '-> '
            for j in i.neighbors:
                newStr += j.name + ', '
            newStr = newStr[:-2]
            print(newStr)



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
            self.slack = None
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


    def calculateSlack(self):
        Q = []
        Q.append(self.start)
        while Q:
            currNode = Q.pop(0)
            currNode.slack = currNode.lateFinish - currNode.earlyFinish
            for i in currNode.neighbors:
                Q.append(i)


def quit():
    sys.exit(0)


def main():
    print(welcomeMessage)

    numActivities = int(input("To get started, please indicate how many projects will be needed in the workflow: "))
    act1Name = input("Great, let's begin! What is the name of your first activity? ")
    act1Name = act1Name.capitalize()
    act1Duration = int(input("What is the duration of the first activity?: "))
    startAct = Graph.Node(act1Name, act1Duration)
    graph = Graph(startAct)
    print("Initializing activities . . .")
    for i in range(numActivities-1):
        currName = input("Please indicate the name of the next activity? ")
        currName = currName.capitalize()
        currDur = int(input("What is the duration of this activity? "))
        node = Graph.Node(currName, currDur)
        graph.addActivity(node)
    graph.setObjective()
    print("Activities set successfully!")
    print("The activities have been set! To complete the workflow construction, please follow the steps below.")
    print("Creating workflow . . .")
    for i in range(len(graph.activities)-1):
        currNode = graph.activities[i]
        neighbors = input("For activity: " + currNode.name + ", what activities immediately proceed it? ")
        neighbors = neighbors.split(',')

        for j in neighbors:
            j = j.capitalize()
            currNode.addEdge(graph.getNode(j))

    if graph.cycleDetection():
        print('\n')
        print("Error: Workflow has a cycle! Cannot perform Critical Path Analysis.")
        sys.exit(0)

    print("Workflow completed successfully! Please verify if the following workflow looks correct: " + '\n')
    graph.printGraphSym()
    verify = input("Does this look correct?" + '\n' + "Please enter 'y' for 'yes' or 'n' for 'no'")
    if verify == 'n':
        print("Error: Workflow is not consistent. Please try again!")
        sys.exit(0)





main()









