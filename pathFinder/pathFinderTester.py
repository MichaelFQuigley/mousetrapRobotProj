#Author: Michael Quigley
#NOTE: tkinter requires Python 3
import sys
#from PyQt4 import QtGui
from Tkinter import *
from pathFinderDijkstra import *
import time

from path_bfs import PathFinderBFS
from path_as import PathFinderAStar

class PathFinderUI:

    def __init__(self, rows_num, cols_num):
        self.tk       = Tk()
        self.rows_num = rows_num
        self.cols_num = cols_num
        self.tiles    = [[None for _ in range(cols_num)] for _ in range(rows_num)]          # Obstacle tiles
        self.path_tiles    = [[None for _ in range(cols_num)] for _ in range(rows_num)]     # Path tiles
        self.fWidth   = 800
        self.fHeight  = 800
        self.canvas   = Canvas(self.tk, width=self.fWidth, height=self.fHeight, borderwidth=5, background='white')
        self.sbmtBtn  = Button(self.tk, text="Submit", command=self.submit)
        self.rstBtn  = Button(self.tk, text="Reset", command=self.reset_path)
        self.tk.wm_title("Path Finder Test UI")
        self.canvas.pack()
        self.sbmtBtn.pack()
        self.rstBtn.pack()
        self.canvas.bind('<Button-1>', self.clickCallback)
        self.canvas.bind('<B1-Motion>', self.clickCallback)
        self.lastPath = []

    def get_col_width(self):
        return self.canvas.winfo_width() / self.cols_num

    def get_row_height(self):
        return self.canvas.winfo_height() / self.rows_num

    def create_rectangle(self, row, col, color):
        x1 = col * self.get_col_width()
        y1 = row * self.get_row_height()
        x2 = x1 + self.get_col_width()
        y2 = y1 + self.get_row_height()
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        
    def set_obstacle(self, row, col, obstacle=True):
        if obstacle:
            self.tiles[row][col] = self.create_rectangle(row, col, "black")
        else:
            self.canvas.delete(self.tiles[row][col])
            self.tiles[row][col] = None 

    def draw_path(self, path):
        self.lastPath = path
        col_width  = self.canvas.winfo_width()/self.cols_num
        row_height = self.canvas.winfo_height()/self.rows_num
        for cell in path:
            row_ind = cell[0]
            col_ind = cell[1]
            if not self.path_tiles[row_ind][col_ind]:
                self.path_tiles[row_ind][col_ind] = self.create_rectangle(row_ind, col_ind, "red")

    def reset_path(self):
        for row_ind in range(self.rows_num):
            for col_ind in range(self.cols_num):
                if self.path_tiles[row_ind][col_ind]:
                    self.canvas.delete(self.path_tiles[row_ind][col_ind])
                    self.path_tiles[row_ind][col_ind] = None

      
    def submit(self):
        # Init grid, origin, and destination
        grid = self.getGrid()
        origin = (0,0)
        dest = (self.cols_num - 1, self.rows_num - 1)

        startTime = time.time()
        #path_finder = PathFinderDijkstra(grid)
        #path_finder = PathFinderBFS(grid)
        path_finder = PathFinderAStar(grid)
        path_length, path = path_finder.get_path(origin, dest)
        endTime = time.time()

        print("Time elapsed: " + str(endTime - startTime))
        print("Path length: " + str(path_length))
        #print("Path: " + str(path))

        self.draw_path(path)

        # Temporary hack to highlight visited nodes
        if path_finder.visited:
            for row in range(self.rows_num):
                for col in range(self.cols_num):
                    if (path_finder.visited[row][col]):
                        if not self.path_tiles[row][col]:
                            self.path_tiles[row][col] = self.create_rectangle(row, col, "yellow")
            
        
        #self.gridPrettyPrint()
        #pathFinder.prettyPrintNodesTraversed()

    #tile layout taken from http://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas
    def clickCallback(self, event):
        col_width  = self.canvas.winfo_width()/self.cols_num
        row_height = self.canvas.winfo_height()/self.rows_num
        col_ind = int(event.x // col_width)
        row_ind = int(event.y // row_height)
        obstacle_present = self.tiles[row_ind][col_ind]
        self.set_obstacle(row_ind, col_ind, not obstacle_present)

    def getGrid(self):
        return [[(self.tiles[j][i] != None) for i in range(self.cols_num)] for j in range(self.rows_num)]
    
    def gridPrettyPrint(self):
        print("Grid:")
        for i in range(self.rows_num):
            for j in range(self.cols_num):
                print(self.tiles[i][j])



pt = PathFinderUI(200, 200)
pt.tk.mainloop()
