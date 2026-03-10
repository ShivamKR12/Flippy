# Flippy

A classic Reversi (Othello) game implemented in Python using Pygame-CE. Play against the computer with a simple AI opponent.

## Features

- Play as White or Black tiles
- Computer opponent with random move selection
- Hint system to show valid moves
- Smooth tile flip animations
- Score display and turn indicator
- New game option
- Standalone executable available

## Requirements

- Python 3.6+ (for source code)
- Pygame-CE library (`pip install pygame-ce`)
- For executable: No additional requirements needed

## Installation

### Option 1: Run from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/ShivamKR12/flippy.git
   cd flippy
   ```

2. Install dependencies:
   ```bash
   pip install pygame-ce
   ```

3. Run the game:
   ```bash
   python flippy.py
   ```

### Option 2: Use Standalone Executable
Download the executable from the [Releases](https://github.com/ShivamKR12/flippy/releases) page:

No installation required - just run the executable.

## How to Play

1. Choose your tile color (White or Black)
2. Click on the board to place your tile
3. Valid moves are highlighted when hints are enabled
4. The goal is to have more tiles of your color than the opponent
5. Game ends when neither player can make a valid move

### Controls

- **Mouse**: Click to place tiles or interact with buttons
- **ESC**: Quit the game
- **Hints Button**: Toggle valid move highlights
- **New Game Button**: Start a new game

## Game Rules

Reversi is played on an 8x8 board. Players take turns placing tiles that flip opponent tiles between their own. A move is valid if it flips at least one opponent tile. The game follows standard Othello rules with proper pass mechanics.

## Files

- `flippy.py` - Main game source code
- `flippyboard.png` - Board background image
- `flippybackground.png` - Game background image

## Credits

- Original game logic based on classic Reversi/Othello
- Built with Pygame-CE
- Font: FreeSansBold (system font)

## License

This project is open source. Feel free to modify and distribute.
