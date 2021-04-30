#coding=utf-8

from database import Database
from enum import Enum
from random import randrange,uniform,choice
from datetime import datetime
import math

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

class GameState(Enum):
    READY = 0
    ACTIVE = 1
    LOST = 2
    WON = 3

class GameBoard:
    width = 0
    height = 0
    mines = 0
    fieldsLeft = 0
    shown = []
    hidden = []
    newGame = True
    state = GameState.READY
    startTimestamp = None
    timer = 0
    flags = 0
    numberOfPlayers = 0
    namesOfPlayers = ""

    def __init__(self,width,height,mines):
        if(mines > width * height - 9):
            raise Exception("Max. miner tilladet er (bredde * højde - 9)")

        self.width = width
        self.height = height
        self.mines = mines
        self.flags = mines
        self.fieldsLeft = width * height - mines

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

    def getShownField(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return self.shown[x][y]

    def getNumberOfFlagsFromOffset(self, x, y):
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.getShownField(x+i,y+j) == FieldValue.FLAG:
                    counter += 1
        return counter

    def rightleftClick(self,x,y):
        if self.state == GameState.READY:
            self.setActive()

        if x < 0 or y < 0 or x >= self.width or y >= self.height or self.state != GameState.ACTIVE or self.shown[x][y].value < 1 or self.shown[x][y].value > 8:
            return [{'x':x,'y':y,'field':self.shown[x][y].value}]

        fields = [{'x':x,'y':y,'field':self.shown[x][y].value}]
        numberOfFlags = self.getNumberOfFlagsFromOffset(x, y)
        if(numberOfFlags == self.shown[x][y].value):
            fields = self.leftClick(fields,x,y+1)
            fields = self.leftClick(fields,x,y-1)
            fields = self.leftClick(fields,x+1,y)
            fields = self.leftClick(fields,x+1,y+1)
            fields = self.leftClick(fields,x+1,y-1)
            fields = self.leftClick(fields,x-1,y)
            fields = self.leftClick(fields,x-1,y+1)
            fields = self.leftClick(fields,x-1,y-1)

        return fields

    def rightClick(self,x,y):
        if self.state == GameState.READY:
            self.setActive()

        if x < 0 or y < 0 or x >= self.width or y >= self.height or self.state != GameState.ACTIVE:
            return [{'x':x,'y':y,'field':self.shown[x][y].value}]

        if self.shown[x][y] == FieldValue.FLAG:
            self.shown[x][y] = FieldValue.BLOCK
            self.flags += 1
        elif self.shown[x][y] == FieldValue.BLOCK:
            self.shown[x][y] = FieldValue.FLAG
            self.flags -= 1

        return [{'x':x,'y':y,'field':self.shown[x][y].value}]

    def leftClick(self,fields,x,y):
        if self.state == GameState.READY:
            self.setActive()
            
        if (x < 0 or y < 0 or x >= self.width or y >= self.height 
            or self.hidden[x][y] == self.shown[x][y]
            or self.shown[x][y] == FieldValue.FLAG
            or self.state != GameState.ACTIVE):
            return fields

        if self.newGame:
            self.initGame(x,y)

        self.shown[x][y] = self.hidden[x][y]
        fields.append({'x':x,'y':y,'field':self.shown[x][y].value})

        if self.hidden[x][y] == FieldValue.MINE:
            #Tabt
            fields = self.revealAllMines(fields) 
            self.setLost()
            return fields

        if self.hidden[x][y] == FieldValue.ZERO:
            fields = self.leftClick(fields,x,y+1)
            fields = self.leftClick(fields,x,y-1)
            fields = self.leftClick(fields,x+1,y)
            fields = self.leftClick(fields,x+1,y+1)
            fields = self.leftClick(fields,x+1,y-1)
            fields = self.leftClick(fields,x-1,y)
            fields = self.leftClick(fields,x-1,y+1)
            fields = self.leftClick(fields,x-1,y-1)
        
        self.fieldsLeft -= 1
        if(self.fieldsLeft == 0):
            #Vundet
            self.setWon()
            
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
        while(i<self.mines):
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

    def getCurrentTimeInSeconds(self):
        if self.startTimestamp is None:
            return 0
        if self.state == GameState.WON or self.state == GameState.LOST:
            return self.timer
        timestampNow = datetime.timestamp(datetime.now())
        self.timer = timestampNow - self.startTimestamp
        self.timer = round(self.timer)
        return self.timer

    def setActive(self):
        self.state = GameState.ACTIVE
        self.startTimestamp = datetime.timestamp(datetime.now())

    def setWon(self):
        self.getCurrentTimeInSeconds()
        database = Database()
        database.insert_highscore(self.width, self.height, self.timer, self.numberOfPlayers, self.namesOfPlayers)
        database.disconnect()
        self.state = GameState.WON

    def setLost(self):
        self.getCurrentTimeInSeconds()
        self.state = GameState.LOST


