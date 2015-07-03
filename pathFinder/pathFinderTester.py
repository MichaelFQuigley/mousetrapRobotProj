#Author: Michael Quigley
#NOTE: tkinter requires Python 3
from tkinter import *

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
        self.tk.wm_title("Path Finder Test UI")
        self.canvas.pack()
        self.sbmtBtn.pack()
        self.canvas.bind('<Button-1>', self.clickCallback)

    def submit(self):
        self.gridPrettyPrint()
        
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
        [print([(0 if self.tiles[j][i] != None else 1) 
        for i in range(self.cols_num)]) 
        for j in range(self.rows_num)]

pt = PathFinderUI(15, 15)
pt.tk.mainloop()