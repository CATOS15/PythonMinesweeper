from BoardModel import *




    


def fieldClicked(gameboard):
    gameboard.blankNeighbors(2,2)
    printGameboard(gameboard)    


def onClick(gameboard,x,y):
    returnValues = []

    if gameboard.newGame:
        returnValues = gameboard.initGameBoard(10,10)
        gameboard.newGame = False
   
    
    return returnValues




def initGame(difficulty,width,height):
    numberOfMines = 99
    gameboard = GameBoard(None,None,width,height,numberOfMines,True,difficulty)

    ## Init empty gameboard
    gameboard.initEmptyGameBoards()
    gameboard.newGame = True  

    return gameboard



def printGameboard(gameboard):
    for r in gameboard:
        for c in r:
            print(str(c.fieldValue.value),end = " ")
        print()
    print("\n")

            



returnValues = []
gameboard = initGame(1,24,24)
#printGameboard(gameboard)

returnValues = gameboard.initGameBoard(10,10)

printGameboard(gameboard.hidden)
print("Shown:")
printGameboard(gameboard.shown)
print(returnValues)
print("\n")

# returnValues = gameboard.click(4,4,False)
# print("Shown:")
# printGameboard(gameboard.shown)

##print(returnValues)
##print("\n")