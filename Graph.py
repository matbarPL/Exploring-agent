# -*- coding: utf-8 -*-
from graphviz import Digraph
from Queue import Queue
import sys
from Board import *

class Vertex:
    def __init__(self,num):
        self.id = num
        self.neighbours = {}
        self.color = 'white' #new: color of node
        self.dist = sys.maxsize #new: distance from beginning (will be used later)
        self.pred = None #new: predecessor
        self.disc = 0 #new: discovery time
        self.fin = 0 #new: end-of-processing time
        self.vis = False
        self.visCounter = 0
        self.isDeleted = False
        
    def addNeighbour(self,nbr,weight=0):
        self.neighbours[nbr] = weight
        
    def setColor(self,color):
        self.color = color
        
    def setDistance(self,d):
        self.dist = d
        
    def setPred(self,p):
        self.pred = p
        
    def setDiscovery(self,dtime):
        self.disc = dtime
        
    def setFinish(self,ftime):
        self.fin = ftime
    
    def setVisited(self, val):
        self.vis = val
        
    def getFinish(self):
        return self.fin
        
    def getDiscovery(self):
        return self.disc
        
    def getPred(self):
        return self.pred
        
    def getDistance(self):
        return self.dist
        
    def getColor(self):
        return self.color
        
    def getNeighbour(self):
        return self.neighbours.keys()
        
    def getNeigbourValues(self,vertIdList = []):
        x = []
        allVisited = True
        for item in self.getNeighbour():
            if not item.isDeleted and item.id not in vertIdList:
                x.append(item.id)
                
                
            if not item.vis:
                allVisited = False
        
        return (x,allVisited)
    
    def getPrior(self):
        return len(self.getNeighbour())
        
    def getAllPriors(self,takeOnlyVisited = 1):
        priors = []
        
        for item in self.getNeighbour():
           priors.append(item.getPrior()+5*item.visCounter*takeOnlyVisited)
            
        return priors
        
    def getWeight(self,nbr):
        return self.neighbours[nbr]
        
    def getVisited(self):
        return self.vis
        
    def setDeleted(self):
        if (len(self.getNeigbourValues()[0]) == 1 ):
                self.isDeleted = True
                
    def getId(self):
        return self.id
                
    def __str__(self):
        
        return str(self.id)+ '-->' + " Color: " + self.color + ", Discovered: " + str(self.disc) + ", Finished:  " + str(self.fin) +\
        ", Distance: " + str(self.dist) + ", Predecessor \n\t[" + str(self.pred)+ "]"

class Graph():
    def __init__(self):
        self.VertexList = {}
        self.numVert = 0
        self.time = 0
        
    def addVertex(self, vert):
        self.numVert += 1
        newVert = Vertex(vert)
        self.VertexList[vert] = newVert
        
    def addEdge(self, fromVert, toVert, weight = 1):
        if fromVert not in self.VertexList.keys():
            self.addVertex(fromVert)
        if toVert not in self.VertexList.keys():
            self.addVertex(toVert)
        self.VertexList[fromVert].addNeighbour(self.VertexList[toVert], weight)
    
    def getVertex(self, vertKey):
        if vertKey in self.VertexList.keys():
            return self.VertexList[vertKey]
        else:
            return None
            
    def getVertices(self):
        return self.VertexList.keys()
        
    def setAllWhite(self):
        for vert in self:
            vert.setColor('white')
        
    def __iter__(self):
        return iter(self.VertexList.values())

    def __contains__(self,n):
        return n in self.VertexList
        
    def getEdges(self):
        connections = []
        for vertKey in self.VertexList.keys():
            vertVal=self.VertexList[vertKey]
            for i in vertVal.getNeighbour():
                connections.append((vertKey, i.getId(), vertVal.getWeight(self.VertexList[i.getId()])))
        return connections
        
    def makeDotGraph(self,name,path =''):
        dot = Digraph(comment='The Round Table',format='png')
        for node in list(self.getVertices()):
            color = self.getVertex(node).color
            dot.node(str(node), None, color=[color if color !='white' else 'yellow'][0], style='filled') 
            
        for edge in self.getEdges():
            dot.edge(str(edge[0]), str(edge[1]),None, color="red" )        
        dot.render(path+name, view=False)
    
    def optWay(self, toVert):
        predList = []
        currentVert = self.getVertex(toVert)
        while currentVert.getPred() != None :
            predList.append(currentVert.getPred())
            currentVert = currentVert.getPred()
        toPrtList = [item.id for item in predList]
        toPrtList = toPrtList[::-1]
        toPrtList.append(toVert)
        if len(toPrtList)>1:
            return toPrtList[1:]
        return toPrtList[:]
    def bfs(self, start): 
        start=self.getVertex(start)
        if start:
            counter=0
            start.setDistance(0)
            start.setPred(None)
            vertQueue = Queue()
            vertQueue.enqueue(start)
            while (vertQueue.size() > 0 ):
                
                currentVert = vertQueue.dequeue()
                for nbr in currentVert.getNeighbour():
                    counter += 1
                    if (nbr.getColor() == 'white' and nbr.id.getProperty() not in [2,3]):
                        nbr.setColor('brown')
                        nbr.setDistance(currentVert.getDistance() + 1)
                        nbr.setPred(currentVert)
                        vertQueue.enqueue(nbr)
                currentVert.setColor('grey')

    def findBestPath(self,start):
        self.bfs(start)
        self.setAllWhite()
        minDist = 10000
        minVert = self.getVertex(start) #dopisane
        for vert in self:
            if not vert.vis and vert.dist < minDist :
                minDist = vert.dist
                minVert = vert
        return self.optWay(minVert.id)
        
    def ourSearch(self,start,n,nObst):
        current = self.getVertex(start)
        path = []
        escapeList = []
        path.append(current.id)
        current.vis = True
        current.visCounter +=1 
        current.setDeleted()
        currNeighbours,allVisited = current.getNeigbourValues()
        neighPriors = list(zip(list(currNeighbours), current.getAllPriors()))
        
        while (len(set(path)) < n**2 - nObst):
            if(not allVisited):
                minimum = min(neighPriors, key=lambda x: x[1])
                current = self.getVertex(minimum[0]) 
                path.append(current.id)
                escapeList= []
            else:
                bestPath = self.findBestPath(current.id)
                path.extend(bestPath[1:])
                current = self.getVertex(bestPath[-1])
                
            currNeighbours,allVisited = current.getNeigbourValues()
            neighPriors = list(zip(list(currNeighbours), current.getAllPriors()))
            current.vis = True
            current.setDeleted()
            current.visCounter +=1
            
        return path


        