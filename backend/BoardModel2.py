from enum import Enum
import math
from random import randrange,uniform,choice


class Field:
    def __init__(self,fieldValue,visited):
        self.fieldValue = fieldValue
        self.visited = visited


class GameBoard:
    ## Global values
    hidden = []
    shown = []
    newGame = True
    returnValues = []

    def __init__(self,width,height,numberOfMines):
        self.width = width
        self.height = height
        self.numberOfMines = numberOfMines


    def initEmptyGameBoards(self): 
         ## Init empty matrixes
        self.shown = [[0 for x in range(self.width)] for y in range(self.height)]
        self.hidden =  [[0 for x in range(self.width)] for y in range(self.height)]
        
        for x in range(self.width):
            for y in range(self.height):
                self.hidden[x][y] = Field(FieldValue.HIDDEN,False)
                self.shown[x][y] = Field(FieldValue.HIDDEN,False)

    def rightClick(self,x,y):
        self.returnValues = []

        if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
            self.shown[x][y].fieldValue
            return {'x':x,'y':y,'field':self.shown[x][y].fieldValue.value}

    def leftClick(self,fields,x,y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height or self.hidden[x][y].visited:
            return fields

        if self.newGame:
            self.initGameBoard(x,y)
            self.newGame = False

        self.shown[x][y].fieldValue = self.hidden[x][y].fieldValue
        self.hidden[x][y].visited = True
        fields.append({'x':x,'y':y,'field':self.shown[x][y].fieldValue.value})

        if self.hidden[x][y].fieldValue == FieldValue.MINE:
            fields = self.revealAllMines(fields)


        if  self.hidden[x][y].fieldValue == FieldValue.BLANK:
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
                if self.hidden[x][y].fieldValue == FieldValue.MINE and not self.hidden[x][y].visited:
                    fields.append({'x':x,'y':y,'field':self.hidden[x][y].fieldValue.value})
                    self.hidden[x][y].visited = True
        
        return fields

    def initGameBoard(self,x,y):
        ## Init blank starting area
        self.initBlankStartArea(x,y)

        ## Insert n number of mines in grid
        self.initMines()

        ## Add fields depending on proximity of mines
        self.initFields()

        return self.returnValues


    def initBlankStartArea(self,x,y):
        blank_fields = []

        ## Calculate num of blank fields 5%-25% blank fields
        min = 0.025
        max = 0.075
        num_fields = self.height * self.width
        procent_of_blank = uniform(min,max)
        num_blank_fields = math.floor(num_fields*procent_of_blank)

        while len(blank_fields) < num_blank_fields:
            if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
                if not self.hidden[x][y].visited:
                    if self.hidden[x][y].fieldValue != FieldValue.BLANK:
                        self.hidden[x][y].fieldValue = FieldValue.BLANK
                        self.shown[x][y].fieldValue = FieldValue.BLANK
                        blank_fields.append({'x':x,'y':y,'field':self.shown[x][y].fieldValue.value})

            ## Pick random inserted point
            random_coor = randrange(0,len(blank_fields))
            x = blank_fields[random_coor].get("x")
            y = blank_fields[random_coor].get("y")

            ## Go in random direction
            XorY =  randrange(0,2)
            num_list = [-1,1]
            UporDown =  choice(num_list)
            if(XorY == 0):
                x = UporDown + x
            elif(XorY == 1):
                y = UporDown + y


    def initMines(self):
            mines_placed = 0

            while mines_placed < self.numberOfMines:
                mineNear = False

                x_mine = randrange(0,self.width)
                y_mine = randrange(0,self.height)

                for x in range(x_mine-1,x_mine+2):
                    for y in range(y_mine-1,y_mine+2):
                        if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
                            if self.hidden[x][y].fieldValue == FieldValue.BLANK:
                                mineNear = True
                                break

                if not mineNear:
                    if self.width == x_mine and self.height == y_mine or self.hidden[x_mine][y_mine].fieldValue == FieldValue.MINE or self.hidden[x_mine][y_mine].fieldValue == FieldValue.BLANK:
                        continue

                    self.hidden[x_mine][y_mine].fieldValue = FieldValue.MINE
                    mines_placed += 1


    def initFields(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.hidden[x][y].fieldValue != None and self.hidden[x][y].fieldValue != FieldValue.MINE and self.hidden[x][y].fieldValue != FieldValue.BLANK:
                    pos_value = self.neighbors(x,y)
                    self.hidden[x][y].fieldValue = FieldValue(pos_value)

    def neighbors(self,start_x,start_y):
        nearbyMine = 0

        for x in range(start_x-1,start_x+2):
            for y in range(start_y-1,start_y+2):
                if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
                    if self.hidden[x][y].fieldValue == FieldValue.MINE:
                        nearbyMine +=1
        return nearbyMine



class FieldValue(Enum):
    HIDDEN = 9  ## Facedown, not marked
    FLAG = 11    ## There is a flag
    MINE = 12    ## There is a mine
    BLANK = 0    ## Click no mine near

    ONE = 1      ## One mine near
    TWO = 2      ## One mine near
    THREE = 3    ## One mine near
    FOUR = 4     ## One mine near
    FIVE = 5     ## One mine near
    SIX = 6      ## One mine near
    SEVEN = 7    ## One mine near
    EIGHT = 8    ## One mine near