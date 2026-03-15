# Import necessary modules for the game.
import random, sys, pygame, time, copy, os
# - random: Used to make random choices, like who goes first or computer's moves.
# - sys: Provides access to system-specific parameters and functions, like exiting the program.
# - pygame: The main library for creating games in Python. It handles graphics, sound, and input.
# - time: Used for delays, like making the computer "think" before moving.
# - copy: Allows deep copying of objects, like duplicating the game board.
# - os: Provides functions for interacting with the operating system, like file paths.

# Import all constants and functions from pygame.locals.
from pygame.locals import *
# This includes things like QUIT, MOUSEBUTTONUP, KEYUP, K_ESCAPE, etc.
# These are used for handling events like closing the window or key presses.

# Game constants: These are fixed values that define the game's appearance and behavior.
# They are written in ALL CAPS by convention to indicate they shouldn't be changed during the game.

# Frames Per Second: How many times the game updates and redraws the screen per second.
# A lower value like 10 means the game runs slower, which is fine for a turn-based game.
FPS = 10

# The width of the game window in pixels.
WINDOWWIDTH = 640
# The height of the game window in pixels.
WINDOWHEIGHT = 480

# The size of each square on the game board in pixels.
# Each tile (space) is 50x50 pixels.
SPACESIZE = 50

# The number of columns on the game board (horizontal).
BOARDWIDTH = 8
# The number of rows on the game board (vertical).
BOARDHEIGHT = 8

# Tile types: Constants representing the different states a board space can have.
# Represents a white game piece.
WHITE_TILE = 'WHITE_TILE'
# Represents a black game piece.
BLACK_TILE = 'BLACK_TILE'
# Represents an empty space on the board with no piece.
EMPTY_SPACE = 'EMPTY_SPACE'
# Represents a hint marker showing where the player can move.
HINT_TILE = 'HINT_TILE'

# The speed of animations, like flipping tiles. Higher values mean faster animations.
ANIMATIONSPEED = 25

# Margins: Calculate the space around the board to center it in the window.
# Horizontal margin: Space on the left and right of the board.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
# Vertical margin: Space on the top and bottom of the board.
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

# Colors: RGB tuples defining colors used in the game.
# RGB stands for Red, Green, Blue. Each value is from 0 to 255.
# Pure white color.
WHITE = (255, 255, 255)
# Pure black color.
BLACK = (0, 0, 0)
# A green color for backgrounds.
GREEN = (0, 155, 0)
# A bright blue color for text backgrounds.
BRIGHTBLUE = (0, 50, 255)
# A brown color for hints.
BROWN = (174, 94, 0)

# More color constants for text and UI elements.
# Background color for some text elements.
TEXTBGCOLOR1 = BRIGHTBLUE
# Background color for other text elements.
TEXTBGCOLOR2 = GREEN
# Color of the grid lines on the board.
GRIDLINECOLOR = BLACK
# Color of the text.
TEXTCOLOR = WHITE
# Color of the hint markers.
HINTCOLOR = BROWN

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
    # Try to get the path from PyInstaller's temporary directory.
    try:
        base_path = sys._MEIPASS
    # If not packaged, use the current working directory.
    except Exception:
        base_path = os.path.abspath(".")
    # Join the base path with the relative path to get the full path.
    return os.path.join(base_path, relative_path)

