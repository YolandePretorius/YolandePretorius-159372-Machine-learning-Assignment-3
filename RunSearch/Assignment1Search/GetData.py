'''
Created on 20/09/2021

@author: yolan
'''
import numpy as np
import Assignment1Search.searchProblem as searchProblem



def readFile(fileName):
    data = np.loadtxt(fileName, delimiter = " ") #puts the file into an array
    print(data)
    return data 

def getlocation(LocationData): 
    widthX =  LocationData[0]
    heightY =  LocationData[1]
    numberStartPoints = int(LocationData[2])
    locationArray = LocationData[3:]
    locationArray = locationArray.reshape(numberStartPoints,2)
    print("locarion array", np.shape(locationArray))
    
    return locationArray

def getMaize(MaizeData):
    widthX =  int(MaizeData[0])
    heightY =  int(MaizeData[1])
    connectivity = MaizeData[2]
    maizeArray = MaizeData[3:]
    newArray = maizeArray.reshape(heightY,widthX)
    print("Maize data",newArray)
    return(newArray,widthX,heightY)

LocationData = readFile("SCMP1\starting_locations.loc")
MaizeData = readFile("SCMP1\mazes\M0_1.mz")
startlocationArray = getlocation(LocationData)
maizeMatrix,Xwidth,Yheight = getMaize(MaizeData)
node = startlocationArray[0]

searchProblem.Search_problem.start_node(node)

