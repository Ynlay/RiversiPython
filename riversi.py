import random
import sys 

# https://inventwithpython.com/chapter15.html

# Prints out the Board
def drawBoard(board):
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)

# Resets the Board
def resetBoard(board): 
    for x in range(8): 
        for y in range(8):
            board[x][y] = ' ' 

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

# Creates a blank board data structure
def getNewBoard():
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board

mainboard = getNewBoard()
resetBoard(mainboard)
drawBoard(mainboard)
