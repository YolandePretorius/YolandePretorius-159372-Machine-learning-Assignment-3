'''
Created on 18/09/2021

@author: yolan
'''
import numpy as np
import Assignment1Search.searchProblem as SP


startNodesList = []
listOfNodes =[]
listOfGoals =[]
ArchList = []
# ArcInverseList = []
ArchListStr =[]
heuristicMap ={}


if __name__ == '__main__':
    pass



def readFile(fileName):
    data = np.loadtxt(fileName, delimiter = " ") #puts the file into an array
    # print(data)
    return data 
'''
    Get list of start locations
'''
def getlocation(LocationData): 
    widthX =  LocationData[0]
    heightY =  LocationData[1]
    numberStartPoints = int(LocationData[2])
    locationArray = LocationData[3:]
    locationArray = locationArray.reshape(numberStartPoints,2)
    # print("locarion array", np.shape(locationArray))
    
    return locationArray
'''
create a maze matrix with width x and height y
'''
def getmaze(mazeData):
    widthX =  int(mazeData[0])
    heightY =  int(mazeData[1])
    connectivity = mazeData[2]
    mazeArray = mazeData[3:]
    newArray = mazeArray.reshape(heightY,widthX)
    # print("maze data",newArray)
    return(newArray,widthX,heightY)
'''
Get binary number of the neighbor to see structure of node
Use binary number to determine if the node can form an arch. if there is a wall no arch will form 
'''
def getNeighbourBin(x,y,mazeMatrix,xWidth,yHeight):
    if ((x >= 0) and (x<xWidth)) and ((y>=0) and (y <yHeight)):
        nodeValueNeighbour = int(mazeMatrix[x][y])    
        nodeBinaryList = [int(i) for i in np.binary_repr(nodeValueNeighbour, 5)]
        return nodeBinaryList
    else:
        return None
'''
Using an logic OR gate to determine if a arch will form
if there is a 1 in the direction the arch wants to be, it send back false meaning there is a wall and a arch can't form
1 or 1 = false
0 or 1 = false
1 or 0 = false
0 or 0 = true
  
   
'''
def ArchTrueFalse(binNumCurent,binNumNeigh):
    if(binNumCurent or binNumNeigh):
        return False
    else: 
        return True
'''
create a search solution by creating a list containing strings of all the archs and anti archs
If node arch and anti arch is not in the arch list then add both to the arch list as the arch goes both ways
'''

        
def AddToArch(x,y,xdir,ydir,direction):
    if(direction == True):
        currentNodeName = createNodeName(x,y) # create a string name using the x,y position of the node
        neighborNodeName = createNodeName(xdir,ydir)
        # print(currentNodeName)
        # print(neighborNodeName)
        archedPoints = SP.Arc(currentNodeName,neighborNodeName)
        antiArchedPoint = SP.Arc(neighborNodeName,currentNodeName)
        archPointStr = str(archedPoints)
        antiArchPointStr = str(antiArchedPoint)
        if(archPointStr not in ArchListStr)and (antiArchPointStr not in ArchListStr):
            ArchListStr.append(archPointStr) # create a list of the different acrched nodes
            ArchListStr.append(antiArchPointStr)
            ArchList.append(antiArchedPoint)
            ArchList.append(archedPoints)
            # print(ArchList)      
'''
Create a list containing all the nodes archs 
Check in all 4 directions if an arch can be create.
Arch can only be created if there is no wall in the direction the arch will be created.
Use binary value of each direction to determine if there is a wall or not.
''' 
def createArchList(x,y,currentNodeBinaryList,neighbourBinValueDown,neighbourBinValueUp,neighbourBinValueLeft,neighbourBinValueRight):
    if(neighbourBinValueDown!= None):
        Down = ArchTrueFalse(currentNodeBinaryList[2],neighbourBinValueDown[4])
        AddToArch(x,y,x+1,y,Down)
    if(neighbourBinValueUp != None):
        up   = ArchTrueFalse(currentNodeBinaryList[4],neighbourBinValueUp[2])
        AddToArch(x,y,x-1,y,up)
    if(neighbourBinValueLeft != None):
        left = ArchTrueFalse(currentNodeBinaryList[1],neighbourBinValueLeft[3])
        AddToArch(x,y,x,y-1,left)
    if(neighbourBinValueRight != None):  
        right = ArchTrueFalse(currentNodeBinaryList[3],neighbourBinValueRight[1])
        AddToArch(x,y,x,y+1,right)  
   
