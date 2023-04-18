# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:19:15 2023

@author: Asim
"""

import tkinter as tk
import dataloader as dl

class dataLoaderUI:
    def __init__(self, width=800, height=400):
        self.width = width
        self.height = height
        self.dataLoader = dl.DataLoader()
        self.createWindow()
    
    def createWindow(self):
        self.window = tk.Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.startWindow()
        
    def startWindow(self):
        message = tk.Label(text="Select the folder which contains both summary.csv and metadata.csv")
        message.pack()
        
        button = tk.Button(text="Import Data", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.openFilePath)
        button.pack()
        

    def openFilePath(self):
        self.folderPath = tk.filedialog.askdirectory()
        self.dataLoader.ImportData(self.folderPath)
        message = tk.Label(text="Data loaded from path:\n" + self.folderPath)
        message.pack()
        
        button = tk.Button(text="View Data", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.viewData)
        button.pack()
        
    def clearWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()
            
    def viewData(self):
        self.clearWindow()
        for data in self.dataLoader.dataList:
            dataFrame = data.data
            message = tk.Label(text=dataFrame)
            message.pack()
        
        button = tk.Button(text="Back", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.startWindow)
        
        
        
win = dataLoaderUI()