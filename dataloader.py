# -*- coding: utf-8 -*-
"""
Classes:
    Data: Individual data object for each data stream that is imported
    DataLoader: Module to load and create data objects
"""
import pandas as pd
import numpy as np

class Data:
    def __init__(self, filePath):
        self.ImportData(filePath)
        self.preprocessTime()
        
    def ImportData(self, filePath):
        self.summary = pd.read_csv(filePath+"/summary.csv")
        self.meta = pd.read_csv(filePath+"/metadata.csv")
    
    #function to turn single datetime column into seperate columns date and time
    def preprocessTime(self):
        datetime = self.summary["Datetime (UTC)"]
        dateIndex = datetime[0].find('T')
        timeIndex = datetime[0].find('Z')
        
        #split datetime, into date and time
        #self.dates = pd.DataFrame([datetime[i][0:dateIndex] for i in range(len(datetime))],columns = ['Date'])
        #self.times = pd.DataFrame([datetime[i][dateIndex+1:timeIndex] for i in range(len(datetime))],columns = ['Time'])
        self.dates = np.array([datetime[i][0:dateIndex] for i in range(len(datetime))])
        self.times = np.array([datetime[i][dateIndex+1:timeIndex] for i in range(len(datetime))])
        #self.datetime = np.array(datetime)
        self.datetime = np.array([datetime[i].replace('T', ' ')[:-1] for i in range(len(datetime))])

class DataLoader:
    #function: adds data stream to list
    def ImportData(self, filePath):
        data = Data(filePath)
        self.data = data

