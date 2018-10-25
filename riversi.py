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


# Sets the tile
def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip is False:
        return false

    board[xstart][ystart] = tile

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


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
                    print(x)
                    print(y)
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '  # Restores the empty space
    # If no tiles are flipped, this is not a valid move
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def Minimax(board, player, depth, maximizingPlayer):
    if depth == 0 or IsTerminalNode(board, player):
        return EvalBoard(board, player)
    if maximizingPlayer:
        bestValue = minEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = Minimax(boardTemp, player, depth - 1, False)
                    bestValue = max(bestValue, v)
    else:  # minimizingPlayer
        bestValue = maxEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = Minimax(boardTemp, player, depth - 1, True)
                    bestValue = min(bestValue, v)
    return bestValue


def AlphaBeta(board, player, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or IsTerminalNode(board, player):
        return EvalBoard(board, player)
    if maximizingPlayer:
        v = minEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = max(v, AlphaBeta(boardTemp, player, depth - 1, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break  # beta cut-off
        return v
    else:  # minimizingPlayer
        v = maxEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = min(v, AlphaBeta(boardTemp, player, depth - 1, alpha, beta, True))
                    beta = min(beta, v)
                    if beta <= alpha:
                        break  # alpha cut-off
        return v

tiles = chooseTile()
playerTile = tiles[0]
enemyTile = tiles[1]

board = newBoard()
resetBoard(board)
drawBoard(board)

print('PLAYER TILE: ' + playerTile)
print('ENEMY TILE: ' + enemyTile)

print("Make a move!: ")
while True:
    move = getPlayerMove(board, playerTile)
    makeMove(board, playerTile, move[0], move[1])
    drawBoard(board)
