# Chess Game Setup Instructions

## Setting Up a Virtual Environment

### For Windows:
```bash
# Navigate to your project directory
cd path/to/chess_game

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### For macOS/Linux:
```bash
# Navigate to your project directory
cd path/to/chess_game

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

Make sure your project has the following directory structure:
```
chess_game/
├── assets/
│   └── pieces/         # Place chess piece sprites here
├── ai/
│   ├── __init__.py
│   ├── features.py
│   ├── model.py
│   └── training.py
├── chess_engine/
│   ├── __init__.py
│   ├── board.py
│   ├── pieces.py
│   └── rules.py
├── gui/
│   ├── __init__.py
│   ├── board_display.py
│   ├── piece_sprites.py
│   └── game_screen.py
├── saves/              # Will be created automatically
├── main.py
├── requirements.txt
└── venv/               # Virtual environment directory
```

## Running the Game

After setting up the virtual environment and installing dependencies:

```bash
# Ensure the virtual environment is activated
# Then run the game
python main.py
```

## Additional Notes

- The game will create placeholder sprites if no actual sprite images are found
- You can save and load games from the in-game menu
- AI difficulty can be adjusted in the options menu