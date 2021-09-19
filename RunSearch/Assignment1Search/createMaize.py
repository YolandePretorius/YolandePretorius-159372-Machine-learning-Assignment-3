'''
Created on 18/09/2021

@author: yolan
'''
import numpy as np

startNodesList = []
listOfNodes =[]
listOfGoals =[]


if __name__ == '__main__':
    pass



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

def getNeighbourBinaryValues(x,y,maizeMatrix,nodeValue,xWidth,yHeight):
    if ((x >= 0) and (x<xWidth)) and ((y>=0) and (y < yHeight)):
        nodeValue = int(maizeMatrix[x][y])
        nodeBinaryValue = bin(nodeValue)
        return nodeBinaryValue
    else:
        return None
        

'''
Check if current node can arch with neighbour nodes through binary values.

'''
def checkNeighboursArch(x,y,maizeMatrix,nodeValue,xWidth,yHeight):
    nodeBinaryValue = bin(nodeValue)
    neighbourBinValue = getNeighbourBinaryValues(x+1,y,maizeMatrix,nodeValue,xWidth,yHeight)
    
        
    

'''
create a list of names (using row and column) for each node that will be used to conned to other nodes
'''
def matrixLoopthroughcreataList(maizeMatrix,xWidth,yHeight):
    x=0
    y=0
    for x in range(xWidth-1):
        for y in range(yHeight-1):
            name = createNodeName(x,y)
            nodeValue = int(maizeMatrix[x][y])
            if(nodeValue > 15):
                listOfGoals.append(name)
            listOfNodes.append(name) 
            checkNeighboursArch(x,y,maizeMatrix,nodeValue,xWidth,yHeight)          
            y=+1
        x =+1

'''
create a list of start nodes. Name consist of row and column
'''   
def loopThroughStartNodeListCreateNodeNames(startlocationArray):
    for node in startlocationArray:
        x = int(node[0])
        y = int(node[1])
        name = createNodeName(x, y)
        startNodesList.append(name)
        
def createNodeName(x,y):
    x =str(x)
    y = str(y)
    name = (x+","+y)
    return name


    
LocationData = readFile("SCMP1\starting_locations.loc")
MaizeData = readFile("SCMP1\mazes\M0_1.mz")

startlocationArray = getlocation(LocationData)
loopThroughStartNodeListCreateNodeNames(startlocationArray)
maizeMatrix,Xwidth,Yheight = getMaize(MaizeData)
matrixLoopthroughcreataList(maizeMatrix,Xwidth,Yheight)