# -*- coding: utf-8 -*-
from Robot import *
import random as r
from matplotlib import pyplot as plt
import pylab 
import imageio
import os
import shutil
import subprocess
from Field import * 
from math import sqrt
class Board():
    def __init__(self, n, nObst, nDirt):
        self.n = n+2
        self.nObst = nObst
        self.nDirt = nDirt
        self.genFields()
        self.addBoundaries()
        self.robot = Robot(self.genRobotPos(),self.fields)
        
    def genRobotPos(self):
        field = self.getField((r.randint(1,self.n-1),r.randint(1,self.n-1)))
        while (field.isObst() or field.isDirt() or field.isWall()):
            field = self.getField((r.randint(1,self.n-1),r.randint(1,self.n-1)))
        return field
    
    def genObst(self):
        tempObst = []
        posObst = (r.randrange(1,self.n-1),r.randrange(1,self.n-1) )
        tempObst.append(posObst)
        while (len(tempObst) !=self.nObst):
            tempObst = list(tempObst)
            tempObst.append((r.randrange(1,self.n-1),r.randrange(1,self.n-1)))
            tempObst = set(tempObst)
        
        return list(tempObst)
    
    def genDirts(self,obstacles):
        tempDirts = []
        while (len(tempDirts) !=self.nDirt):
            posDirt = (r.randrange(1,self.n-1),r.randrange(1,self.n-1))   
            if posDirt not in obstacles:
                tempDirts.append(posDirt)
            tempDirts = list(set(tempDirts))
   
        return list(tempDirts)
    
    def genFields(self):
        self.fields = []
        lObst = self.genObst()
        lDirt = self.genDirts(lObst)
        for i in range(self.n):
            for j in range(self.n):
                if (i,j) in lObst:
                    self.fields.append(Field((i,j),'obstacle'))
                elif (i,j) in lDirt:
                    self.fields.append(Field((i,j),'dirt'))
                else:
                    self.fields.append(Field((i,j),'empty'))
    
    def addBoundaries(self):
        for i in range(self.n):
            self.getField((i,self.n-1)).setProperty('wall')
            self.getField((self.n-1,i)).setProperty('wall')
            self.getField((0,i)).setProperty('wall')
            self.getField((i,0)).setProperty('wall')
            
    def getField(self,pos):
        for item in self.fields:
            if (item.pos == pos):
                return item

    def getProperyOfField(self,fieldPos):
        for item in self.fields:
            if item.pos == fieldPos:
                return item.property
        
    def checkMoves(self,square):
        possMoves = []
        lMoves = [(-1,0),(1,0),(0,1),(0,-1)]
        for item in lMoves:
            move = tuple(map(sum, zip(self.pos, item)))
            if move in self.lAvail:
                possMoves.append(move)
        
    def draw(self,moves,pos,path,keepPictures = False, gif=True):
        ex = 0.001
        x,y = [i for i in range(self.n)], [i for i in range(self.n)]
        positions = [(i[0]+0.5,i[1]+0.5) for i in moves]
        lObst = []
        lDirt = []
        lWall = []   
        if (gif ==True):
            try: 
                os.makedirs(path[:-1])
            except OSError:
                if os.path.isdir(path[:-1]):
                    shutil.rmtree(path[:-1])
                    os.makedirs(path[:-1])
                    
        filenames = []
        lMoves = [(-1,0),(1,0),(0,1),(0,-1)]
        print(len(moves))
        for i in range(len(moves)):
            printProgressBar(i,len(moves)-1,"Progress","Creating gif")
            fig = plt.gcf()
            
            fig.set_size_inches(8, 8)
            plt.axis([0-ex, self.n+ex, 0-ex, self.n+ex])
            
            plt.gca().set_aspect('equal', adjustable='box')
            plt.grid(True,color = 'k')
            
            plt.gca().patch.set_facecolor('0.8')

            for item in lMoves:
                move = tuple(map(sum, zip(moves[i], item)))
                itemProp = self.getProperyOfField(move)
                if itemProp == 1:
                    lDirt.append(self.getField(move).pos)
                elif itemProp ==2:
                    lObst.append(self.getField(move).pos)
                elif itemProp ==3:
                    lWall.append(self.getField(move).pos)

            ox,oy = [x[0] + 0.5 for x in lObst], [x[1] + 0.5 for x in lObst]
            dx,dy = [x[0] + 0.5 for x in lDirt], [x[1] + 0.5 for x in lDirt]
            wx,wy = [x[0] + 0.5 for x in lWall], [x[1] + 0.5 for x in lWall]
            
            plt.plot(ox,oy,'ys',markersize=8/self.n*55)
            plt.plot(dx,dy,'k8',markersize=8/self.n*55)
            plt.plot(wx,wy,'gs',markersize=8/self.n*55)
            
            ax, ay = [x[0] for x in positions[:i+1]], [x[1]  for x in positions[:i+1]]
            
            plt.plot(ax,ay,'rs',markersize=8/self.n*55)
            plt.plot(positions[i][0],positions[i][1],'wo',markersize=8/self.n*30)
            f = path+str(i)+'.png'
            pylab.savefig(f)
            filenames.append(f)  
            plt.close()
            
        lWall = [x.pos for x in self.fields if x.property == 3]
        for i in range(len(moves),len(moves)+10):
            fig = plt.gcf()
            
            fig.set_size_inches(8, 8)
            plt.axis([0-ex, self.n+ex, 0-ex, self.n+ex])
            
            plt.gca().set_aspect('equal', adjustable='box')
            plt.grid(True,color = 'k')
            
            plt.gca().patch.set_facecolor('0.8')
            wx,wy = [x[0] + 0.5 for x in lWall], [x[1] + 0.5 for x in lWall]
            
            plt.plot(ox,oy,'ys',markersize=8/self.n*55)
            plt.plot(dx,dy,'k8',markersize=8/self.n*55)
            plt.plot(wx,wy,'gs',markersize=8/self.n*55)
                  
            plt.plot(ax,ay,'rs',markersize=8/self.n*55)
            plt.plot(positions[-1][0],positions[-1][1],'wo',markersize=8/self.n*30)
            f = path+str(i)+'.png'
            pylab.savefig(f)
            filenames.append(f)  
            plt.close()
            
        if (gif == True):
            images = []
            for filename in filenames:
                images.append(imageio.imread(filename))
            imageio.mimsave(path+'oursearch.gif', images,fps = int(sqrt(len(moves))/2))
            
        if (not keepPictures):
            for filename in filenames:
                os.remove(filename)
        subprocess.call(path+'oursearch.gif',shell=True)
        
    def drawGraph(self, moves, pos, graph, path, keepPictures = False, gif=False):
        
        filenames = []
        filenames2 = []
        prevVert = []
        currVert = []

        for i in range(len(moves)):
            printProgressBar(i,len(moves)-1,"Progress","Creating graph")
            prevVert = currVert
            currVert = graph.getVertex(moves[i])
            currVert.setColor('brown')
            if prevVert:
                prevVert.setColor('red')
            graph.makeDotGraph(str(i),path)
            filenames.append(path+str(i)+'.png')
            filenames2.append(path+str(i))
        if (gif):
            images = []
            for filename in filenames:
                images.append(imageio.imread(filename))
            imageio.mimsave(path+'graph.gif', images,fps = 6)
        if (not keepPictures):
            for i in range(len(filenames)):
                os.remove(filenames[i])
                os.remove(filenames2[i])
        subprocess.call(path+'graph.gif',shell=True)
        
    def run(self,sourcePath):
        print('Board ' + str(self.n) + ' x ' + str(self.n) +'.\n')
        print(str(self.nObst) + ' obstacles on the board.\n')
        print(str(self.nDirt) + ' dirts on the board.\n')
        dec = input(sourcePath + ' is the location where your gif files will be created.'\
              + 'If in your comupter this path already exists it will be replaced by the new folder.\n'\
              + 'Do you want to continue? [Y]\[N] \n')
        while (dec not in ['y', 'Y','n','N']):
            dec = input('Please the correct letter!\n' + sourcePath +\
                 ' is the location where your gif files will be created.'\
              + 'If in your comupter this path already exists it will be replaced by the new folder.\n'\
              + 'Do you want to continue? [Y]\[N] \n')
       
        while (dec in ['n','N']):     
            sourcePath = input ('Please type in a new path.\n')
            
            dec = input(sourcePath + ' is the location where your gif files will be created. '\
              + 'If in your comupter this path already exists, it will be replaced by the new folder.\n'\
              + 'Do you want to continue? [Y]\[N] \n')       
        return self.robot.discover(sourcePath)
            
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 70, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

    if iteration == total: 
        print()
        
if __name__ == '__main__':
    #type your path in here
    path = ''
    b = Board(5,3,3)
    b.draw(b.run(path),b.robot.posField.pos,path,False,True)   
