from enum import Enum
import math
from random import randrange,uniform,choice

class GameBoard:
    ## Global values
    hidden = []
    shown = []
    newGame = True

    def __init__(self,width,height,numberOfMines):
        self.width = width
        self.height = height
        self.numberOfMines = numberOfMines

        self.shown = [[0 for x in range(self.height)] for y in range(self.width)]
        self.hidden =  [[0 for x in range(self.height)] for y in range(self.width)]
        
        for x in range(self.width):
            for y in range(self.height):
                self.hidden[x][y] = FieldValue.ZERO
                self.shown[x][y] = FieldValue.BLOCK

    def getShownFields(self):
        fields = []
        for x, row in enumerate(self.shown):
            for y, fieldValue in enumerate(row):
                fields.append({'x':x,'y':y,'field':fieldValue.value})
        return fields

    def rightClick(self,x,y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return

        if self.shown[x][y] == FieldValue.FLAG:
            self.shown[x][y] = FieldValue.BLOCK
        elif self.shown[x][y] == FieldValue.BLOCK:
            self.shown[x][y] = FieldValue.FLAG

        return {'x':x,'y':y,'field':self.shown[x][y].value}

    def leftClick(self,fields,x,y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height or self.hidden[x][y] == self.shown[x][y]:
            return fields

        if self.newGame:
            self.initGame(x,y)

        self.shown[x][y] = self.hidden[x][y]
        fields.append({'x':x,'y':y,'field':self.shown[x][y].value})

        if self.hidden[x][y] == FieldValue.MINE:
            fields = self.revealAllMines(fields)


        if  self.hidden[x][y] == FieldValue.ZERO:
            fields = self.leftClick(fields,x,y+1)
            fields = self.leftClick(fields,x,y-1)
            
            fields = self.leftClick(fields,x+1,y)
            fields = self.leftClick(fields,x+1,y+1)
            fields = self.leftClick(fields,x+1,y-1)

            fields = self.leftClick(fields,x-1,y)
            fields = self.leftClick(fields,x-1,y+1)
            fields = self.leftClick(fields,x-1,y-1)

        return fields


    def revealAllMines(self,fields):
        for x in range(self.width):
            for y in range(self.height):
                if self.hidden[x][y] == FieldValue.MINE:
                    self.shown[x][y] = self.hidden[x][y]
                    fields.append({'x':x,'y':y,'field':self.hidden[x][y].value})
        return fields


    def initGame(self,x,y):
        i = 0
        while(i<self.numberOfMines):
            xB = randrange(0,self.width)
            yB = randrange(0,self.height)

            if((x == xB and y==yB) or (x-1 == xB and y==yB) or (x-1 == xB and y-1==yB) or (x == xB and y-1==yB)
                or (x+1 == xB and y-1==yB) or (x+1 == xB and y==yB) or (x+1 == xB and y+1==yB) or (x == xB and y+1==yB) 
                or (x-1 == xB and y+1==yB) or self.hidden[xB][yB] == FieldValue.MINE):
                continue

            self.hidden[xB][yB] = FieldValue.MINE
            self.appendNumber(xB,yB+1)
            self.appendNumber(xB,yB-1)

            self.appendNumber(xB-1,yB)
            self.appendNumber(xB-1,yB-1)
            self.appendNumber(xB-1,yB+1)

            self.appendNumber(xB+1,yB)
            self.appendNumber(xB+1,yB-1)
            self.appendNumber(xB+1,yB+1)

            i+=1
            
        self.newGame = False
    
    def appendNumber(self,x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return

        if self.hidden[x][y] != FieldValue.MINE:
            self.hidden[x][y] = FieldValue(self.hidden[x][y].value+1) 


class FieldValue(Enum):
    BLOCK = 10
    FLAG = 11
    MINE = 12
    
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8