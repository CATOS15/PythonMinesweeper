from BoardModel import *




    


def fieldClicked(gameboard):
    gameboard.blankNeighbors(2,2)
    printGameboard(gameboard)    


def onClick(gameboard,x,y):
    returnValues = []

    if gameboard.newGame:
        returnValues = gameboard.initGameBoard(2,2)
        gameboard.newGame = False
   
    
    return returnValues




def initGame(difficulty,width,height):
    numberOfMines = 5
    gameboard = GameBoard(None,width,height,numberOfMines,True,difficulty)

    ## Init empty gameboard
    gameboard.initEmptyGameBoards()
    gameboard.newGame = True  

    return gameboard



def printGameboard(gameboard):
    for r in gameboard.hidden:
        for c in r:
            print(str(c.fieldValue.value),end = " ")
        print()
    print("\n")

            



returnValues = []
gameboard = initGame(1,5,5)
printGameboard(gameboard)

returnValues = gameboard.initGameBoard(2,2)
printGameboard(gameboard)
print(returnValues)
print("\n")

returnValues = gameboard.click(4,4,False)
print(returnValues)
print("\n")