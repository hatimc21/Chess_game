#!/usr/bin/env python3
"""
Script to set up the project structure for the chess game.
"""

import os
import sys

def create_directory(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def create_empty_file(filepath):
    """Create an empty file if it doesn't exist."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            pass
        print(f"Created empty file: {filepath}")
    else:
        print(f"File already exists: {filepath}")

def setup_project():
    """Set up the chess game project structure."""
    print("Setting up chess game project structure...")
    
    # Create main directories
    directories = [
        "assets",
        "assets/pieces",
        "chess_engine",
        "gui",
        "ai",
        "saves"
    ]
    
    for directory in directories:
        create_directory(directory)
    
    # Create __init__.py files
    init_files = [
        "chess_engine/__init__.py",
        "gui/__init__.py",
        "ai/__init__.py"
    ]
    
    for init_file in init_files:
        create_empty_file(init_file)
    
    print("\nProject structure setup complete!")
    print("\nNext steps:")
    print("1. Create a virtual environment:")
    print("   python -m venv venv")
    print("2. Activate the virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Install the required packages:")
    print("   pip install -r requirements.txt")
    print("4. Generate chess piece sprites:")
    print("   python create_sprites.py")
    print("5. Run the game:")
    print("   python main.py")

if __name__ == "__main__":
    setup_project()