# -*- coding: utf-8 -*-
"""
Classes:
    Data: Individual data object for each data stream that is imported
    DataLoader: Module to load and create data objects
"""
import pandas as pd

class Data:
    def __init__(self, filePath):
        self.ImportData(filePath)
        
    def ImportData(self, filePath):
        self.data = pd.read_csv(filePath+"summary.csv")
        self.meta = pd.read_csv(filePath+"metadata.csv")


class DataLoader:
    def __init__(self):
        #list of data streams
        self.dataList = []
    
    #function: adds data stream to list
    def ImportData(self, filePath):
        data = Data(filePath)
        self.dataList.append(data)

