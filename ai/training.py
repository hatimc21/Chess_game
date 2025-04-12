# ai/training.py
"""
This file contains functions for training the chess AI model.
"""

import os
import pickle
import random
import numpy as np
from ai.features import extract_features
from ai.model import ChessAI
from chess_engine.board import Board


def generate_training_data(num_positions=10000, moves_per_game=30):
    """
    Generate training data from random games.
    
    Args:
        num_positions (int): Number of positions to generate
        moves_per_game (int): Maximum number of moves per game
        
    Returns:
        tuple: (positions, scores) lists of board positions and their evaluations
    """
    positions = []
    scores = []
    
    # Initialize a simple evaluator
    evaluator = ChessAI(difficulty=1)
    
    games_needed = num_positions // moves_per_game + 1
    
    for game in range(games_needed):
        board = Board()
        
        # Play a random game
        for move_num in range(moves_per_game):
            # Get valid moves
            valid_moves = board.get_valid_moves()
            
            if not valid_moves or board.checkmate or board.stalemate:
                break
            
            # Choose a random move
            move = random.choice(valid_moves)
            
            # Save the position before the move
            positions.append(board)
            
            # Evaluate position
            score = evaluator._evaluate_material(board)
            scores.append(score)
            
            # Make the move
            board.make_move(move)
    
    # Trim to requested size
    positions = positions[:num_positions]
    scores = scores[:num_positions]
    
    return positions, scores


def train_from_pgn(pgn_file, model_file='ai_model.pkl', num_games=1000):
    """
    Train the AI model from a PGN file of chess games.
    
    Args:
        pgn_file (str): Path to PGN file
        model_file (str): Path to save the trained model
        num_games (int): Number of games to use
        
    Note: This requires the python-chess library
    """
    try:
        import chess.pgn
    except ImportError:
        print("This function requires the python-chess library.")
        print("Please install it using: pip install python-chess")
        return
    
    # Initialize lists for positions and scores
    positions = []
    scores = []
    
    # Open PGN file
    with open(pgn_file) as f:
        game_count = 0
        
        # Process games
        while game_count < num_games:
            # Read game
            game = chess.pgn.read_game(f)
            
            if game is None:
                break  # End of file
            
            # Get result
            result = game.headers.get("Result", "*")
            
            # Skip games without a clear result
            if result not in ["1-0", "0-1", "1/2-1/2"]:
                continue
            
            # Convert result to score
            final_score = 1.0 if result == "1-0" else -1.0 if result == "0-1" else 0.0
            
            # Track board state
            board = chess.Board()
            
            # Process moves
            for move in game.mainline_moves():
                # Make the move
                board.push(move)
                
                # Skip early game positions
                if board.fullmove_number < 5:
                    continue
                
                # Convert board to our format
                our_board = _convert_board(board)
                
                # Skip invalid positions
                if our_board is None:
                    continue
                
                positions.append(our_board)
                
                # Calculate score based on final result, weighted by move number
                # Later moves are more indicative of final result
                move_weight = min(1.0, board.fullmove_number / 40.0)
                score = final_score * move_weight
                scores.append(score)
            
            game_count += 1
            if game_count % 100 == 0:
                print(f"Processed {game_count} games")
    
    # Train the AI
    ai = ChessAI(difficulty=5)
    ai.train(positions, scores)
    
    # Save the model
    save_model(ai, model_file)
    
    print(f"Model trained on {len(positions)} positions and saved to {model_file}")


def _convert_board(chess_board):
    """
    Convert a python-chess board to our board format.
    
    Args:
        chess_board: python-chess Board object
        
    Returns:
        Board: Our Board object, or None if conversion failed
    """
    try:
        # Get FEN representation
        fen = chess_board.fen()
        
        # Create our board
        our_board = Board()
        
        # Load from FEN
        our_board.load_from_fen(fen)
        
        return our_board
    except Exception as e:
        print(f"Error converting board: {e}")
        return None


def save_model(ai, filename='ai_model.pkl'):
    """
    Save the trained AI model to a file.
    
    Args:
        ai (ChessAI): The trained AI object
        filename (str): File path to save to
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    
    with open(filename, 'wb') as f:
        pickle.dump(ai, f)


def load_model(filename='ai_model.pkl'):
    """
    Load a trained AI model from a file.
    
    Args:
        filename (str): File path to load from
        
    Returns:
        ChessAI: The loaded AI object, or None if loading failed
    """
    try:
        with open(filename, 'rb') as f:
            ai = pickle.load(f)
        return ai
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def generate_simple_dataset():
    """
    Generate a simple dataset for initial training.
    
    Returns:
        tuple: (positions, scores) lists of board positions and their evaluations
    """
    # Create 100 random positions
    positions, material_scores = generate_training_data(num_positions=100, moves_per_game=20)
    
    # Initialize lists for feature vectors and scores
    X = []
    y = []
    
    # Extract features and prepare dataset
    for i, board in enumerate(positions):
        # Extract features
        features = extract_features(board)
        X.append(features)
        
        # Use material score as target
        score = material_scores[i]
        y.append(score)
    
    return np.array(X), np.array(y)


def train_simple_model(model_file='ai_model.pkl'):
    """
    Train a simple model for initial use.
    
    Args:
        model_file (str): File path to save the model
    """
    from sklearn.ensemble import RandomForestRegressor
    
    # Generate dataset
    X, y = generate_simple_dataset()
    
    # Create model
    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=10,
        random_state=42
    )
    
    # Train model
    model.fit(X, y)
    
    # Create AI object
    ai = ChessAI(difficulty=3)
    ai.initialize_model()
    ai.model = model
    
    # Save model
    save_model(ai, model_file)
    
    print(f"Simple model trained and saved to {model_file}")


if __name__ == "__main__":
    # Generate a simple model when running this script directly
    train_simple_model()