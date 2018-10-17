import random
import sys


# Prints out the Board
def drawBoard(board):
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)
    print('    1   2   3   4   5   6   7   8')


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
def newBoard():

    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board


# WRITE ON BOARD NO VALIDATION
# PLAYER INPUT
def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move.')
        move = input().lower()
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            break
        else:
            print('That is not a valid move.')
            print('Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81, will be the top-right corner.')
    return[x, y]


def makeMove(board, tile, xstart, ystart):
    board[xstart][ystart] = tile
    return True


def chooseTile():
    print('Do you want to start first or second?')
    print('O starts First, X starts Second')
    playerTile = input().upper()
    while(playerTile not in ['O', 'X']):
        print('Do you want to start first or second?')
        print('O starts First, X starts Second')
        playerTile = input().upper()
    if playerTile == 'X':
        enemyTile = 'O'
    else: 
        enemyTile = 'X'
    return [playerTile, enemyTile]


tiles = chooseTile()
playerTile = tiles[0]
enemyTile = tiles[1]

board = newBoard()
resetBoard(board)
drawBoard(board)

print('PLAYER TILE: ' + playerTile)
print('ENEMY TILE: ' + enemyTile)

