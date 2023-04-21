# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:19:15 2023

@author: Asim
"""

import tkinter as tk
import dataloader as dl
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class Window:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        #creation of the window
        self.createWindow()
    
    #Function: Create a window to the specified dimensions
    def createWindow(self):
        self.window = tk.Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.startWindow()
        
        self.window.mainloop
    
    #Function: clear all widgets
    def clearWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    

class dataLoaderUI(Window):
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.dataLoader = dl.DataLoader()
        #creation of the window
        self.createWindow()
        self.startWindow()

    
    #Function: Allows importing of files
    def startWindow(self):
        self.clearWindow()
        #message appears in window
        message = tk.Label(self.window, text="Select the folder which contains both summary.csv and metadata.csv")
        message.place(x=50, y=50)
        
        #button when clicked, will open a file dialog
        button = tk.Button(self.window, text="Import Data", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.openFilePath)
        button.place(x=50, y=100)
        
    #Function: file dialog
    def openFilePath(self):
        self.clearWindow()
        self.folderPath = tk.filedialog.askdirectory()
        self.dataLoader.ImportData(self.folderPath)
        message = tk.Label(self.window, text="Data loaded from path:\n" + self.folderPath)
        message.place(x=50, y=50)
        
        #Button to view data once imported
        button = tk.Button(self.window, text="View Data", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.viewData)
        button.place(x=50, y=100)
    
    #Function: testing function to see if dataframe successfully imported and viewable
    def viewData(self):
        self.clearWindow()
        for data in self.dataLoader.dataList:
            dataFrame = data.summary
            message = tk.Label(self.window, text=dataFrame)
            message.place(x=50, y=100)
        #button to go back
        button = tk.Button(self.window, text="Back", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.startWindow)
        button.place(x=50, y=100)
        
        nextButton = tk.Button(self.window, text="Next", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.gotoGraphPanel)
        nextButton.place(x=50, y=300)
        
    def gotoGraphPanel(self):
        self.graphPanel = GraphPanel(self.dataLoader.dataList, self.window)
        
class GraphPanel(Window):
    def __init__(self, dataList, win):
        self.data = dataList
        #if we pass a tkinter window, then don't create new window
        if (win):
            self.window = win
        else:
            self.createWindow()
            
        self.setUpWindow()
    
    def setUpWindow(self):
        self.clearWindow()
        self.plot()
    
    #Function: plots all of the data
    def plot(self):
        data = self.data[0].summary
        columns = data.columns[3:-1]
        
        fig = Figure(figsize = (5, 5), dpi = 100)
        numOfPlots = len(columns)
        
        for i,col in enumerate(columns):
            current_plot = fig.add_subplot(numOfPlots, 1, i+1)
            current_plot.plot(data[col])

        canvas = FigureCanvasTkAgg(fig, master = self.window)  
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()

        