def main():
    """
    The main function that starts the game.
    
    This function initializes Pygame, sets up the game window, loads resources,
    and enters the main game loop. It keeps restarting the game until the player
    chooses not to play again.
    
    No parameters.
    No return value.
    """
    # Declare global variables that will be used throughout the game.
    # Global variables are accessible from any function in the file.
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE
    # - MAINCLOCK: Controls the game's frame rate.
    # - FONT: A small font for regular text.
    # - DISPLAYSURF: The main window surface where everything is drawn.
    # - BGIMAGE: The background image of the game board.
    # - BIGFONT: A larger font for headings.
    
    # Initialize all Pygame modules. This must be called before using any Pygame functions.
    # It sets up the display, sound, etc.
    pygame.init()
    
    # Create a Clock object to control the game's speed (frames per second).
    MAINCLOCK = pygame.time.Clock()
    
    # Create the game window with the specified width and height.
    # DISPLAYSURF is a Surface object representing the window.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    # Set the title of the window to 'flippy'.
    pygame.display.set_caption('flippy')
    
    # Load the game icon image from the file 'flippylogo.png'.
    # resource_path ensures it works whether running as script or executable.
    logo = pygame.image.load(resource_path('flippylogo.png'))
    
    # Set the window icon to the loaded logo image.
    pygame.display.set_icon(logo)
    
    # Load a font for small text. 'freesansbold.ttf' is a built-in Pygame font.
    # Size 16 pixels.
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    
    # Load a larger font for big text, size 32 pixels.
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
    
    # Load the board image.
    boardImage = pygame.image.load(resource_path('flippyboard.png'))
    # Resize the board image to fit the entire board area (8x8 spaces, each 50 pixels).
    # smoothscale makes the scaling look better.
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    
    # Get a Rect object for the board image, which has position and size info.
    boardImageRect = boardImage.get_rect()
    # Position the board image at the top-left of the board area (with margins).
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    
    # Load the background image.
    BGIMAGE = pygame.image.load(resource_path('flippybackground.png'))
    # Scale it to fill the entire window.
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    # Draw the board image onto the background image at the specified position.
    # This creates a composite background with the board on top.
    BGIMAGE.blit(boardImage, boardImageRect)
    
    # Main game loop: Keep playing games until the player quits.
    while True:
        # runGame() returns True if the player wants to play again, False otherwise.
        if runGame() == False:
            # If runGame returns False, exit the loop and end the program.
            break

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
    # Calculate the column: Subtract the left margin, then divide by space size.
    x = (mousex - XMARGIN) // SPACESIZE
    # Integer division (//) gives the grid position.
    # Calculate the row: Subtract the top margin, then divide by space size.
    y = (mousey - YMARGIN) // SPACESIZE
    # Check if the calculated position is within the board boundaries.
    if isOnBoard(x, y):
        # Return the board coordinates as a tuple.
        return (x, y)
    # If not on the board, return None.
    return None

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
    # Get the current scores from the board.
    scores = getScoreOfBoard(boardToDraw)
    # Get the player's score.
    playerScore = scores[playerTile]
    # Get the computer's score.
    computerScore = scores[computerTile]
    # Format the player's score text.
    playerText = f'Player: {playerScore}'
    # Format the computer's score text.
    computerText = f'Computer: {computerScore}'
    # Format the turn text, capitalizing the first letter.
    turnText = f'Turn: {turn.capitalize()}'
    
    # Render the player text into a Surface (image) with the font.
    playerSurf = FONT.render(playerText, True, TEXTCOLOR, TEXTBGCOLOR1)
    # True for anti-aliasing, TEXTCOLOR for text, TEXTBGCOLOR1 for background.
    # Get the Rect for positioning the text.
    playerRect = playerSurf.get_rect()
    # Position it near the top-right of the window.
    playerRect.topleft = (WINDOWWIDTH - 120, 70)
    
    # Similar for computer score, below the player score.
    computerSurf = FONT.render(computerText, True, TEXTCOLOR, TEXTBGCOLOR1)
    computerRect = computerSurf.get_rect()
    computerRect.topleft = (WINDOWWIDTH - 120, 90)
    
    # Turn text below the scores.
    turnSurf = FONT.render(turnText, True, TEXTCOLOR, TEXTBGCOLOR1)
    turnRect = turnSurf.get_rect()
    turnRect.topleft = (WINDOWWIDTH - 120, 110)
    
    # Draw the player text onto the display surface.
    DISPLAYSURF.blit(playerSurf, playerRect)
    # Draw the other texts.
    DISPLAYSURF.blit(computerSurf, computerRect)
    DISPLAYSURF.blit(turnSurf, turnRect)

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
    # Get a list of all valid moves for the computer.
    validMoves = getValidMoves(mainBoard, computerTile)
    # If there are valid moves,
    if validMoves:
        # Randomly pick one and return it.
        return random.choice(validMoves)
    # If no valid moves, return None.
    return None

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
    # Create a new empty board.
    mainBoard = getNewBoard()
    # Set up the starting position with 4 tiles in the center.
    resetBoard(mainBoard)
    # Initially, hints are not shown.
    showHints = False
    # Randomly decide who goes first.
    turn = random.choice(['computer', 'player'])
    # Count how many turns in a row have been passed (no moves).
    consecutivePasses = 0
    
    # Draw the initial board on the screen.
    drawBoard(mainBoard)
    # Ask the player to choose white or black, and assign tiles.
    playerTile, computerTile = enterPlayerTile()
    
    # Render the "New Game" button text.
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    # Position it at the top-right of the window.
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    # "Hints" button below "New Game".
    hintsRect.topright = (WINDOWWIDTH - 8, 40)
    
    # Main game loop for this game.
    while True:
        # It's the player's turn.
        if turn == 'player':
            # Get all valid moves for the player.
            validMoves = getValidMoves(mainBoard, playerTile)
            # If the player has moves,
            if validMoves:
                # Reset the pass counter.
                consecutivePasses = 0
                # Variable to store the player's chosen move.
                movexy = None
                # Loop until the player makes a valid move.
                while movexy == None:
                    if showHints:
                        # If hints are on, show the board with hint markers.
                        boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                    else:
                        # Otherwise, show the normal board.
                        boardToDraw = mainBoard
                    # Check if the player wants to quit.
                    checkForQuit()
                    # Process all pending events.
                    for event in pygame.event.get():
                        # If the mouse was clicked,
                        if event.type == MOUSEBUTTONUP:
                            # Get the mouse position.
                            mousex, mousey = event.pos
                            # If clicked on "New Game",
                            if newGameRect.collidepoint((mousex, mousey)):
                                # Start a new game.
                                return True
                            # If clicked on "Hints",
                            elif hintsRect.collidepoint((mousex, mousey)):
                                # Toggle hints on/off.
                                showHints = not showHints
                            # Convert mouse position to board coordinates.
                            movexy = getSpaceClicked(mousex, mousey)
                            # If clicked on board but not a valid move,
                            if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                                # Ignore it.
                                movexy = None
                    # Draw the board (with or without hints).
                    drawBoard(boardToDraw)
                    # Draw the scores and turn info.
                    drawInfo(boardToDraw, playerTile, computerTile, turn)
                    # Draw the "New Game" button.
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    # Draw the "Hints" button.
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    # Limit the frame rate.
                    MAINCLOCK.tick(FPS)
                    # Update the display to show the changes.
                    pygame.display.update()
                # Make the player's move, with animation.
                makeMove(mainBoard, playerTile, movexy[0], movexy[1], True, mainBoard)
                # Switch to computer's turn.
                turn = 'computer'
            # If player has no valid moves,
            else:
                # Increment pass counter.
                consecutivePasses += 1
                # Pass to computer.
                turn = 'computer'
        # It's the computer's turn.
        else:
            # Get computer's valid moves.
            validMoves = getValidMoves(mainBoard, computerTile)
            # If computer has moves,
            if validMoves:
                # Reset pass counter.
                consecutivePasses = 0
                # Draw the current board.
                drawBoard(mainBoard)
                # Draw info.
                drawInfo(mainBoard, playerTile, computerTile, turn)
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)
                # Update display.
                pygame.display.update()
                # Wait a random time (0.5 to 1.5 seconds) to simulate thinking.
                time.sleep(random.randint(5, 15) * 0.1)
                # Get the computer's move.
                x, y = getComputerMove(mainBoard, computerTile)
                # Make the move with animation.
                makeMove(mainBoard, computerTile, x, y, True, mainBoard)
                # Switch to player's turn.
                turn = 'player'
            # If computer has no moves,
            else:
                # Increment pass counter.
                consecutivePasses += 1
                # Pass to player.
                turn = 'player'
        
        # If both players passed in a row, game is over.
        if consecutivePasses >= 2:
            # Exit the game loop.
            break
    
    # Draw the final board.
    drawBoard(mainBoard)
    # Draw final scores.
    drawInfo(mainBoard, playerTile, computerTile, turn)
    
    # Get final scores.
    scores = getScoreOfBoard(mainBoard)
    if scores[playerTile] > scores[computerTile]:
        # Player won.
        text = 'You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile])
    elif scores[playerTile] < scores[computerTile]:
        # Player lost.
        text = 'You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile])
    else:
        # Tie game.
        text = 'The game was a tie!'
    
    # Render the result text.
    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    # Center it on the screen.
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    # Draw the result text.
    DISPLAYSURF.blit(textSurf, textRect)
    
    # "Play again?" below the result.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)
    
    # "Yes" button on the left.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)
    
    # "No" button on the right.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)
    
    # Loop to wait for player's choice to play again or quit.
    while True:
        # Check for quit events.
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # If clicked "Yes",
                if yesRect.collidepoint((mousex, mousey)):
                    # Play again.
                    return True
                # If clicked "No",
                elif noRect.collidepoint((mousex, mousey)):
                    # Quit.
                    return False
        # Draw the result text.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        # Draw the buttons.
        DISPLAYSURF.blit(noSurf, noRect)
        # Update display.
        pygame.display.update()
        # Limit frame rate.
        MAINCLOCK.tick(FPS)

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
    # Add margin, multiply by space size, add half space to get center.
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

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
        # New tile is white.
        additionalTileColor = WHITE
    else:
        # New tile is black.
        additionalTileColor = BLACK
    # Get pixel position of the new tile.
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    # Draw the new tile immediately.
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    # Update the screen.
    pygame.display.update()
    # Wait a bit.
    MAINCLOCK.tick(ANIMATIONSPEED)
    
    # Loop through color values from 0 to 255 in steps.
    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        # This creates the gradual color change.
        
        if tileColor == WHITE_TILE:
            # For white tiles, start from black (0) to white (255).
            color = tuple([rgbValues] * 3)
        elif tileColor == BLACK_TILE:
            # For black tiles, start from white (255) to black (0).
            color = tuple([255 - rgbValues] * 3)
        
        # For each tile to flip,
        for x, y in tilesToFlip:
            # Get its pixel position.
            centerx, centery = translateBoardToPixelCoord(x, y)
            # Draw it with the current color.
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        # Redraw the new tile.
        pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
        
        # Redraw the board background.
        drawBoard(mainBoard)
        # Update screen.
        pygame.display.update()
        # Control animation speed.
        MAINCLOCK.tick(ANIMATIONSPEED)
        # Allow quitting during animation.
        checkForQuit()

