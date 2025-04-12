# ai/model.py
"""
This file contains the ChessAI class for implementing the Random Forest-based chess AI.
"""

import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from ai.features import extract_features


class ChessAI:
    """
    Class for chess AI using Random Forest to evaluate positions and select moves.
    """
    
    def __init__(self, difficulty=3):
        """
        Initialize the chess AI.
        
        Args:
            difficulty (int): Difficulty level (1-5)
        """
        self.difficulty = difficulty
        self.model = None
        self.initialized = False
        
        # For search
        self.search_depth = max(1, min(5, difficulty))
        self.nodes_evaluated = 0
        
        # Piece values for simple evaluation
        self.piece_values = {
            'P': 100,  # Pawn
            'N': 320,  # Knight
            'B': 330,  # Bishop
            'R': 500,  # Rook
            'Q': 900,  # Queen
            'K': 20000  # King - very high value to ensure it's never sacrificed
        }
    
    def initialize_model(self):
        """Initialize the Random Forest model."""
        if not self.initialized:
            # Create a new model
            self.model = RandomForestRegressor(
                n_estimators=100,  # Number of trees
                max_depth=10,      # Maximum depth of trees
                random_state=42    # For reproducibility
            )
            self.initialized = True
    
    def train(self, positions, scores):
        """
        Train the model on a dataset of positions and their evaluations.
        
        Args:
            positions (list): List of board positions (boards)
            scores (list): Corresponding evaluation scores
        """
        self.initialize_model()
        
        # Extract features from positions
        X = np.array([extract_features(board) for board in positions])
        y = np.array(scores)
        
        # Train the model
        self.model.fit(X, y)
    
    def evaluate_position(self, board):
        """
        Evaluate a chess position.
        
        Args:
            board: The chess board object
            
        Returns:
            float: Evaluation score (positive for white advantage, negative for black)
        """
        # Use the trained model if available
        if self.initialized and self.model is not None:
            # Extract features
            features = extract_features(board)
            
            # Predict evaluation
            return self.model.predict([features])[0]
        else:
            # Fall back to simple material counting if model not trained
            return self._evaluate_material(board)
    
    def _evaluate_material(self, board):
        """
        Simple material counting evaluation.
        
        Args:
            board: The chess board object
            
        Returns:
            float: Material advantage (positive for white advantage)
        """
        white_material = 0
        black_material = 0
        
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece is None:
                    continue
                
                value = self.piece_values[piece.piece_type]
                
                if piece.is_white:
                    white_material += value
                else:
                    black_material += value
        
        return white_material - black_material
    
    def choose_move(self, board):
        """
        Choose the best move for the current player.
        
        Args:
            board: The chess board object
            
        Returns:
            Move: The chosen move
        """
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            return None  # No valid moves
        
        # If playing randomly (difficulty 1), just return a random move
        if self.difficulty == 1:
            return random.choice(valid_moves)
        
        # For higher difficulties, use search
        best_move = None
        best_score = float('-inf') if board.white_to_move else float('inf')
        
        # Reset node count
        self.nodes_evaluated = 0
        
        # Search for the best move
        alpha = float('-inf')
        beta = float('inf')
        
        for move in valid_moves:
            # Make the move on the board
            board.make_move(move)
            
            # Evaluate the resulting position
            if self.difficulty >= 3:
                # Use minimax with alpha-beta pruning for higher difficulties
                score = self._minimax(
                    board, 
                    self.search_depth - 1, 
                    alpha, 
                    beta, 
                    not board.white_to_move
                )
            else:
                # Just evaluate the position for low difficulty
                score = self.evaluate_position(board)
                
                # Flip score for black
                if not board.white_to_move:
                    score = -score
            
            # Undo the move
            board.undo_move()
            
            # Update best move
            if board.white_to_move:
                if score > best_score:
                    best_score = score
                    best_move = move
                    # Update alpha
                    alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                    # Update beta
                    beta = min(beta, best_score)
        
        # If difficulty is less than max, occasionally choose a random move
        if self.difficulty < 5 and random.random() < 0.2 - (self.difficulty * 0.04):
            return random.choice(valid_moves)
        
        return best_move
    
    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning for position evaluation.
        
        Args:
            board: The chess board object
            depth (int): Current search depth
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            is_maximizing (bool): Whether to maximize or minimize
            
        Returns:
            float: Best score for the position
        """
        self.nodes_evaluated += 1
        
        # Check game end conditions
        if board.checkmate:
            return -10000 if is_maximizing else 10000
        elif board.stalemate:
            return 0
        
        # If depth reached or too many nodes evaluated, evaluate the position
        if depth == 0 or self.nodes_evaluated > 10000:
            score = self.evaluate_position(board)
            return score if is_maximizing else -score
        
        valid_moves = board.get_valid_moves()
        
        if is_maximizing:
            best_score = float('-inf')
            for move in valid_moves:
                board.make_move(move)
                score = self._minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return best_score
        else:
            best_score = float('inf')
            for move in valid_moves:
                board.make_move(move)
                score = self._minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return best_score