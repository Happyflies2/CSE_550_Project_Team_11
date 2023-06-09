# -*- coding: utf-8 -*-
"""
Classes:
    Data: Individual data object for each data stream that is imported
    DataLoader: Module to load and create data objects
"""
import pandas as pd
import numpy as np
from datetime import datetime

class Data:
    #data constructor method:
    #input: filePath for data
    def __init__(self, filePath):
        self.ImportData(filePath)
        self.preprocessTime()
    #Import data method:
    #opens the csv files, and puts them in the data frame
    def ImportData(self, filePath):
        self.summary = pd.read_csv(filePath+"/summary.csv")
        self.meta = pd.read_csv(filePath+"/metadata.csv")
    
    #function to turn single datetime column into seperate columns date and time
    def preprocessTime(self):
        datetime = self.summary["Datetime (UTC)"]
        dateIndex = datetime[0].find('T')
        timeIndex = datetime[0].find('Z')
        
        #split datetime, into date and time
        self.dates = np.array([datetime[i][0:dateIndex] for i in range(len(datetime))])
        self.times = np.array([datetime[i][dateIndex+1:timeIndex] for i in range(len(datetime))])
        #removes extra character T
        self.datetime = np.array([datetime[i].replace('T', ' ')[:-1] for i in range(len(datetime))])
        
    #Placeholder function for filter requirement
    #didn't quite work
    def filterData(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = input("Enter start date (YYYY-MM-DD): ")
        if end_date is None:
            end_date = input("Enter end date (YYYY-MM-DD): ")
            
        #convert start_date and end_date strings to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        #create condition to filter the summary dataframe based on user input
        condition = (self.dates >= start_date.strftime("%Y-%m-%d")) & (self.dates <= end_date.strftime("%Y-%m-%d"))
        
        #create new instance of data class for filtered data
        filtered_summary = self.summary[condition]
        filtered_data = Data("")
        filtered_data.summary = filtered_summary
        filtered_data.meta = self.meta
        filtered_data.preprocessTime()
        return filtered_data

class DataLoader:
    #function: adds data stream to list
    def ImportData(self, filePath):
        data = Data(filePath)
        self.data = data