def drawBoard(board):
    """
    Draw the game board and all tiles on the screen.
    
    This draws the background, then places tiles and hints on top.
    
    Parameters:
    board: The 2D list representing the game board.
    
    No return value.
    """
    # Draw the background image (which includes the board grid).
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())
    # Loop through each column.
    for x in range(BOARDWIDTH):
        # Loop through each row.
        for y in range(BOARDHEIGHT):
            # Get the pixel center of this space.
            centerx, centery = translateBoardToPixelCoord(x, y)
            # If there's a tile here,
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    # Set color to white.
                    tileColor = WHITE
                else:
                    # Set color to black.
                    tileColor = BLACK
                # Draw a circle for the tile.
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
            # If this is a hint,
            if board[x][y] == HINT_TILE:
                # Draw a small square hint marker.
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))

    # Draw the vertical grid lines.
    for x in range(BOARDWIDTH + 1):
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        # Draw a vertical line.
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    # Draw the horizontal grid lines.
    for y in range(BOARDHEIGHT + 1):
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        # Draw a horizontal line.
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

def getNewBoard():
    """
    Create a new empty game board.
    
    Returns a 2D list with BOARDWIDTH columns and BOARDHEIGHT rows,
    all initialized to EMPTY_SPACE.
    
    No parameters.
    
    Returns:
    list: 2D list representing the board.
    """
    # Start with empty list.
    board = []
    # For each column,
    for i in range(BOARDWIDTH):
        # Add a row of empty spaces.
        board.append([EMPTY_SPACE] * BOARDHEIGHT)
    # Return the new board.
    return board

