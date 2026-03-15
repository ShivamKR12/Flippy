import random, sys, pygame, time, copy, os
# Import necessary modules for the game.
# - random: Used to make random choices, like who goes first or computer's moves.
# - sys: Provides access to system-specific parameters and functions, like exiting the program.
# - pygame: The main library for creating games in Python. It handles graphics, sound, and input.
# - time: Used for delays, like making the computer "think" before moving.
# - copy: Allows deep copying of objects, like duplicating the game board.
# - os: Provides functions for interacting with the operating system, like file paths.

from pygame.locals import *
# Import all constants and functions from pygame.locals.
# This includes things like QUIT, MOUSEBUTTONUP, KEYUP, K_ESCAPE, etc.
# These are used for handling events like closing the window or key presses.

# Game constants: These are fixed values that define the game's appearance and behavior.
# They are written in ALL CAPS by convention to indicate they shouldn't be changed during the game.

FPS = 10
# Frames Per Second: How many times the game updates and redraws the screen per second.
# A lower value like 10 means the game runs slower, which is fine for a turn-based game.

WINDOWWIDTH = 640
# The width of the game window in pixels.
WINDOWHEIGHT = 480
# The height of the game window in pixels.

SPACESIZE = 50
# The size of each square on the game board in pixels.
# Each tile (space) is 50x50 pixels.

BOARDWIDTH = 8
# The number of columns on the game board (horizontal).
BOARDHEIGHT = 8
# The number of rows on the game board (vertical).

# Tile types: Constants representing the different states a board space can have.
WHITE_TILE = 'WHITE_TILE'
# Represents a white game piece.
BLACK_TILE = 'BLACK_TILE'
# Represents a black game piece.
EMPTY_SPACE = 'EMPTY_SPACE'
# Represents an empty space on the board with no piece.
HINT_TILE = 'HINT_TILE'
# Represents a hint marker showing where the player can move.

ANIMATIONSPEED = 25
# The speed of animations, like flipping tiles. Higher values mean faster animations.

# Margins: Calculate the space around the board to center it in the window.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
# Horizontal margin: Space on the left and right of the board.
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)
# Vertical margin: Space on the top and bottom of the board.

# Colors: RGB tuples defining colors used in the game.
# RGB stands for Red, Green, Blue. Each value is from 0 to 255.
WHITE = (255, 255, 255)
# Pure white color.
BLACK = (0, 0, 0)
# Pure black color.
GREEN = (0, 155, 0)
# A green color for backgrounds.
BRIGHTBLUE = (0, 50, 255)
# A bright blue color for text backgrounds.
BROWN = (174, 94, 0)
# A brown color for hints.

# More color constants for text and UI elements.
TEXTBGCOLOR1 = BRIGHTBLUE
# Background color for some text elements.
TEXTBGCOLOR2 = GREEN
# Background color for other text elements.
GRIDLINECOLOR = BLACK
# Color of the grid lines on the board.
TEXTCOLOR = WHITE
# Color of the text.
HINTCOLOR = BROWN
# Color of the hint markers.

def resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    
    This function is used to find files like images, even when the game is packaged into an executable.
    When running as a script, it uses the current directory.
    When packaged with PyInstaller, it uses the temporary directory where files are extracted.
    
    Parameters:
    relative_path (str): The relative path to the resource file (e.g., 'image.png').
    
    Returns:
    str: The absolute path to the resource file.
    """
    try:
        # Try to get the path from PyInstaller's temporary directory.
        base_path = sys._MEIPASS
    except Exception:
        # If not packaged, use the current working directory.
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    # Join the base path with the relative path to get the full path.

def main():
    """
    The main function that starts the game.
    
    This function initializes Pygame, sets up the game window, loads resources,
    and enters the main game loop. It keeps restarting the game until the player
    chooses not to play again.
    
    No parameters.
    No return value.
    """
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE
    # Declare global variables that will be used throughout the game.
    # Global variables are accessible from any function in the file.
    # - MAINCLOCK: Controls the game's frame rate.
    # - DISPLAYSURF: The main window surface where everything is drawn.
    # - FONT: A small font for regular text.
    # - BIGFONT: A larger font for headings.
    # - BGIMAGE: The background image of the game board.
    
    pygame.init()
    # Initialize all Pygame modules. This must be called before using any Pygame functions.
    # It sets up the display, sound, etc.
    
    MAINCLOCK = pygame.time.Clock()
    # Create a Clock object to control the game's speed (frames per second).
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Create the game window with the specified width and height.
    # DISPLAYSURF is a Surface object representing the window.
    
    pygame.display.set_caption('flippy')
    # Set the title of the window to 'flippy'.
    
    logo = pygame.image.load(resource_path('flippylogo.png'))
    # Load the game icon image from the file 'flippylogo.png'.
    # resource_path ensures it works whether running as script or executable.
    
    pygame.display.set_icon(logo)
    # Set the window icon to the loaded logo image.
    
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    # Load a font for small text. 'freesansbold.ttf' is a built-in Pygame font.
    # Size 16 pixels.
    
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
    # Load a larger font for big text, size 32 pixels.
    
    boardImage = pygame.image.load(resource_path('flippyboard.png'))
    # Load the board image.
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    # Resize the board image to fit the entire board area (8x8 spaces, each 50 pixels).
    # smoothscale makes the scaling look better.
    
    boardImageRect = boardImage.get_rect()
    # Get a Rect object for the board image, which has position and size info.
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    # Position the board image at the top-left of the board area (with margins).
    
    BGIMAGE = pygame.image.load(resource_path('flippybackground.png'))
    # Load the background image.
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    # Scale it to fill the entire window.
    BGIMAGE.blit(boardImage, boardImageRect)
    # Draw the board image onto the background image at the specified position.
    # This creates a composite background with the board on top.
    
    while True:
        # Main game loop: Keep playing games until the player quits.
        if runGame() == False:
            # runGame() returns True if the player wants to play again, False otherwise.
            break
        # If runGame returns False, exit the loop and end the program.

def getSpaceClicked(mousex, mousey):
    """
    Convert mouse coordinates to board coordinates.
    
    Given the x and y position of the mouse click (in pixels),
    calculate which board space (column and row) was clicked.
    
    Parameters:
    mousex (int): The x-coordinate of the mouse click.
    mousey (int): The y-coordinate of the mouse click.
    
    Returns:
    tuple or None: (x, y) board coordinates if on the board, None otherwise.
    """
    x = (mousex - XMARGIN) // SPACESIZE
    # Calculate the column: Subtract the left margin, then divide by space size.
    # Integer division (//) gives the grid position.
    y = (mousey - YMARGIN) // SPACESIZE
    # Calculate the row: Subtract the top margin, then divide by space size.
    if isOnBoard(x, y):
        # Check if the calculated position is within the board boundaries.
        return (x, y)
        # Return the board coordinates as a tuple.
    return None
    # If not on the board, return None.

def drawInfo(boardToDraw, playerTile, computerTile, turn):
    """
    Draw the game information on the screen.
    
    This includes the current scores for player and computer,
    and whose turn it is. The text is drawn on the right side of the window.
    
    Parameters:
    boardToDraw: The board to get scores from (can be the main board or with hints).
    playerTile (str): The player's tile color ('WHITE_TILE' or 'BLACK_TILE').
    computerTile (str): The computer's tile color.
    turn (str): Whose turn it is ('player' or 'computer').
    
    No return value.
    """
    scores = getScoreOfBoard(boardToDraw)
    # Get the current scores from the board.
    playerScore = scores[playerTile]
    # Get the player's score.
    computerScore = scores[computerTile]
    # Get the computer's score.
    playerText = f'Player: {playerScore}'
    # Format the player's score text.
    computerText = f'Computer: {computerScore}'
    # Format the computer's score text.
    turnText = f'Turn: {turn.capitalize()}'
    # Format the turn text, capitalizing the first letter.
    
    playerSurf = FONT.render(playerText, True, TEXTCOLOR, TEXTBGCOLOR1)
    # Render the player text into a Surface (image) with the font.
    # True for anti-aliasing, TEXTCOLOR for text, TEXTBGCOLOR1 for background.
    playerRect = playerSurf.get_rect()
    # Get the Rect for positioning the text.
    playerRect.topleft = (WINDOWWIDTH - 120, 70)
    # Position it near the top-right of the window.
    
    computerSurf = FONT.render(computerText, True, TEXTCOLOR, TEXTBGCOLOR1)
    computerRect = computerSurf.get_rect()
    computerRect.topleft = (WINDOWWIDTH - 120, 90)
    # Similar for computer score, below the player score.
    
    turnSurf = FONT.render(turnText, True, TEXTCOLOR, TEXTBGCOLOR1)
    turnRect = turnSurf.get_rect()
    turnRect.topleft = (WINDOWWIDTH - 120, 110)
    # Turn text below the scores.
    
    DISPLAYSURF.blit(playerSurf, playerRect)
    # Draw the player text onto the display surface.
    DISPLAYSURF.blit(computerSurf, computerRect)
    DISPLAYSURF.blit(turnSurf, turnRect)
    # Draw the other texts.

def getComputerMove(mainBoard, computerTile):
    """
    Determine the computer's move.
    
    The computer randomly chooses from all valid moves.
    In a real AI, this would be smarter, but here it's simple.
    
    Parameters:
    mainBoard: The current game board.
    computerTile (str): The computer's tile color.
    
    Returns:
    tuple or None: (x, y) coordinates of the move, or None if no moves available.
    """
    validMoves = getValidMoves(mainBoard, computerTile)
    # Get a list of all valid moves for the computer.
    if validMoves:
        # If there are valid moves,
        return random.choice(validMoves)
        # Randomly pick one and return it.
    return None
    # If no valid moves, return None.

def runGame():
    """
    Run a single game of Othello/Reversi.
    
    This function handles the game loop: setting up the board, alternating turns,
    handling player input, computer moves, and checking for game end.
    At the end, it shows the result and asks if the player wants to play again.
    
    No parameters.
    
    Returns:
    bool: True if the player wants to play again, False otherwise.
    """
    mainBoard = getNewBoard()
    # Create a new empty board.
    resetBoard(mainBoard)
    # Set up the starting position with 4 tiles in the center.
    showHints = False
    # Initially, hints are not shown.
    turn = random.choice(['computer', 'player'])
    # Randomly decide who goes first.
    consecutivePasses = 0
    # Count how many turns in a row have been passed (no moves).
    
    drawBoard(mainBoard)
    # Draw the initial board on the screen.
    playerTile, computerTile = enterPlayerTile()
    # Ask the player to choose white or black, and assign tiles.
    
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    # Render the "New Game" button text.
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    # Position it at the top-right of the window.
    
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH - 8, 40)
    # "Hints" button below "New Game".
    
    while True:
        # Main game loop for this game.
        if turn == 'player':
            # It's the player's turn.
            validMoves = getValidMoves(mainBoard, playerTile)
            # Get all valid moves for the player.
            if validMoves:
                # If the player has moves,
                consecutivePasses = 0
                # Reset the pass counter.
                movexy = None
                # Variable to store the player's chosen move.
                while movexy == None:
                    # Loop until the player makes a valid move.
                    if showHints:
                        boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                        # If hints are on, show the board with hint markers.
                    else:
                        boardToDraw = mainBoard
                        # Otherwise, show the normal board.
                    checkForQuit()
                    # Check if the player wants to quit.
                    for event in pygame.event.get():
                        # Process all pending events.
                        if event.type == MOUSEBUTTONUP:
                            # If the mouse was clicked,
                            mousex, mousey = event.pos
                            # Get the mouse position.
                            if newGameRect.collidepoint((mousex, mousey)):
                                # If clicked on "New Game",
                                return True
                                # Start a new game.
                            elif hintsRect.collidepoint((mousex, mousey)):
                                # If clicked on "Hints",
                                showHints = not showHints
                                # Toggle hints on/off.
                            movexy = getSpaceClicked(mousex, mousey)
                            # Convert mouse position to board coordinates.
                            if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                                # If clicked on board but not a valid move,
                                movexy = None
                                # Ignore it.
                    drawBoard(boardToDraw)
                    # Draw the board (with or without hints).
                    drawInfo(boardToDraw, playerTile, computerTile, turn)
                    # Draw the scores and turn info.
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    # Draw the "New Game" button.
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    # Draw the "Hints" button.
                    MAINCLOCK.tick(FPS)
                    # Limit the frame rate.
                    pygame.display.update()
                    # Update the display to show the changes.
                makeMove(mainBoard, playerTile, movexy[0], movexy[1], True, mainBoard)
                # Make the player's move, with animation.
                turn = 'computer'
                # Switch to computer's turn.
            else:
                # If player has no valid moves,
                consecutivePasses += 1
                # Increment pass counter.
                turn = 'computer'
                # Pass to computer.
        else:
            # It's the computer's turn.
            validMoves = getValidMoves(mainBoard, computerTile)
            # Get computer's valid moves.
            if validMoves:
                # If computer has moves,
                consecutivePasses = 0
                # Reset pass counter.
                drawBoard(mainBoard)
                # Draw the current board.
                drawInfo(mainBoard, playerTile, computerTile, turn)
                # Draw info.
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)
                pygame.display.update()
                # Update display.
                time.sleep(random.randint(5, 15) * 0.1)
                # Wait a random time (0.5 to 1.5 seconds) to simulate thinking.
                x, y = getComputerMove(mainBoard, computerTile)
                # Get the computer's move.
                makeMove(mainBoard, computerTile, x, y, True, mainBoard)
                # Make the move with animation.
                turn = 'player'
                # Switch to player's turn.
            else:
                # If computer has no moves,
                consecutivePasses += 1
                # Increment pass counter.
                turn = 'player'
                # Pass to player.
        
        if consecutivePasses >= 2:
            # If both players passed in a row, game is over.
            break
            # Exit the game loop.
    
    drawBoard(mainBoard)
    # Draw the final board.
    drawInfo(mainBoard, playerTile, computerTile, turn)
    # Draw final scores.
    
    scores = getScoreOfBoard(mainBoard)
    # Get final scores.
    if scores[playerTile] > scores[computerTile]:
        text = 'You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile])
        # Player won.
    elif scores[playerTile] < scores[computerTile]:
        text = 'You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile])
        # Player lost.
    else:
        text = 'The game was a tie!'
        # Tie game.
    
    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    # Render the result text.
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    # Center it on the screen.
    DISPLAYSURF.blit(textSurf, textRect)
    # Draw the result text.
    
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)
    # "Play again?" below the result.
    
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)
    # "Yes" button on the left.
    
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)
    # "No" button on the right.
    
    while True:
        # Loop to wait for player's choice to play again or quit.
        checkForQuit()
        # Check for quit events.
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint((mousex, mousey)):
                    # If clicked "Yes",
                    return True
                    # Play again.
                elif noRect.collidepoint((mousex, mousey)):
                    # If clicked "No",
                    return False
                    # Quit.
        DISPLAYSURF.blit(textSurf, textRect)
        # Draw the result text.
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        # Draw the buttons.
        pygame.display.update()
        # Update display.
        MAINCLOCK.tick(FPS)
        # Limit frame rate.

def translateBoardToPixelCoord(x, y):
    """
    Convert board coordinates to pixel coordinates.
    
    Given a board position (x, y), calculate the pixel position
    of the center of that space on the screen.
    
    Parameters:
    x (int): Column on the board (0-7).
    y (int): Row on the board (0-7).
    
    Returns:
    tuple: (pixel_x, pixel_y) center of the space.
    """
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)
    # Add margin, multiply by space size, add half space to get center.

def animateTileChange(tilesToFlip, tileColor, additionalTile, mainBoard):
    """
    Animate the flipping of tiles when a move is made.
    
    This creates a visual effect where tiles change color gradually,
    and the new tile appears instantly.
    
    Parameters:
    tilesToFlip (list): List of (x, y) positions of tiles to flip.
    tileColor (str): The color of the player's tile ('WHITE_TILE' or 'BLACK_TILE').
    additionalTile (tuple): (x, y) position of the new tile placed.
    mainBoard: The game board.
    
    No return value.
    """
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
        # New tile is white.
    else:
        additionalTileColor = BLACK
        # New tile is black.
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    # Get pixel position of the new tile.
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    # Draw the new tile immediately.
    pygame.display.update()
    # Update the screen.
    MAINCLOCK.tick(ANIMATIONSPEED)
    # Wait a bit.
    
    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        # Loop through color values from 0 to 255 in steps.
        # This creates the gradual color change.
        
        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3)
            # For white tiles, start from black (0) to white (255).
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3)
            # For black tiles, start from white (255) to black (0).
        
        for x, y in tilesToFlip:
            # For each tile to flip,
            centerx, centery = translateBoardToPixelCoord(x, y)
            # Get its pixel position.
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
            # Draw it with the current color.
        pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
        # Redraw the new tile.
        
        drawBoard(mainBoard)
        # Redraw the board background.
        pygame.display.update()
        # Update screen.
        MAINCLOCK.tick(ANIMATIONSPEED)
        # Control animation speed.
        checkForQuit()
        # Allow quitting during animation.

def drawBoard(board):
    """
    Draw the game board and all tiles on the screen.
    
    This draws the background, then places tiles and hints on top.
    
    Parameters:
    board: The 2D list representing the game board.
    
    No return value.
    """
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())
    # Draw the background image (which includes the board grid).
    for x in range(BOARDWIDTH):
        # Loop through each column.
        for y in range(BOARDHEIGHT):
            # Loop through each row.
            centerx, centery = translateBoardToPixelCoord(x, y)
            # Get the pixel center of this space.
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                # If there's a tile here,
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                    # Set color to white.
                else:
                    tileColor = BLACK
                    # Set color to black.
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
                # Draw a circle for the tile.
            if board[x][y] == HINT_TILE:
                # If this is a hint,
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))
                # Draw a small square hint marker.

    for x in range(BOARDWIDTH + 1):
        # Draw the vertical grid lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
        # Draw a vertical line.
    for y in range(BOARDHEIGHT + 1):
        # Draw the horizontal grid lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
        # Draw a horizontal line.

def getNewBoard():
    """
    Create a new empty game board.
    
    Returns a 2D list with BOARDWIDTH columns and BOARDHEIGHT rows,
    all initialized to EMPTY_SPACE.
    
    No parameters.
    
    Returns:
    list: 2D list representing the board.
    """
    board = []
    # Start with empty list.
    for i in range(BOARDWIDTH):
        # For each column,
        board.append([EMPTY_SPACE] * BOARDHEIGHT)
        # Add a row of empty spaces.
    return board
    # Return the new board.

def resetBoard(board):
    """
    Reset the board to the starting position.
    
    Clears all spaces and places the initial 4 tiles in the center.
    
    Parameters:
    board: The board to reset (modified in place).
    
    No return value.
    """
    for x in range(BOARDWIDTH):
        # Loop through columns.
        for y in range(BOARDHEIGHT):
            # Loop through rows.
            board[x][y] = EMPTY_SPACE
            # Set to empty.
    # Place the starting tiles:
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE
    # Standard Othello starting position.

def getScoreOfBoard(board):
    """
    Count the number of white and black tiles on the board.
    
    Parameters:
    board: The game board.
    
    Returns:
    dict: {'WHITE_TILE': count, 'BLACK_TILE': count}
    """
    xscore = 0
    # White score.
    oscore = 0
    # Black score.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                xscore += 1
                # Count white tiles.
            if board[x][y] == BLACK_TILE:
                oscore += 1
                # Count black tiles.
    return {WHITE_TILE:xscore, BLACK_TILE:oscore}
    # Return as dictionary.

def enterPlayerTile():
    """
    Let the player choose their tile color.
    
    Displays options for white or black, waits for click.
    
    No parameters.
    
    Returns:
    tuple: (playerTile, computerTile) as strings.
    """
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    # Render the question text.
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    # Center it.
    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    # "White" option.
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)
    # Position left.
    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    # "Black" option.
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)
    # Position right.
    while True:
        # Loop until choice made.
        checkForQuit()
        # Check for quit.
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    # Chose white.
                    return [WHITE_TILE, BLACK_TILE]
                    # Player white, computer black.
                elif oRect.collidepoint((mousex, mousey)):
                    # Chose black.
                    return [BLACK_TILE, WHITE_TILE]
                    # Player black, computer white.
        DISPLAYSURF.blit(textSurf, textRect)
        # Draw question.
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        # Draw options.
        pygame.display.update()
        # Update screen.
        MAINCLOCK.tick(FPS)
        # Limit frame rate.

def makeMove(board, tile, xstart, ystart, realMove=False, mainBoard=None):
    """
    Make a move on the board.
    
    Places the tile and flips the opponent's tiles.
    If realMove is True, also animates the change.
    
    Parameters:
    board: The board to modify.
    tile (str): The tile color to place.
    xstart (int): Column to place tile.
    ystart (int): Row to place tile.
    realMove (bool): Whether this is a real move (with animation).
    mainBoard: The main board for animation (if different from board).
    
    Returns:
    bool: True if move was valid, False otherwise.
    """
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    # Check if move is valid and get tiles to flip.
    if tilesToFlip == False:
        # If invalid,
        return False
        # Return False.
    board[xstart][ystart] = tile
    # Place the tile.
    if realMove:
        # If real move,
        animateTileChange(tilesToFlip, tile, (xstart, ystart), mainBoard if mainBoard is not None else board)
        # Animate the flip.
        for x, y in tilesToFlip:
            # Then actually flip the tiles.
            board[x][y] = tile
    return True
    # Return success.

def isValidMove(board, tile, xstart, ystart):
    """
    Check if a move is valid and return tiles to flip.
    
    A move is valid if it places a tile that sandwiches opponent tiles
    in at least one direction, flipping them to your color.
    
    Parameters:
    board: The game board.
    tile (str): The tile color to place.
    xstart (int): Column to check.
    ystart (int): Row to check.
    
    Returns:
    list or False: List of (x, y) tiles to flip, or False if invalid.
    """
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        # If space not empty or out of bounds,
        return False
        # Invalid.
    board[xstart][ystart] = tile
    # Temporarily place the tile.
    otherTile = getOpponentTile(tile)
    # Get opponent's color.
    tilesToFlip = []
    # List to collect tiles to flip.
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        # Check all 8 directions.
        x, y = xstart, ystart
        # Start from the placed tile.
        x += xdirection
        y += ydirection
        # Move in this direction.
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # If next space has opponent tile,
            x += xdirection
            y += ydirection
            # Continue in direction.
            if not isOnBoard(x, y):
                # If went off board,
                continue
                # Skip this direction.
            while board[x][y] == otherTile:
                # While still opponent tiles,
                x += xdirection
                y += ydirection
                # Keep going.
                if not isOnBoard(x, y):
                    # If off board,
                    break
                    # Stop.
            if not isOnBoard(x, y):
                # If ended off board,
                continue
                # Skip.
            if board[x][y] == tile:
                # If ended on own tile,
                while True:
                    # Backtrack and collect tiles to flip.
                    x -= xdirection
                    y -= ydirection
                    # Move back.
                    if x == xstart and y == ystart:
                        # Until back at start,
                        break
                        # Done.
                    tilesToFlip.append([x, y])
                    # Add to flip list.
    board[xstart][ystart] = EMPTY_SPACE
    # Remove temporary tile.
    if len(tilesToFlip) == 0:
        # If no tiles to flip,
        return False
        # Invalid move.
    return tilesToFlip
    # Return the list of tiles to flip.

def isOnBoard(x, y):
    """
    Check if coordinates are within the board boundaries.
    
    Parameters:
    x (int): Column.
    y (int): Row.
    
    Returns:
    bool: True if on board, False otherwise.
    """
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT
    # Check if x and y are between 0 and board size - 1.

def getBoardWithValidMoves(board, tile):
    """
    Create a copy of the board with hint tiles for valid moves.
    
    Parameters:
    board: The original board.
    tile (str): The tile color to check moves for.
    
    Returns:
    list: A new board with HINT_TILE in valid move positions.
    """
    dupeBoard = copy.deepcopy(board)
    # Make a deep copy of the board.
    for x, y in getValidMoves(dupeBoard, tile):
        # For each valid move,
        dupeBoard[x][y] = HINT_TILE
        # Place a hint.
    return dupeBoard
    # Return the modified copy.

def getValidMoves(board, tile):
    """
    Get a list of all valid moves for a tile color.
    
    Parameters:
    board: The game board.
    tile (str): The tile color.
    
    Returns:
    list: List of (x, y) tuples for valid moves.
    """
    validMoves = []
    # Start empty list.
    for x in range(BOARDWIDTH):
        # Check every column.
        for y in range(BOARDHEIGHT):
            # Check every row.
            if isValidMove(board, tile, x, y) != False:
                # If move is valid,
                validMoves.append((x, y))
                # Add to list.
    return validMoves
    # Return the list.

def getOpponentTile(tile):
    """
    Get the opponent's tile color.
    
    Parameters:
    tile (str): A tile color.
    
    Returns:
    str: The opposite color.
    """
    if tile == WHITE_TILE:
        return BLACK_TILE
        # Opposite of white is black.
    else:
        return WHITE_TILE
        # Opposite of black is white.

def checkForQuit():
    """
    Check for quit events and handle them.
    
    If the user closes the window or presses Escape, quit the game.
    
    No parameters.
    No return value.
    """
    for event in pygame.event.get(QUIT):
        # If window close event,
        terminate()
        # Quit.
    for event in pygame.event.get(KEYUP):
        # If key released,
        if event.key == K_ESCAPE:
            # If Escape key,
            terminate()
            # Quit.
        else:
            pygame.event.post(event)
            # Otherwise, put the event back for other handlers.

def terminate():
    """
    Clean up and exit the program.
    
    Quits Pygame and exits the Python program.
    
    No parameters.
    No return value.
    """
    pygame.quit()
    # Shut down Pygame.
    sys.exit()
    # Exit the program.

if __name__ == '__main__':
    # If this script is run directly (not imported),
    main()
    # Start the game.
