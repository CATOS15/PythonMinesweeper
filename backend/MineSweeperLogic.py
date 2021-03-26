from BoardModel import *




    


def fieldClicked(gameboard):
    if gameboard.newGame:
        popluateGameBoard(gameboard)

    




def popluateGameBoard(gameboard,numberOfMines,x,y):
    ## Insert mines
    gameboard.numberOfMines = numberOfMines


    ## Set newgame false
    gameboard.newGame = False   



