'''
Created on 18/09/2021

@author: yolan
'''
import numpy as np

if __name__ == '__main__':
    pass



def readFile(fileName):
    data = np.loadtxt(fileName, delimiter = " ") #puts the file into an array
    print(data)
    return data 

def getlocation(LocationData): 
    widthX =  LocationData[0]
    heightY =  LocationData[1]
    numberStartPoints = LocationData[2]
    locationArray = LocationData[3:]
    print("locarion array", np.shape(locationArray))

def getMaize(MaizeData):
    widthX =  MaizeData[0]
    heightY =  MaizeData[1]
    connectivity = MaizeData[2]
    maizeArray = MaizeData[3:]
    print("Maize data",np.shape(maizeArray))
    
LocationData = readFile("SCMP1\starting_locations.loc")
MaizeData = readFile("SCMP1\mazes\M0_1.mz")

getlocation(LocationData)
getMaize(MaizeData)