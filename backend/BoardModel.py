from enum import Enum
from random import Random
import math

class GameBoards:
    def __init__(self,shown,hidden,width,height,numberOfMines,newGame):
        self.shown = shown
        self.hidden = hidden
        self.width = width
        self.height = height
        self.numberOfMines = numberOfMines
        self.newGame = newGame

    def initEmptyGameBoard(self,width,height,numberOfMines): 
        self.shown = [[]]
        self.hidden =  [[]]
        self.numberOfMines = numberOfMines

        for i in range(width):
            for j in range(height):
                
                self.shown[i][j] = FieldValue.HIDDEN
                self.hidden[i][j] = FieldValue.HIDDEN
    
        return GameBoards(self.shown,self.hidden,self.width,self.height)

    def initGameBoard(self,x,y):
        self.initMines(x,y)


        ## Set new game
        self.newGame = False


    def initMines(self,x,y):
        mines_placed = 0

        while mines_placed < self.numberOfMines:
            x_mine = Random(self.width)
            y_mine = Random(self.heigth)
            
            if x == x_mine and y == y_mine or self[x_mine][y_mine] == FieldValue.MINE or self[x_mine][y_mine] == FieldValue.BLANK:
                continue

            self.hidden[x_mine][y_mine] = FieldValue.MINE
            mines_placed += 1

    def initFields(self):
          for i in range(width):
            for j in range(height):
                var = "kayt"


    def initStartArea(self,x,y):
        ## Set number of start field
        min = math.floor(self.width*self.height*0.1)
        max = math.floor(self.width*self.height*0.2)
        start_field = Random.randint(min, max)

        ## Set initalitial starting
        current_x = self.x
        current_y = self.y

        placed_start_fields = 0

        ## lav et recursivt kald det tjekker nærliggende blanke felter
        ## Vi ønsker at lave et starts mønster, der sikre et starts område af en vis størrelse
        ## 
  

        
                
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
    FLAG = 9     ## Marked mine
    MINE = 10    ## There is a mine
    BLANK = 11   ## Click no mine near