def resetBoard(board):
    """
    Reset the board to the starting position.
    
    Clears all spaces and places the initial 4 tiles in the center.
    
    Parameters:
    board: The board to reset (modified in place).
    
    No return value.
    """
    # Loop through columns.
    for x in range(BOARDWIDTH):
        # Loop through rows.
        for y in range(BOARDHEIGHT):
            # Set to empty.
            board[x][y] = EMPTY_SPACE
    # Place the starting tiles:
    # Standard Othello starting position.
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE

def getScoreOfBoard(board):
    """
    Count the number of white and black tiles on the board.
    
    Parameters:
    board: The game board.
    
    Returns:
    dict: {'WHITE_TILE': count, 'BLACK_TILE': count}
    """
    # White score.
    xscore = 0
    # Black score.
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                # Count white tiles.
                xscore += 1
            if board[x][y] == BLACK_TILE:
                # Count black tiles.
                oscore += 1
    # Return as dictionary.
    return {WHITE_TILE:xscore, BLACK_TILE:oscore}

def enterPlayerTile():
    """
    Let the player choose their tile color.
    
    Displays options for white or black, waits for click.
    
    No parameters.
    
    Returns:
    tuple: (playerTile, computerTile) as strings.
    """
    # Render the question text.
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    # Center it.
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    # "White" option.
    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    # Position left.
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)
    # "Black" option.
    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    # Position right.
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)
    # Loop until choice made.
    while True:
        # Check for quit.
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # Chose white.
                if xRect.collidepoint((mousex, mousey)):
                    # Player white, computer black.
                    return [WHITE_TILE, BLACK_TILE]
                # Chose black.
                elif oRect.collidepoint((mousex, mousey)):
                    # Player black, computer white.
                    return [BLACK_TILE, WHITE_TILE]
        # Draw question.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        # Draw options.
        DISPLAYSURF.blit(oSurf, oRect)
        # Update screen.
        pygame.display.update()
        # Limit frame rate.
        MAINCLOCK.tick(FPS)

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
    # Check if move is valid and get tiles to flip.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    # If invalid,
    if tilesToFlip == False:
        # Return False.
        return False
    # Place the tile.
    board[xstart][ystart] = tile
    # If real move,
    if realMove:
        # Animate the flip.
        animateTileChange(tilesToFlip, tile, (xstart, ystart), mainBoard if mainBoard is not None else board)
        # Then actually flip the tiles.
        for x, y in tilesToFlip:
            board[x][y] = tile
    # Return success.
    return True

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
    # If space not empty or out of bounds,
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        # Invalid.
        return False
    # Temporarily place the tile.
    board[xstart][ystart] = tile
    # Get opponent's color.
    otherTile = getOpponentTile(tile)
    # List to collect tiles to flip.
    tilesToFlip = []
    # Check all 8 directions.
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        # Start from the placed tile.
        x, y = xstart, ystart
        x += xdirection
        # Move in this direction.
        y += ydirection
        # If next space has opponent tile,
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            # Continue in direction.
            y += ydirection
            # If went off board,
            if not isOnBoard(x, y):
                # Skip this direction.
                continue
            # While still opponent tiles,
            while board[x][y] == otherTile:
                x += xdirection
                # Keep going.
                y += ydirection
                # If off board,
                if not isOnBoard(x, y):
                    # Stop.
                    break
            # If ended off board,
            if not isOnBoard(x, y):
                # Skip.
                continue
            # If ended on own tile,
            if board[x][y] == tile:
                # Backtrack and collect tiles to flip.
                while True:
                    x -= xdirection
                    # Move back.
                    y -= ydirection
                    # Until back at start,
                    if x == xstart and y == ystart:
                        # Done.
                        break
                    # Add to flip list.
                    tilesToFlip.append([x, y])
    # Remove temporary tile.
    board[xstart][ystart] = EMPTY_SPACE
    # If no tiles to flip,
    if len(tilesToFlip) == 0:
        # Invalid move.
        return False
    # Return the list of tiles to flip.
    return tilesToFlip

