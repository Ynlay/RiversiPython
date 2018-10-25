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

# Returns True if the coordinates are located on the board
def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7

# Returns False if the player's move on space xstart, ystart is invalid
# If it is a valid movie, returns a list of spaces that would become the player's if they made a move here
def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != '' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    
    tilesToFlip = []
    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1][-1,-1],[-1,0],[-1,1]]:
        x,y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction 

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
            # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way
            if board[x][y] == tile: 
                while True: 
                    x -= xdirection
                    y -= ydirection 
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x,y])
    
    board[xstart][ystart] = '' # Restores the empty space
    # If no tiles are flipped, this is not a valid move
    if len(tilesToFlip) == 0: 
        return False
    return tilesToFlip

# Returns a new board with '.' marking the valid moves the given player can make
def getBoardWithValidMoves(board, tile):
    dupeBoard = getBoardCopy(board)

    for x,y in getValidMoves(dupeBoard,tile):
        dupeBoard[x][y] = '.'
    return dupeBoard
    
# Returns a list of [x,y] lists of valid moves for the given player on the given board
def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x,y])
    return validMoves

# Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'
def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8): 
        for y in range(8):
            if board[x][y] == 'X': 
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

# Let the plyaer type which tile they want to be
def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    
    # The first element in the list is the player's tile, the second is the computer's tile
    if tile == 'X':
        return['X','O']
    else: 
        return['O','X']

# Randomly choose the player who goes first
def whoGoesFirst(): 
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'player'

# Returns True if the player wants to play again
def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Place the tile on the board at xstart, ystart and flip any of the opponent's pieces
# Returns False if this is an invalid move, True if it is valid
def makeMove(board, tile, xstart, ystart): 
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x,y in tilesToFlip: 
        board[x][y] = tile
    return True

# Make a duplicate of the board list and return the duplicate
def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard

# Returns True if the position is in one of the four corners
def isOnCorner(x, y):
    return (x==0 and y==0) or (x==7 and y==0) or (x==0 and y==7) or (x==7 and y==7)

# Let the player type in their move. Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
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
            if isValidMove(board, playerTile, x, y) == False: 
                continue
            else: 
                break
        else: 
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81, will be the top-right corner.')
    return[x, y]
    
 # Given a board and the computer's tile, determine where to move and return that move as a [x, y] list
def getComputerMove(board, computerTile):
   
    possibleMoves = getValidMoves(board, computerTile)

    # Randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # Always go for a corner if available
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    
    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    bestMove = [-1,-1]
    for x, y in possibleMoves: 
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x,y]
            bestScore = score
    return bestMove
    
def showPoints(playerTile, computerTile):
    # Prints out the current score
    scores = getScoreOfBoard(mainboard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))


print('Welcome to Othello!')

while True: 
    # Reset the board and game 
    mainboard = getNewBoard()
    resetBoard(mainboard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True: 
        if turn == 'player': 
            # Player's turn
            if showHints: 
                validMovesBoard = getBoardWithValidMoves(mainboard, playerTile)
                drawBoard(validMovesBoard)
            else: 
                drawBoard(mainboard)
                
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainboard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # Terminate
            elif move == 'hints':
                showHints = not showHints
                continue
            else: 
                makeMove(mainboard, playerTile, move[0], move[1])

            if getValidMoves(mainboard, computerTile) == []:
                break
            else: 
                turn = 'computer'
        else: 
            # Computer's turn
            drawBoard(mainboard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainboard, computerTile)
            makeMove(mainboard, computerTile, x, y)

            if getValidMoves(mainboard, playerTile) == []: 
                break
            else: 
                turn = 'player'

    # Display the final score
    drawBoard(mainboard)
    scores = getScoreOfBoard(mainboard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]: 
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]: 
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else: 
        print('The game was a tie!')
    if not playAgain():
        break
