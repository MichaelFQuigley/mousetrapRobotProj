#pathFinderDijkstra.py
#Author: Michael Quigley

#assumes that the origin is at the top left        
from copy import copy, deepcopy
from math import sqrt
from collections import deque

class NodeQueue:
    def __init__(self):
        self.nodesList = deque()
        self.nodesSet  = set()
    
    def printStack(self):
        print(self.nodesList)
    
    def empty(self):
        return len(self.nodesList) == 0
    
    def peek(self):
        if len(self.nodesList) > 0:
            return self.nodesList[len(self.nodesList) - 1]
        else:
            return []
            
    def enqueue(self,element):
        self.nodesSet.add(element)
        self.nodesList.append(element)
        
    def dequeue(self):
        result = self.nodesList.popleft()
        self.nodesSet.remove(result)
        return result
    

class PathFinderDijkstra:
    def __init__(self, grid):
        #grid is 2D array of Booleans
        #a value of False in a cell indicates that the cell can be traveled to
        #a value of True in a cell indicates that the cell is blocked and cannot be traveled to
        self.grid           = grid
        #-1 indicates the node cant be traversed
        self.nodesTraversed = [[-1.0 if grid[j][i] == 1 else float("inf")
                                    for i in range(len(grid[j]))] 
                                        for j in range(len(grid))]
    
    
    
    def getNeighbors(self, currPos):
        adjNodeList = []
        x = currPos[0]
        y = currPos[1]
        top    = y + 1
        bottom = y - 1
        left   = x - 1
        right  = x + 1
        #bound checks
        topCheck    = top < len(self.grid)
        bottomCheck = bottom >= 0
        leftCheck   = left >= 0
        rightCheck  = right < len(self.grid[0])

        if rightCheck:
            adjNodeList.append( (right, y) )
            if bottomCheck:
                adjNodeList.append( (right, bottom) )       
            if topCheck:
                adjNodeList.append( (right, top) )
        if leftCheck:
            adjNodeList.append( (left, y) )   
            if bottomCheck:
                adjNodeList.append( (left, bottom) )       
            if topCheck:
                adjNodeList.append( (left, top) )            
        if topCheck:
            adjNodeList.append( (x, top) )
        if bottomCheck:
            adjNodeList.append( (x, bottom) )
        
        return adjNodeList
        
        

    def getWeight(self, currPos, neighborPos):
        if currPos[0] != neighborPos[0] and currPos[1] != neighborPos[1]:
            return 1.414 #sqrt(2)
        return 1
        

    def prettyPrintNodesTraversed(self):
        for j in range(len(self.nodesTraversed)):
            print(self.nodesTraversed[j])

        
        
        
    #currPos  = (xCoord, yCoord)
    #endPos   = (xCoord, yCoord)
    def getShortestPath(self, currPos, endPos, currPathLen = 0, minPathLen =  float("inf")):
        if currPos == endPos:
            return (currPathLen, [endPos])
        currMin = float("inf")
        currPathPart = []
        for neighbor in self.getNeighbors(currPos):
            nodeMinPathLen = self.getDist(neighbor)
            if currPathLen < nodeMinPathLen:
                self.setDist(neighbor, currPathLen)
            else:
                continue
                
            tempMin, pathPart = self.getShortestPath(neighbor, endPos, currPathLen + self.getWeight(currPos, neighbor))
            if tempMin < currMin:
                currMin = tempMin
                currPathPart = pathPart
        currPathPart.append(currPos)
        return (currMin, currPathPart)
        
    def getDist(self, node):
        return self.nodesTraversed[node[1]][node[0]]
        
    def setDist(self, node, value):
        self.nodesTraversed[node[1]][node[0]] = value
        
    def weightGraphIterative(self, startPos, endPos):
        nodeQueue    = NodeQueue()
        self.setDist(startPos, 0)
        nodeQueue.enqueue(startPos)
        currPos = startPos
        while not nodeQueue.empty() and currPos != endPos:
            currPos = nodeQueue.dequeue()
            for neighbor in self.getNeighbors(currPos):
                if neighbor not in nodeQueue.nodesSet and self.getDist(neighbor) != -1:
                    nodeQueue.enqueue(neighbor)
                weight = self.getWeight(currPos, neighbor) + self.getDist(currPos)
                if weight < self.getDist(neighbor) and self.getDist(neighbor) != -1:
                    self.setDist(neighbor, weight)
            
       
    def getShortestPathIterative(self, startPos, endPos):
        self.weightGraphIterative(startPos, endPos)
        traveled = [endPos]
        currPath = [endPos]
        
        currPos = endPos
        while currPos != startPos:
            currMin      = float('inf')
            bestNeighbor = None
            for neighbor in self.getNeighbors(currPos):
                if neighbor in traveled:
                    continue
                traveled.append(neighbor)
                if self.getDist(neighbor) < currMin and self.getDist(neighbor) != -1:
                    currMin = self.getDist(neighbor)
                    bestNeighbor = neighbor
            if bestNeighbor != None:
                currPos = bestNeighbor
                currPath.append(bestNeighbor)
        print(currPath)
        return self.getDist(endPos), currPath
        

        
 
