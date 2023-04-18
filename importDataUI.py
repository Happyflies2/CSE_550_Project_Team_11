# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:19:15 2023

@author: Asim
"""

import tkinter as tk
import dataloader as dl

class dataLoaderUI:
    def __init__(self, width=800, height=400):
        #width and height of window
        self.width = width
        self.height = height
        self.dataLoader = dl.DataLoader()
        #creation of the window
        self.createWindow()
    
    #Function: Create a window to the specified dimensions
    def createWindow(self):
        self.window = tk.Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        #Setup initial window
        self.startWindow()
    
    #Function: Allows importing of files
    def startWindow(self):
        self.clearWindow()
        #message appears in window
        message = tk.Label(text="Select the folder which contains both summary.csv and metadata.csv")
        message.pack()
        
        #button when clicked, will open a file dialog
        button = tk.Button(text="Import Data", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.openFilePath)
        button.pack()
        
    #Function: file dialog
    def openFilePath(self):
        self.folderPath = tk.filedialog.askdirectory()
        self.dataLoader.ImportData(self.folderPath)
        message = tk.Label(text="Data loaded from path:\n" + self.folderPath)
        message.pack()
        
        #Button to view data once imported
        button = tk.Button(text="View Data", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.viewData)
        button.pack()
    
    #Function: clear all widgets
    def clearWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()
            
    #Function: testing function to see if dataframe successfully imported and viewable
    def viewData(self):
        self.clearWindow()
        for data in self.dataLoader.dataList:
            dataFrame = data.data
            message = tk.Label(text=dataFrame)
            message.pack()
        #button to go back
        button = tk.Button(text="Back", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.startWindow)
        button.pack()