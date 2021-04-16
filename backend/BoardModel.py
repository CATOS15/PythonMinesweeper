from enum import Enum
import math
from random import randrange,uniform
import json

class Field:
    def __init__(self,fieldValue,visited):
        self.fieldValue = fieldValue
        self.visited = visited

class GameBoards:
    def __init__(self,hidden,width,height,numberOfMines,newGame):
        self.hidden = hidden
        self.width = width
        self.height = height
        self.numberOfMines = numberOfMines
        self.newGame = newGame

    ## Global return list
    returnValues = []

    def initEmptyGameBoards(self): 
        #self.shown = [[0 for x in range(self.width)] for y in range(self.height)]
        self.hidden =  [[0 for x in range(self.width)] for y in range(self.height)]
        
        for x in range(self.width):
            for y in range(self.height):
                self.hidden[x][y] = Field(FieldValue.HIDDEN,False)
            
                
    def initGameBoard(self,x,y):
        returnValues = []

        ## init blank area
        returnValues = self.initBlankStartArea(x,y)

        ## Insert n number of mines in grid
        self.initMines(self.width,self.height)

        ## Add fields depending on proximity of mines
        self.initFields()

        return returnValues


    def initBlankStartArea(self,x,y):
        returnValues = []

        if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
            self.hidden[x][y].fieldValue = FieldValue.BLANK
            returnValues.append({'x':x,'y':y,'field':self.hidden[x][y].fieldValue.value})

        return returnValues

    def initMines(self,width,height):
        mines_placed = 0

        while mines_placed < self.numberOfMines:
            x_mine = randrange(0,width)
            y_mine = randrange(0,height)
            
            if width == x_mine and height == y_mine or self.hidden[x_mine][y_mine].fieldValue == FieldValue.MINE or self.hidden[x_mine][y_mine].fieldValue == FieldValue.BLANK:
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



    def onClick(self,start_x,start_y):
        returnValues = []

        if (start_x >= 0 and start_y >= 0) and (start_x < self.width and start_y < self.height):
            if self.newGame:
                self.hidden[start_x][start_y].fieldValue = FieldValue.BLANK
                returnValues.append({'x':start_x,'y':start_y,'field':self.hidden[start_x][start_y].fieldValue.value})
            else:
                returnValues.append({'x':start_x,'y':start_y,'field':self.hidden[start_x][start_y].fieldValue.value})

        return json.dumps(returnValues)


            
            #returnValues.append("{Coordinates['x1:']}")

    # def onClick(self,start_x,start_y):
    #     if (start_x >= 0 and start_y >= 0) and (start_x < self.width and start_y < self.height):
    #         if self.hidden[start_x][start_y].fieldValue == FieldValue.MINE:
    #             self.shown[start_x][start_y].fieldValue = self.hidden[start_x][start_y].fieldValue
    #             ## lost frequence
    #             return
    #         elif self.hidden[start_x][start_y].fieldValue.value >= 1 and self.hidden[start_x][start_y].fieldValue.value <= 9:
    #             self.shown[start_x][start_y].fieldValue = self.hidden[start_x][start_y].fieldValue
    #             return
            # else: 
            #     self.blankNeighbors(start_x,start_x)

   
        








    # def blankNeighbors(self,start_x,start_y):
    #     for x in range(start_x-1,start_x+2):
    #         for y in range(start_y-1,start_y+2):
    #             if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
    #                 if self.hidden[x][y].visited:
    #                     continue
    #                 if self.hidden[start_x][start_y].value >= 1 and self.hidden[start_x][start_y].value <= 9:
    #                     self.shown = self.hidden
    #                 elif self.hidden[start_x][start_y] == FieldValue.BLANK:
    #                     self.blankNeighbors(x,y)

                         

    # def initBlankStartArea(self,x,y):
    #      ## Calculate num of blank fields 5%-25% blank fields
    #     min = 0.25
    #     max = 0.50
    #     num_fields = self.height * self.width
    #     procent_of_blank = uniform(min,max)
    #     blank_fields = math.floor(num_fields*procent_of_blank)

    #     blank_fields_insterted = 0




    # def insertBlankFields(self,x,y,num_blank_fields,blank_fields_insterted): 
    #     if blank_fields_insterted > blank_fields:
    #         return

    #      if (x >= 0 and y >= 0) and (x < self.width and y < self.height):
    #          if self.hidden != FieldValue.Blank or not self.visited:

        

    #     XorY =  randrange(0,2)
    #     UporDown =  randrange(-1,2)










    # def initStartArea(self,x,y):
    #     ## Set number of start field
    #     min = math.floor(self.width*self.height*0.1)
    #     max = math.floor(self.width*self.height*0.2)
    #     start_field = Random.randint(min, max)

    #     ## Set initalitial starting
    #     current_x = x
    #     current_y = y

    #     placed_start_fields = 0
        
    #     startingPoint = []

    #     while len(startingPoint) < start_field:
    #         if len(startingPoint) == 0:
    #            var = "kayt"
    #     ## lav et recursivt kald det tjekker nærliggende blanke felter
    #     ## Vi ønsker at lave et starts mønster, der sikre et starts område af en vis størrelse
    #     ## 
    
    # def recursiveStart(self, x,y,current_mine_nr):
    #     if self.numberOfMines < current_mine_nr:
    #         return False
    #     if self.hidden[x][y] is None:
    #         return False
    #     if self.hidden[x][y] == FieldValue.HIDDEN:
    #         self.hidden[x][y] = FieldValue.BLANK
    #         newX = x + randrange.randint(0,1)
    #         newY = y + randrange.randint(0,1)

    #         if self.hidden[newX][newY] == FieldValue.HIDDEN:
    #             self.hidden[newX][newY] =FieldValue.BLANK
        
    #     #recursiveStart(newX,newY,current_mine_nr)

        
                
class FieldValue(Enum):
    HIDDEN = 10  ## Facedown, not marked
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