def isOnBoard(x, y):
    """
    Check if coordinates are within the board boundaries.
    
    Parameters:
    x (int): Column.
    y (int): Row.
    
    Returns:
    bool: True if on board, False otherwise.
    """
    # Check if x and y are between 0 and board size - 1.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT

def getBoardWithValidMoves(board, tile):
    """
    Create a copy of the board with hint tiles for valid moves.
    
    Parameters:
    board: The original board.
    tile (str): The tile color to check moves for.
    
    Returns:
    list: A new board with HINT_TILE in valid move positions.
    """
    # Make a deep copy of the board.
    dupeBoard = copy.deepcopy(board)
    # For each valid move,
    for x, y in getValidMoves(dupeBoard, tile):
        # Place a hint.
        dupeBoard[x][y] = HINT_TILE
    # Return the modified copy.
    return dupeBoard

def getValidMoves(board, tile):
    """
    Get a list of all valid moves for a tile color.
    
    Parameters:
    board: The game board.
    tile (str): The tile color.
    
    Returns:
    list: List of (x, y) tuples for valid moves.
    """
    # Start empty list.
    validMoves = []
    # Check every column.
    for x in range(BOARDWIDTH):
        # Check every row.
        for y in range(BOARDHEIGHT):
            # If move is valid,
            if isValidMove(board, tile, x, y) != False:
                # Add to list.
                validMoves.append((x, y))
    # Return the list.
    return validMoves

def getOpponentTile(tile):
    """
    Get the opponent's tile color.
    
    Parameters:
    tile (str): A tile color.
    
    Returns:
    str: The opposite color.
    """
    if tile == WHITE_TILE:
        # Opposite of white is black.
        return BLACK_TILE
    else:
        # Opposite of black is white.
        return WHITE_TILE

def checkForQuit():
    """
    Check for quit events and handle them.
    
    If the user closes the window or presses Escape, quit the game.
    
    No parameters.
    No return value.
    """
    # If window close event,
    for event in pygame.event.get(QUIT):
        # Quit.
        terminate()
    # If key released,
    for event in pygame.event.get(KEYUP):
        # If Escape key,
        if event.key == K_ESCAPE:
            # Quit.
            terminate()
        else:
            # Otherwise, put the event back for other handlers.
            pygame.event.post(event)

def terminate():
    """
    Clean up and exit the program.
    
    Quits Pygame and exits the Python program.
    
    No parameters.
    No return value.
    """
    # Shut down Pygame.
    pygame.quit()
    # Exit the program.
    sys.exit()

# If this script is run directly (not imported),
if __name__ == '__main__':
    # Start the game.
    main()
