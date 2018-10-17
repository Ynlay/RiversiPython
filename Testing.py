import random
import sys 

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

def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True: 
        print ('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            break
        else: 
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81, will be the top-right corner.')
    return[x, y]

def makeMove(board, tile, xstart, ystart): 
    board[xstart][ystart] = tile
    return True

while True: 
    # Reset the board and game 
    mainboard = getNewBoard()
    resetBoard(mainboard)
    playerTile = 'X'
    computerTile = 'O'
    turn = 'player'



    while True: 
        if turn == 'player': 
            # Player's turn
            drawBoard(mainboard)
            move = getPlayerMove(mainboard, playerTile)
            makeMove(mainboard, playerTile, move[0], move[1])
        else: 
            # Computer's turn
            drawBoard(mainboard)
            input('Press Enter to continue')