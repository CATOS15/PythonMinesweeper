from enum import Enum
import math
from random import randrange

class GameBoards:
    def __init__(self,shown,hidden,width,height,numberOfMines,newGame):
        self.shown = shown
        self.hidden = hidden
        self.width = width
        self.height = height
        self.numberOfMines = numberOfMines
        self.newGame = newGame

    def initEmptyGameBoards(self): 
        self.shown =  [[0 for x in range(self.width)] for y in range(self.height)] 
        self.hidden =  [[0 for x in range(self.width)] for y in range(self.height)] 

        for i in range(self.width):
            for j in range(self.height):
                self.shown[i][j] = FieldValue.HIDDEN
                self.hidden[i][j] = FieldValue.HIDDEN


    def initGameBoard(self):
        ## Insert n number of mines in grid
        self.initMines(self.width,self.height)

        ## Add fields depending on proximity of mines
        self.initFields()

        ## Set new game
        self.newGame = False


    def initMines(self,width,height):
        mines_placed = 0

        while mines_placed < self.numberOfMines:
            x_mine = randrange(0,width)
            y_mine = randrange(0,height)
            
            if width == x_mine and height == y_mine or self.hidden[x_mine][y_mine] == FieldValue.MINE.value or self.hidden[x_mine][y_mine] == FieldValue.BLANK:
                continue

            self.hidden[x_mine][y_mine] = FieldValue.MINE.value
            mines_placed += 1

    def initFields(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.hidden[i][j] != None and self.hidden[i][j] != FieldValue.MINE.value and self.hidden[i][j] != FieldValue.BLANK:
                    pos_value = self.neighbors(i,j)
                    self.hidden[i][j] = pos_value

    def neighbors(self,start_x,start_y):
        nearbyMine = 0

        for i in range(start_x-1,start_x+1):
            for j in range(start_y-1,start_y+1):
                if not (i < 0 and j < 0) and not(i > self.width and j > self.height):
                    if i != start_x and j != start_y:
                        if self.hidden[i][j] == FieldValue.MINE.value:
                            nearbyMine +=1

        # for i in (start_x-1 for start_x in range(start_x+1)):
        #     for j in (start_y-1 for start_y in range(start_y+1)):
        #         if self.hidden[i][j] != None :
        #             if i != start_x and j != start_y:
        #                 if self.hidden[i][j] == FieldValue.MINE.value:
        #                     nearbyMine = nearbyMine + 1 
        return nearbyMine
















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
    HIDDEN = 0   ## Facedown, not marked
    ONE = 1      ## One mine near
    TWO = 2      ## One mine near
    THREE = 3    ## One mine near
    FOUR = 4     ## One mine near
    FIVE = 5     ## One mine near
    SIX = 6      ## One mine near
    SEVEN = 7    ## One mine near
    EIGHT = 8    ## One mine near
    MINE = 9    ## There is a mine
    FLAG = 10     ## Marked mine
    BLANK = 11   ## Click no mine near

