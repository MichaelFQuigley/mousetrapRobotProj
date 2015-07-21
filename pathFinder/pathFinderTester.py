#Author: Michael Quigley
#NOTE: tkinter requires Python 3
import sys
#from PyQt4 import QtGui
from Tkinter import *
from pathFinderDijkstra import *
import time

import path

class PathFinderUI:

    def __init__(self, rows_num, cols_num):
        self.tk       = Tk()
        self.rows_num = rows_num
        self.cols_num = cols_num
        self.tiles    = [[None for _ in range(cols_num)] for _ in range(rows_num)]
        self.fWidth   = 500
        self.fHeight  = 500
        self.canvas   = Canvas(self.tk, width=self.fWidth, height=self.fHeight, borderwidth=5, background='white')
        self.sbmtBtn  = Button(self.tk, text="Submit", command=self.submit)
        self.rstBtn  = Button(self.tk, text="Reset", command=self.reset)
        self.tk.wm_title("Path Finder Test UI")
        self.canvas.pack()
        self.sbmtBtn.pack()
        self.rstBtn.pack()
        self.canvas.bind('<Button-1>', self.clickCallback)
        self.canvas.bind('<B1-Motion>', self.clickCallback)
        self.lastPath = []
     
    def resetPath(self):
        if len(self.lastPath) > 0:
            col_width  = self.canvas.winfo_width()/self.cols_num
            row_height = self.canvas.winfo_height()/self.rows_num
            for cell in path:
                row_ind = cell[1]
                col_ind = cell[0]
                self.tiles[row_ind][col_ind] = self.canvas.create_rectangle(col_ind*col_width, row_ind*row_height, (col_ind + 1)*col_width, (row_ind + 1)*row_height, fill="red")
        self.lastPath = []
        
    def drawPath(self, path):
        self.lastPath = path
        col_width  = self.canvas.winfo_width()/self.cols_num
        row_height = self.canvas.winfo_height()/self.rows_num
        for cell in path:
            row_ind = cell[1]
            col_ind = cell[0]
            self.tiles[row_ind][col_ind] = self.canvas.create_rectangle(col_ind*col_width, row_ind*row_height, (col_ind + 1)*col_width, (row_ind + 1)*row_height, fill="red")
      
    def reset(self):
        for row_ind in range(self.rows_num):
            for col_ind in range(self.cols_num):
                if self.tiles[row_ind][col_ind]:
                    self.canvas.delete(self.tiles[row_ind][col_ind])
                    self.tiles[row_ind][col_ind] = None

      
    def submit(self):
        pathFinder = PathFinderDijkstra(self.getGrid())
        startTime = time.time()
        shortestPathLen, shortestPath = pathFinder.getShortestPathIterative((0,0), (self.cols_num - 1, self.rows_num - 1))
        endTime = time.time()
        print("Time elapsed: " + str(endTime - startTime))
        self.drawPath(shortestPath)
        #self.gridPrettyPrint()
       # pathFinder.prettyPrintNodesTraversed()
        
    #tile layout taken from http://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
    def clickCallback(self, event):
        col_width  = self.canvas.winfo_width()/self.cols_num
        row_height = self.canvas.winfo_height()/self.rows_num
        col_ind = int(event.x // col_width)
        row_ind = int(event.y // row_height)

        if not self.tiles[row_ind][col_ind]:
            self.tiles[row_ind][col_ind] = self.canvas.create_rectangle(col_ind*col_width, row_ind*row_height, (col_ind + 1)*col_width, (row_ind + 1)*row_height, fill="black")
        else:
            self.canvas.delete(self.tiles[row_ind][col_ind])
            self.tiles[row_ind][col_ind] = None

    def getGrid(self):
        return [[(self.tiles[j][i] != None) for i in range(self.cols_num)] for j in range(self.rows_num)]
     
    def gridPrettyPrint(self):
        print("Grid:")
        for i in range(self.rows_num):
            for j in range(self.cols_num):
                print(self.tiles[i][j])



pt = PathFinderUI(50, 50)
pt.tk.mainloop()