'''
Check if current node can arch with neighbour nodes through binary values.
'''
def checkNeighboursArch(x,y,mazeMatrix,nodeValue,xWidth,yHeight):
    currentNodeBinaryList = [int(i) for i in np.binary_repr(nodeValue,5)]
    neighbourBinValueDown = getNeighbourBin(x+1,y,mazeMatrix,xWidth,yHeight)
    neighbourBinValueUp = getNeighbourBin(x-1,y,mazeMatrix,xWidth,yHeight)
    neighbourBinValueLeft = getNeighbourBin(x,y-1,mazeMatrix,xWidth,yHeight)
    neighbourBinValueRight = getNeighbourBin(x,y+1,mazeMatrix,xWidth,yHeight)
    createArchList(x,y,currentNodeBinaryList,neighbourBinValueDown,neighbourBinValueUp,neighbourBinValueLeft,neighbourBinValueRight)
         
    

'''
create a list of names (using row and column) for each node that will be used to connect to other nodes
'''
def matrixLoopthroughcreataList(mazeMatrix,xWidth,yHeight):
    x=0
    y=0
    for x in range(xWidth):
        for y in range(yHeight):
            name = createNodeName(x,y)
            nodeValue = int(mazeMatrix[x][y])
            if(nodeValue > 15): # nodes with values > 15 is assigned as a goal node
                listOfGoals.append(name)
            listOfNodes.append(name) 
            checkNeighboursArch(x,y,mazeMatrix,nodeValue,xWidth,yHeight)          
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
'''
Use x and y position to create a string node name
'''  
def createNodeName(x,y):
    x =str(x)
    y = str(y)
    name = (x+","+y)
    return name
'''
 Used the website below to determine what the heuristc function should look like
 https://aigents.co/blog/publication/distance-metrics-for-machine-learning
 using manhattnan distace where on a node allows 4  directional movement
 heuristic value is calculated by determining the sum of distance between node x and y values from goal x and y values
 The value of the goal node will be 0 
 '''   
def calculateHeursticDistance(node,x,y,goalX,goalY):
    dx = abs(x - goalX)
    dy = abs(y - goalY)
    D = 1 # cost for moving one space between nodes
    cost = D*(dx + dy)
    heuristicMap[node] = cost
    # print(heuristicMap)

'''
Traverse through nodes and calculate heuristic value for each node.

'''   

def heuristic(goal):
    for node in listOfNodes:
        nodeXY = node.split(",")
        goalXY = goal.split(",")
        x =  int(nodeXY[0])
        y = int(nodeXY[1])
        goalX = int(goalXY[0])
        goalY = int(goalXY[1])
        calculateHeursticDistance(node,x,y,goalX,goalY)
        
def runSearchProblem():    
    LocationData = readFile("SCMP4\starting_locations.loc")
    mazeData = readFile("SCMP4\mazes\M100_10.mz")
    '''
    for a 3 x 3 maze test maze
    '''
    # LocationData = ("0,0")
    # mazeData = readFile("SCMP1\mazes\Test2.mz")

    startlocationArray =getlocation(LocationData)
    loopThroughStartNodeListCreateNodeNames(startlocationArray)
    mazeMatrix,Xwidth,Yheight = getmaze(mazeData)
    matrixLoopthroughcreataList(mazeMatrix,Xwidth,Yheight)
    heuristic(listOfGoals[0])
    # searchproblemNew = SP.Search_problem_from_explicit_graph(listOfNodes,ArchList,start =startNodesList[2],goals=listOfGoals,hmap=heuristicMap)
    searchproblemNew = SP.Search_problem_from_explicit_graph(listOfNodes,ArchList,start =startNodesList[0],goals=listOfGoals) # without heuristic map
    # searchproblemNew = SP.Search_problem_from_explicit_graph(listOfNodes,ArchList,start =LocationData,goals=listOfGoals)
    return searchproblemNew
# runSearchProblem()