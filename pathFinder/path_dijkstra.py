#Author: Michael Quigley

#assumes that the origin is at the top left        
from copy import copy, deepcopy
from math import sqrt
from collections import deque

from path import PathFinder


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
    

class PathFinderDijkstra(PathFinder):

    def __init__(self, grid):
        PathFinder.__init__(self, grid)

	#-1 indicates the node cant be traversed
        self.nodesTraversed = [[-1.0 if grid[row][col] == 1 else float("inf")
                                    for col in range(len(grid[row]))] 
                                        for row in range(len(grid))]
    
    
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
        for neighbor in self.get_neighbors(currPos):
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
        return self.nodesTraversed[node[0]][node[1]]
        
    def setDist(self, node, value):
        self.nodesTraversed[node[0]][node[1]] = value
        
    def weightGraphIterative(self, startPos, endPos):
        nodeQueue    = NodeQueue()
        self.setDist(startPos, 0)
        nodeQueue.enqueue(startPos)
        currPos = startPos
        while not nodeQueue.empty() and currPos != endPos:
            currPos = nodeQueue.dequeue()
            for neighbor in self.get_neighbors(*currPos):
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
            for neighbor in self.get_neighbors(*currPos):
                if neighbor in traveled:
                    continue
                traveled.append(neighbor)
                if self.getDist(neighbor) < currMin and self.getDist(neighbor) != -1:
                    currMin = self.getDist(neighbor)
                    bestNeighbor = neighbor
            if bestNeighbor != None:
                currPos = bestNeighbor
                currPath.append(bestNeighbor)
        #print(currPath)
        return self.getDist(endPos), currPath

    def get_path(self, origin, dest, weights = None):
        path_legth, path = self.getShortestPathIterative(origin, dest)
        path.reverse()
        return path_legth, path

        
 
