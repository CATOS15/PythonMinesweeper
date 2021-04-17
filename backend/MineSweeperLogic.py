from BoardModel2 import *

    

def fieldClicked(gameboard):
    gameboard.blankNeighbors(2,2)
    printGameboard(gameboard)    


def onClick(gameboard,x,y):
    returnValues = []

    if gameboard.newGame:
        returnValues = gameboard.initGameBoard(10,10)
        gameboard.newGame = False
   
    
    return returnValues




def initGame(difficulty):
    ## Set number of mines
    numberOfMines = 0
    width = 0
    height = 0

    if difficulty == 0:
        numberOfMines = 10
        width = 10
        height = 8
    elif difficulty == 1:
        numberOfMines = 40
        width = 14
        height = 14
    elif difficulty == 2:
        numberOfMines = 99
        width = 24
        height = 20

    gameboard = GameBoard(width,height,numberOfMines)

    ## Init empty gameboard
    gameboard.initEmptyGameBoards()

    return gameboard



def printGameboard(gameboard):
    for r in gameboard:
        for c in r:
            print(str(c.fieldValue.value),end = " ")
        print()
    print("\n")

            



# returnValues = []
# gameboard = initGame(1,24,24)
# #printGameboard(gameboard)

# returnValues = gameboard.initGameBoard(10,10)

# printGameboard(gameboard.hidden)
# print("Shown:")
# printGameboard(gameboard.shown)
# print(returnValues)
# print("\n")

# # returnValues = gameboard.click(4,4,False)
# # print("Shown:")
# # printGameboard(gameboard.shown)

# ##print(returnValues)
# ##print("\n")