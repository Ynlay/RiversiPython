import random
import sys
import os
import copy


# Prints out the Board
def drawBoard(board):
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(n):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)
    print('    1   2   3   4   5   6   7   8')


# Resets the Board
def resetBoard(board):
    for x in range(n):
        for y in range(n):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


# Creates a blank board data structure
def newBoard():

    board = []
    for i in range(n):
        board.append([' '] * n)
    return board


# Player Input with validation on the board
def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move.')
        move = input().lower()
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) is False:
                print("Wrong Move try again!")
                continue
            else:
                break
        else:
            print('That is not a valid move.')
            print('Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81, will be the top-right corner.')
    return[x, y]


# if no valid move(s) possible then True
def isTerminalNode(board, player):
    for y in range(n):
        for x in range(n):
            if isValidMove(board, player, x, y):
                return False
    return True


# Calculates Best Move
def bestMove(board, player):
    maxPoints = 0
    mx = -1
    my = -1
    for y in range(n):
        for x in range(n):
            tilesToFlip = isValidMove(board, player, x, y)
            if tilesToFlip:
                boardTemp = makeMove(copy.deepcopy(board), player, x, y)

                points = AlphaBeta(boardTemp, player, depth, minEvalBoard,
                                   maxEvalBoard, True)

                if points > maxPoints:
                    maxPoints = points
                    mx = x
                    my = y
    return (mx, my)


# Sets the tile, returns the board
def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip is False:
        return false

    board[xstart][ystart] = tile

    for x, y in tilesToFlip:
        board[x][y] = tile
    return board


# Allows the player to pick the tile he wants
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


# Returns True if the coordinates are located on the board
def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


# Returns False if the player's move on space xstart, ystart is invalid
# If it is a valid movie, returns a list of spaces that would become the
# player's if they made a move here
def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile   # temporarily set the tile on the board

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1],
                                   [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        # There is a piece belonging to the other player next to our piece
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                # Break out of while loop then continue in for loop
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            # There are pieces to flip over. Go in the reverse direction until
            # we reach the original space, noting all the tiles along the way
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '  # Restores the empty space
    # If no tiles are flipped, this is not a valid move
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


# Alpha Beta pruning
def AlphaBeta(board, player, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or isTerminalNode(board, player):
        return evalBoard(board, player)
    if maximizingPlayer:
        v = minEvalBoard
        for y in range(n):
            for x in range(n):
                tilesToFlip = isValidMove(board, player, x, y)
                if tilesToFlip:
                    boardTemp = makeMove(copy.deepcopy(board), player, x, y)
                    v = max(v, AlphaBeta(boardTemp, player, depth - 1, alpha,
                                         beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break  # beta cut-off
        return v
    else:  # minimizingPlayer
        v = maxEvalBoard
        for y in range(n):
            for x in range(n):
                tilesToFlip = isValidMove(board, player, x, y)
                if tilesToFlip:
                    boardTemp = makeMove(copy.deepcopy(board), player, x, y)
                    v = min(v, AlphaBeta(boardTemp, player, depth - 1, alpha,
                            beta, True))
                    beta = min(beta, v)
                    if beta <= alpha:
                        break  # alpha cut-off
        return v


# Evaluates the board's score
def evalBoard(board, player):
    score = 0
    for y in range(n):
        for x in range(n):
            if board[y][x] == player:
                if (x == 0 or x == n - 1) and (y == 0 or y == n - 1):
                    score += 4  # corner
                elif (x == 0 or x == n - 1) or (y == 0 or y == n - 1):
                    score += 2  # side
                else:
                    score += 1
    return score

n = 8  # Board size
minEvalBoard = -1  # min - 1
maxEvalBoard = n * n + 4 * n + 4 + 1  # max + 1

tiles = chooseTile()
playerTile = tiles[0]
enemyTile = tiles[1]
currentTile = 'O'

depth = 4

board = newBoard()
resetBoard(board)
drawBoard(board)

print('PLAYER TILE: ' + playerTile)
print('ENEMY TILE: ' + enemyTile)

while True:

    if currentTile == playerTile:  # user's turn
        move = getPlayerMove(board, playerTile)
        makeMove(board, playerTile, move[0], move[1])
        drawBoard(board)
        currentTile = enemyTile
    else:  # AI's turn
        print('Confirm AI\'s turn (press any key)')
        input()
        (x, y) = bestMove(board, currentTile)
        if not (x == -1 and y == -1):
            board = makeMove(board, enemyTile, x, y)
            drawBoard(board)
            print('AI played (X Y): ' + str(x+1) + '' + str(y+1))
            currentTile = playerTile

    if isTerminalNode(board, currentTile):
            print('No more moves left! Cannot play! Game ended!')
            print('Score User: ' + str(evalBoard(board, 'O')))
            print('Score AI  : ' + str(evalBoard(board, 'X')))
            os._exit(0)
