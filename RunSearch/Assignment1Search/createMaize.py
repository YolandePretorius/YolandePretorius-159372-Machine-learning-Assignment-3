'''
Created on 18/09/2021

@author: yolan
'''
import numpy as np
import Assignment1Search.searchProblem as SP

startNodesList = []
listOfNodes =[]
listOfGoals =[]
ArchListnonCyclic = []
# ArcInverseList = []
ArchListStr =[]


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
'''
Get binary number of the neighbor to see structure of node
Use binary number to determine if the node can form an arch. if there is a wall no arch will form 
'''
def getNeighbourBin(x,y,maizeMatrix,xWidth,yHeight):
    if ((x >= 0) and (x<xWidth)) and ((y>=0) and (y <yHeight)):
        nodeValueNeighbour = int(maizeMatrix[x][y])    
        nodeBinaryList = [int(i) for i in np.binary_repr(nodeValueNeighbour, 5)]
        return nodeBinaryList
    else:
        return None
 
def ArchTrueFalse(binNumCurent,binNumNeigh):
    if(binNumCurent or binNumNeigh):
        return False
    else: 
        return True
'''
create a acyclic  search solution by creating a list containing strings of all the archs and anti archs
If node arch and anti arch is not in the arch list then add 
'''
    
def AddToArchListACyclic(x,y,xdir,ydir,direction):
    if(direction == True):
        currentNodeName = createNodeName(x,y) 
        neighborNodeName = createNodeName(xdir,ydir)
        print(currentNodeName)
        print(neighborNodeName)
        archedPoints = SP.Arc(currentNodeName,neighborNodeName)
        antiArchedPoint = SP.Arc(neighborNodeName,currentNodeName)
        archPointStr = str(archedPoints)
        antiArchPointStr = str(antiArchedPoint)
        if(archPointStr not in ArchListStr) and (antiArchPointStr not in ArchListStr) :
            ArchListStr.append(archPointStr) # create a list of the different acrched nodes
            ArchListStr.append(antiArchPointStr)
            ArchListnonCyclic.append(archedPoints)
            print(ArchListnonCyclic)
        
def AddToArchListCyclic(x,y,xdir,ydir,direction):
    if(direction == True):
        currentNodeName = createNodeName(x,y) 
        neighborNodeName = createNodeName(xdir,ydir)
        print(currentNodeName)
        print(neighborNodeName)
        archedPoints = SP.Arc(currentNodeName,neighborNodeName)
        antiArchedPoint = SP.Arc(neighborNodeName,currentNodeName)
        archPointStr = str(archedPoints)
        antiArchPointStr = str(antiArchedPoint)
        if(archPointStr not in ArchListStr)and (antiArchPointStr not in ArchListStr):
            ArchListStr.append(archPointStr) # create a list of the different acrched nodes
            ArchListStr.append(antiArchPointStr)
            ArchListnonCyclic.append(antiArchedPoint)
            ArchListnonCyclic.append(archedPoints)
            print(ArchListnonCyclic)      
 
def createArchList(x,y,currentNodeBinaryList,neighbourBinValueDown,neighbourBinValueUp,neighbourBinValueLeft,neighbourBinValueRight):
    if(neighbourBinValueDown!= None):
        Down = ArchTrueFalse(currentNodeBinaryList[2],neighbourBinValueDown[4])
        AddToArchListCyclic(x,y,x+1,y,Down)
    if(neighbourBinValueUp != None):
        up   = ArchTrueFalse(currentNodeBinaryList[4],neighbourBinValueUp[2])
        AddToArchListCyclic(x,y,x-1,y,up)
    if(neighbourBinValueLeft != None):
        left = ArchTrueFalse(currentNodeBinaryList[1],neighbourBinValueLeft[3])
        AddToArchListCyclic(x,y,x,y-1,left)
    if(neighbourBinValueRight != None):  
        right = ArchTrueFalse(currentNodeBinaryList[3],neighbourBinValueRight[1])
        AddToArchListCyclic(x,y,x,y+1,right)  
   
'''
Check if current node can arch with neighbour nodes through binary values.
'''
def checkNeighboursArch(x,y,maizeMatrix,nodeValue,xWidth,yHeight):
    currentNodeBinaryList = [int(i) for i in np.binary_repr(nodeValue,5)]
    neighbourBinValueDown = getNeighbourBin(x+1,y,maizeMatrix,xWidth,yHeight)
    neighbourBinValueUp = getNeighbourBin(x-1,y,maizeMatrix,xWidth,yHeight)
    neighbourBinValueLeft = getNeighbourBin(x,y-1,maizeMatrix,xWidth,yHeight)
    neighbourBinValueRight = getNeighbourBin(x,y+1,maizeMatrix,xWidth,yHeight)
    createArchList(x,y,currentNodeBinaryList,neighbourBinValueDown,neighbourBinValueUp,neighbourBinValueLeft,neighbourBinValueRight)
         
    

'''
create a list of names (using row and column) for each node that will be used to conned to other nodes
'''
def matrixLoopthroughcreataList(maizeMatrix,xWidth,yHeight):
    x=0
    y=0
    for x in range(xWidth):
        for y in range(yHeight):
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


def runSearchProblem():    
    LocationData = readFile("SCMP1\starting_locations.loc")
    MaizeData = readFile("SCMP1\mazes\M0_1.mz")
    # LocationData = ("0,0")
    # MaizeData = readFile("SCMP1\mazes\Test2.mz")

    startlocationArray =getlocation(LocationData)
    loopThroughStartNodeListCreateNodeNames(startlocationArray)
    maizeMatrix,Xwidth,Yheight = getMaize(MaizeData)
    matrixLoopthroughcreataList(maizeMatrix,Xwidth,Yheight)

    searchproblemNew = SP.Search_problem_from_explicit_graph(listOfNodes,ArchListnonCyclic,start =startNodesList[0],goals=listOfGoals)
    # searchproblemNew = SP.Search_problem_from_explicit_graph(listOfNodes,ArchListnonCyclic,start =LocationData,goals=listOfGoals)
    return searchproblemNew
# runSearchProblem()