# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:19:15 2023

@author: Asim
"""

import tkinter as tk
import dataloader as dl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates

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

    
    #Function: clear all widgets
    def clearWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    
#Method: Creates initializes dataLoader window
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
        message = tk.Label(self.window, text="Select the folder with the data.")
        message.pack()
        
        #button when clicked, will open a file dialog
        button = tk.Button(self.window, text="Select Folder", width = 25, height = 5, bg = "black", 
                           fg = "white", command=self.openFilePath)

        button.pack()


    #method takes root path and returns two lists:
    #dates: list of all date folders
    #users: list of all users for each date folder
    def findDateAndUserFolders(self, path):    
        from os import listdir
        
        #list of date folders
        dates = listdir(path)
        users = []

        #go through files, and find users
        for folders in dates:
            newpath = path+"/"+folders
            user = listdir(newpath)
            users.append(user)
            
        return dates, users
        
    #method to load data    
    def loadData(self, option):
        self.dataLoader.ImportData(self.folderPath+'/'+ self.date_select_var.get() +'/'+option)
        
        
    #creates drop-down menu for the users
    def select_user(self, sel):
        #if the user_selection exists, destroy it
        #prevents too many option menus from appearing
        if (self.user_selections):
            self.user_selections[0].destroy()
        
        message = tk.Label(self.window, text="Select the user.")
        message.pack()
        #find index of date, will use that index for finding users
        index = self.date_options.index(sel)
        #user variable
        user_select_var = tk.StringVar(self.window)
        #options list
        user_selection = tk.OptionMenu(self.window, user_select_var, *self.user_options[index], command = self.loadData)
        #add options menu to list for easy deletion
        self.user_selections.append(user_selection)
        user_selection.pack()
        

        
    
    #Function: file dialog
    def openFilePath(self):
        self.clearWindow()
        self.folderPath = tk.filedialog.askdirectory()
        
        
        self.date_options, self.user_options = self.findDateAndUserFolders(self.folderPath)
            
        #trick: to use list to delete old selections
        self.user_selections = []


        #variable to hold selected item
        self.date_select_var = tk.StringVar(self.window)
        #drop down widget with dates
        message = tk.Label(self.window, text="Select the date.")
        message.pack()
        
        date_selection = tk.OptionMenu(self.window, self.date_select_var, *self.date_options, command=self.select_user)
        date_selection.pack()

        #Attribute Selection
        self.checkVariables = []
        attributes = ["Acc magnitude avg","Eda avg","Temp avg","Movement intensity","Steps count","Rest","On Wrist"]
        
        
        #selecting the attributes
        message = tk.Label(self.window, text="Select Attributes to Import")
        message.place(x=500, y = 10)
        for index, attr in enumerate(attributes):
            #creating variable to store check data
            self.checkVariables.append(tk.IntVar(self.window))
            #creates check widget
            check = tk.Checkbutton(self.window, text=attr, variable=self.checkVariables[index])
            check.place(x=500, y=50+index*50)
            



        #radio selection for the time conversions
        message = tk.Label(self.window, text="Select a timezone")
        message.pack(anchor=tk.W)
        
        #radio buttons for time zone conversion (DOESN'T WORK RIGHT NOW)
        self.time_zone_var = tk.IntVar(self.window)
        time_select = tk.Radiobutton(self.window, text="Local Time",padx = 20, variable=self.time_zone_var, value=1)
        time_select.pack(anchor=tk.W)
        
        time_select = tk.Radiobutton(self.window, text="UTC",padx = 20, variable=self.time_zone_var, value=2)
        time_select.pack(anchor=tk.W)
        
        
        #Button to view data once imported
        
        button = tk.Button(self.window, text="Import Data", width = 25, height = 5, bg = "black", fg = "white", command=self.gotoGraphPanel)
        button.place(x=50, y=200)


        self.window.mainloop 
        
    #selecting attributes
    def attributeSelection(self, dataFrame):
        #attribute selection
        headers = dataFrame.columns[3:-1]
        selected_attributes = []
        
        #go through the check variables to find the selected attributes
        for index,value in enumerate(self.checkVariables):
            if (value.get() == 1):
                selected_attributes.append(headers[index])
        
        return selected_attributes
        
    
    #go to graph panel UI, transition to graph panel UI
    def gotoGraphPanel(self):
        df = self.dataLoader.data.summary
        self.graphPanel = GraphPanel(self.dataLoader.data,self.attributeSelection(df), self.window)
    

class GraphPanel(Window):
    def __init__(self, data,attributes, win):
        self.data = data
        #if we pass a tkinter window, then don't create new window
        if (win):
            self.window = win
        else:
            self.createWindow()
            
        self.attributes = attributes
        self.setUpWindow()
    
    def setUpWindow(self):
        self.clearWindow()
        self.selectPlotType()
    
    def selectPlotType(self):
        message = tk.Label(self.window, text="Select a Chart Type")
        message.pack()
        
        methods = ["plot", "scatter", "bar", "step", "stem"]
        plot_select_var = tk.StringVar(self.window)
        plot_selection = tk.OptionMenu(self.window, plot_select_var, *methods, command=self.plot)
        plot_selection.pack()
        self.window.mainloop
       
        
    #Function: plots all of the data
    def plot(self, method):
        self.clearWindow()
        
        data = self.data.summary    
        data = data[self.attributes]
        columns = data.columns
        
        
        fig = Figure(figsize = (5, 5), dpi = 100, tight_layout=True)

        numOfPlots = len(columns)
        
        for i,col in enumerate(columns):
            current_plot = fig.add_subplot(numOfPlots, 1, i+1)
            current_plot.set_title(f"{columns[i]}")
            
            #user method parameter to invoke correct method
            chart = "current_plot."+method+"(self.data.datetime, data[col])"
            #create the chart based on selection
            eval(chart)

        
            current_plot.set_xlabel("Date")
            
            
            #Reducing number of ticks
            current_plot.xaxis.set_major_locator(mdates.HourLocator(interval = 3000))
            current_plot.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 5000))
            
            #format labels to look cleaner
            fig.autofmt_xdate()
           


        canvas = FigureCanvasTkAgg(fig, master = self.window)  
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        #tool bar to explore plot
        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        
        #button to close window
        exitButton = tk.Button(self.window, text="Quit", command=self.window.destroy)
        exitButton.pack()

        
        statisticsButton = tk.Button(self.window, text="View Statistics") #add command=function as a parameter
        statisticsButton.pack()

        