# CRITICAL PATH CALCULATOR #
# Nikhill Joshi
# Last updated: 5/9/2021

# Description: The Critical Path of a project is defined as the sequence of events
# that will yield the shortest duration of completion. In large-scale projects with multiple
# activities/inter-dependencies, it can be overwhelming to determine which activities are
# deemed 'high priority' and which activities can be delayed with little consequence. With
# this program, a user is able to initialize a project workflow and the Critical Path is
# returned, giving them a starting point on the steps needed to successfully complete their
# project. I create Graph/Node classes to represent the workflow/activities, and created
# algorithms for conducting the 'first pass' and 'second pass' which are needed to finally
# calculate the Critical Path.


import time
import numpy as np
import matplotlib.pyplot as plt     #will be used when visualizations are supported

welcomeMessage = """Welcome to the Critical Path Program! This program will help you solve all
of your project management needs. To get started, please follow the instructions below.""" + '\n'


# Graph class containing 'Node' subclass
class Graph:
    #constructor
    #@param: start node (first activity in workflow)
    #@return: none
    def __init__(self, start):
        self.start = start
        self.end = None
        self.size = 0
        self.activities = [self.start]



    #adds activity to graph
    #@param: node to add to workflow
    #@return: none
    def addActivity(self, node):
        self.activities.append(node)
        self.size = len(self.activities)



    #adds objective to graph (end result)
    #@param: node to add to workflow that serves as final objective
    #@return: none
    def addObjective(self, node):
        self.addActivity(node)
        self.end = self.activities[len(self.activities)-1]



    #sets objective to specified node
    #@param: none
    #@return: none
    def setObjective(self):
        self.end = self.activities[len(self.activities)-1]



    #getter method to return specified node
    #@param: name of node to be returned
    #@return: specified node
    def getNode(self, name):
        for i in self.activities:
            if i.name == name:
                return i

    #-TODO-
    #Implement algorithm to detect if cycles present among activities in workflow
    #Current implemtation is similar to DFS, but broken
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


    #Prints the graph/node adjacency list relationships
    #@param: none
    #@return: none; prints graph
    def printGraphSym(self):
        for i in range(len(self.activities)-1):
            currNode = self.activities[i]
            newStr = str(currNode.name) + '-> '
            for j in currNode.neighbors:
                newStr += j.name + ', '
            newStr = newStr[:-2]
            print(newStr)



    #Prints the graph/node adjacency list relationships
    #@param: none
    #@return: no return; prints graph
    def printGraph(self):
        for i in self.activities:
            arr = [i.name]
            for j in i.neighbors:
                arr.append(j.name)
            print(arr)




    #Returns list of nodes that point to specified node
    #@param: specified node
    #@return: list containing nodes that point to param
    def getIncomingEdges(self, node):
        arr = []
        for i in self.activities:
            if node in i.neighbors:
                arr.append(i)
        return arr



    #Reverses the graph; useful for conducting backwards-pass functionality when
    #calculating Critical Path
    #@param: none
    #@return: none
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




    #Node subclass
    class Node:

        #constructor
        #param: name of node, duration of activity
        #@return: none
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

        #adds an edge to an existing node
        #@param: node to create edge between
        #@return: none
        def addEdge(self, node):
            self.neighbors[node] = 1
            self.numActivities = len(self.neighbors)


    #FIRST PASS (STEP 1)
    #conducts the first pass of our workflow. Does a single pass in the forward direction
    #and calculates earlyFinish/earlyStart for all activities in the workplace. Metrics
    #are used for calculating Critical Path.
    #@param: none
    #@return: none
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



    # SECOND PASS (STEP 2)
    # conducts the second pass of our workflow. Does a single pass in the backward direction
    # and calculates lateFinish/lateStart for all activities in the workplace. Metrics
    # are used for calculating Critical Path.
    # @param: none
    # @return: none
    def secondPass(self):
        self.reverseGraph()
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


    #Caclulates the slack for each activity in the worlflow. The 'slack' of an activity
    #is defined as the duration of time that can pass from the proposed start such that
    #the activity will still finish on time. Large slack means the activity can start later
    #than expected, low slack means that delaying the activity will delay entire objective
    #@param: none
    #@return: none
    def calculateSlack(self):
        Q = []
        Q.append(self.start)
        while Q:
            currNode = Q.pop(0)
            currNode.slack = currNode.lateStart - currNode.earlyStart
            for i in currNode.neighbors:
                Q.append(i)


    #Finds Critical Path of workflow based on the First/Second passes. Utilizes algorithm
    #similar to BFS to traverse graph and create the sequence of activities representing
    #the Critical Path
    #@param: none
    #@return: the Critical Path
    def findCriticalPath(self):
        Q = []
        critPath = []
        Q.append(self.start)
        while Q:
            currNode = Q.pop(0)
            if not currNode.slack:
                if currNode not in critPath:
                    critPath.append(currNode)
            for i in currNode.neighbors:
                Q.append(i)
        newStr = ''
        for i in range(len(critPath)):
            currData = critPath[i]
            newStr += currData.name + ' -> '
        newStr = newStr[:-4]
        return newStr


def initializeGraph(graph):
    for i in range(len(graph.activities)-1):
        currNode = graph.activities[i]
        neighbors = input("For activity: " + currNode.name + ", what activities immediately proceed it? ")
        neighbors = neighbors.split(',')

        for j in neighbors:
            j = j.capitalize()
            currNode.addEdge(graph.getNode(j))


def clear(graph):
    for i in range(len(graph.activities)-1):
        currNode = graph.activities[i]
        currNode.neighbors.clear()

def initializeFirstActivity():
    numActivities = int(input("To get started, please indicate how many projects will be needed in the workflow: "))
    act1Name = input("Great, let's begin! What is the name of your first activity? ")
    act1Name = act1Name.capitalize()
    act1Duration = int(input("What is the duration of the first activity?: "))
    startAct = Graph.Node(act1Name, act1Duration)
    graph = Graph(startAct)
    return [numActivities, graph]

# - TODO -
# add more edge cases to increase UX as well as improve robustness for unusual user
# inputs. Also optimize/correct input texts.
def main():
    print(welcomeMessage)
    data = initializeFirstActivity()
    numActivities = data[0]
    graph = data[1]
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

    initializeGraph(graph)

    print("Workflow completed successfully! Please verify if the following workflow looks correct: " + '\n')
    graph.printGraphSym()
    verify = input("Does this look correct?" + '\n' + "Please enter 'y' for 'yes' or 'n' for 'no' ")
    if verify == 'n':
        print("Error: Workflow is not consistent. Please try again!")
        clear(graph)
        initializeGraph(graph)
    print("Great! We will now calculate the Critical Path")
    time.sleep(2)
    print("Calculating Forward Pass . . .")
    graph.firstPass()
    time.sleep(3)
    print("Calculating Backward Pass . . .")
    graph.secondPass()
    time.sleep(3)
    print("Calculating Float . . .")
    graph.calculateSlack()
    time.sleep(2)
    print("Done! Below is the Critical Path for your project." + '\n')
    print(graph.findCriticalPath())


main()









