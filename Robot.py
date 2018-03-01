# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 20:42:57 2018

@author: Mateusz
"""

import random as r
from Board import *
from Graph import *

class Robot():
    def __init__(self,startField,boardFields):
        self.posField = startField
        self.boardFields = boardFields
        self.fields = []
        self.lAvail = []
        self.lDirt = []
        self.lObst = []
        self.lWall = []
        self.path = [self.posField.pos]
        self.graph = Graph()
        
    def addFields(self,lFields):
        lMoves = {(-1,0):'left',(1,0):'right',(0,1):'up',(0,-1):'down'}
        for field in lFields:
            if field not in self.fields:
                if field.getProperty() == 0:
                    self.lAvail.append(field.pos)
                elif field.getProperty() == 1:
                    self.lDirt.append(field.pos)
                elif field.getProperty() == 2:
                    self.lObst.append(field.pos)
                else:
                    self.lWall.append(field.pos)
                    lMoves[tuple(map(sum, zip(self.posField.pos, tuple(map(lambda x :-x, field.pos)))))]
                self.fields.append(field)
                
    def move(self):
        lMoves = [(-1,0),(1,0),(0,1),(0,-1)]
        lFields = []
        
        for item in lMoves:
            move = tuple(map(sum, zip(self.posField.pos, item)))
            for field in self.boardFields:
                if field.pos == move:
                    lFields.append(field)
                    self.graph.addEdge(self.posField,field)
       
        self.addFields(lFields)
        self.posField.fieldVisited()
        self.graph.getVertex(self.posField).setVisited(True)
        notVisited = [x for x in lFields if not x.isVisited() and x.property not in [2,3]]
        if (len(notVisited) != 0):
            self.posField = notVisited[r.randint(0,len(notVisited)-1)]
            self.path.append(self.posField.pos)
        else:
            escapeList = self.graph.findBestPath(self.posField)
            self.posField = escapeList[-1]
            pToExt = [x.pos for x in escapeList]
            self.path.extend(pToExt)
            
    def finish(self):
        if len(self.path) > 4:
            return self.path[-1] == self.path[-2] == self.path[-3] == self.path[-4]
        return False
        
    def discover(self,sourcePath):
        while (not self.finish()):
            self.move()
        self.path = self.path[:-3]
        return self.path
    

    
    