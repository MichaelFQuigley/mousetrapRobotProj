#pathFinder.py
#Author: Michael Quigley

#assumes that the origin is at the top left        
from copy import copy, deepcopy

class PathFinder:
    def __init__(self, grid):
        #grid is 2D array of Booleans
        #a value of False in a cell indicates that the cell can be traveled to
        #a value of True in a cell indicates that the cell is blocked and cannot be traveled to
        self.grid           = grid
        #-1 indicates the node cant be traversed
        self.nodesTraversed = [[-1.0 if grid[j][i] == True else float("inf")
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
        
        

    def prettyPrintNodesTraversed(self):
        [print(self.nodesTraversed[j])
            for j in range(len(self.nodesTraversed))]
        
        
        
    #currPos  = (xCoord, yCoord)
    #endPos   = (xCoord, yCoord)
    def getShortestPath(self, currPos, endPos, currPathLen = 0, minPathLen =  float("inf")):
        if currPos == endPos:
            return (currPathLen, [endPos])
        currMin = float("inf")
        currPathPart = []
        for neighbor in self.getNeighbors(currPos):
            nodeMinPathLen = self.nodesTraversed[neighbor[1]][neighbor[0]]
            if currPathLen < nodeMinPathLen:
                self.nodesTraversed[neighbor[1]][neighbor[0]] = currPathLen
            else:
                continue
                
            tempMin, pathPart = self.getShortestPath(neighbor, endPos, currPathLen + 1)
            if tempMin < currMin:
                currMin = tempMin
                currPathPart = pathPart
        currPathPart.append(currPos)
        return (currMin, currPathPart)
        

        
 