# -*- coding: utf-8 -*-

class Field(object):
    def __init__(self,pos,propert='empty'):
        self.dic = {'empty':0,'dirt':1,'obstacle':2,'wall':3}
        self.pos = pos
        self.property = self.dic[propert]
        self.visited = False
        
    def setProperty(self,propert):
        self.property = self.dic[propert]
        
    def fieldVisited(self):
        self.visited = True
        
    def isVisited(self):
        return self.visited
        
    def isWall(self):
        return self.property == 3

    def isObst(self):
        return self.property == 2
    
    def isDirt(self):
        return self.property == 1 
        
    def getField(self,pos):
        if pos == self.pos:
            return self
        return None
    
    def getPos(self):
        return self.pos
    
    def getProperty(self):
        return self.property
    
    def __contains__(self,item):
        return item.pos == self.pos and self.property == item.property and self.visited == item.visited
    
    def __str__(self):
        return str(self.pos) + " " + str(self.property) 
    