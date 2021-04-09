from BoardModel import *




    


#def fieldClicked(gameboard):
    

    




def initGame(numberOfMines,width,height):
    ## Add information to gameboard
    print( "test ")
    gameboard = GameBoards(None,None,width,height,numberOfMines,True)

    ## Init empty gameboard
    gameboard.initEmptyGameBoards()

    ## Init fields in gameboard
    gameboard.initGameBoard()
    

    ## Set newgame false
    gameboard.newGame = False   

    printGameboard(gameboard)    



def printGameboard(gameboard):
    for r in gameboard.hidden:
        for c in r:
            print(str(c.value),end = " ")
        print()
            

initGame(23,5,5)

