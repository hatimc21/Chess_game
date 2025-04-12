# Chess Game

A fully-featured chess game implemented in Python using Pygame. This application provides a complete chess experience with a graphical user interface, standard chess rules, and various gameplay features.





## Features

- Complete implementation of chess rules
- Graphical user interface with draggable pieces
- Move validation and highlighting of possible moves
- Special moves: castling, en passant, and pawn promotion
- Move history panel
- Game state tracking (check, checkmate, stalemate)
- Undo move functionality
- Save and load games


## Installation

### Prerequisites

- Python 3.8 or higher
- Pygame library


### Setting Up a Virtual Environment

#### For Windows:

```shellscript
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### For macOS/Linux:

```shellscript
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

After installing the dependencies, you can run the game with:

```shellscript
python main.py
```

### Game Controls

- **Mouse Click**: Select and move pieces
- **New Game Button**: Start a new game
- **Undo Button**: Undo the last move
- **Pawn Promotion**: When a pawn reaches the opposite end of the board, a menu will appear allowing you to choose which piece to promote to


## Project Structure

```plaintext
Chess_game/
├── assets/
│   └── pieces/       # Chess piece images
├── chess_engine/     # Core chess logic
│   ├── __init__.py
│   └── board.py      # Board representation and move validation
├── gui/              # User interface components
│   ├── __init__.py
│   ├── board_display.py  # Board rendering
│   └── ui_components.py  # UI elements (buttons, panels, etc.)
├── saves/            # Saved game files
├── ai/               # AI opponent (if implemented)
├── main.py           # Main entry point
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

## Technical Details

### Chess Engine

The chess engine handles:

- Board representation
- Move validation
- Special moves (castling, en passant, pawn promotion)
- Check and checkmate detection
- Game state tracking


### GUI

The graphical interface provides:

- Visual representation of the chess board and pieces
- Interactive elements for game control
- Move highlighting
- Game information display


## Future Enhancements

- AI opponent with adjustable difficulty levels
- Network play functionality
- Opening book and endgame database
- Game analysis tools
- Customizable themes and piece sets


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Chess piece images are from [source/attribution]
- Thanks to the Pygame community for their excellent documentation and support


---

Feel free to contribute to this project by submitting issues or pull requests!
