"""
This file contains the ChessAI class for the chess game.
"""

import random

class ChessAI:
    """Class for chess AI."""
    
    def __init__(self, difficulty=3):
        """
        Initialize the chess AI.
        
        Args:
            difficulty (int): AI difficulty level (1-5)
        """
        self.difficulty = difficulty
        self.search_depth = max(1, min(5, difficulty))
        
        # Piece values for evaluation
        self.piece_values = {
            'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
            'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900
        }
        
        # Position values for evaluation
        self.position_values = {
            'P': [  # Pawn
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'N': [  # Knight
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            'B': [  # Bishop
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            'R': [  # Rook
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]
            ],
            'Q': [  # Queen
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],
            'K': [  # King (middlegame)
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20]
            ],
            'K_endgame': [  # King (endgame)
                [-50, -40, -30, -20, -20, -30, -40, -50],
                [-30, -20, -10, 0, 0, -10, -20, -30],
                [-30, -10, 20, 30, 30, 20, -10, -30],
                [-30, -10, 30, 40, 40, 30, -10, -30],
                [-30, -10, 30, 40, 40, 30, -10, -30],
                [-30, -10, 20, 30, 30, 20, -10, -30],
                [-30, -30, 0, 0, 0, 0, -30, -30],
                [-50, -30, -30, -30, -30, -30, -30, -50]
            ]
        }
        
        # Mirror position values for black pieces
        for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
            self.position_values[piece] = [[-x for x in row] for row in self.position_values[piece.upper()]][::-1]
    
    def find_best_move(self, board):
        """
        Find the best move for the current position.
        
        Args:
            board: The chess board
            
        Returns:
            Move: The best move
        """
        # Get all valid moves
        valid_moves = board.get_all_valid_moves()
        
        if not valid_moves:
            return None
        
        # For very low difficulty, just return a random move
        if self.difficulty == 1:
            return random.choice(valid_moves)
        
        # For higher difficulties, use minimax with alpha-beta pruning
        best_score = float('-inf')
        best_move = None
        
        # Randomize move order for more variety
        random.shuffle(valid_moves)
        
        # Alpha-beta pruning bounds
        alpha = float('-inf')
        beta = float('inf')
        
        for move in valid_moves:
            # Make the move
            board.make_move(move)
            
            # Evaluate the position
            score = -self._minimax(board, self.search_depth - 1, -beta, -alpha, not board.white_to_move)
            
            # Undo the move
            board.undo_move()
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = move
            
            # Update alpha
            alpha = max(alpha, best_score)
        
        return best_move
    
    def _minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The chess board
            depth (int): Search depth
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): Whether the current player is maximizing
            
        Returns:
            float: Evaluation score
        """
        # Base case: reached maximum depth or game over
        if depth == 0 or board.checkmate or board.stalemate:
            return self._evaluate_board(board)
        
        # Get all valid moves
        valid_moves = board.get_all_valid_moves()
        
        if maximizing_player:
            max_score = float('-inf')
            
            for move in valid_moves:
                # Make the move
                board.make_move(move)
                
                # Recursively evaluate the position
                score = self._minimax(board, depth - 1, alpha, beta, False)
                
                # Undo the move
                board.undo_move()
                
                # Update max score
                max_score = max(max_score, score)
                
                # Update alpha
                alpha = max(alpha, max_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return max_score
        else:
            min_score = float('inf')
            
            for move in valid_moves:
                # Make the move
                board.make_move(move)
                
                # Recursively evaluate the position
                score = self._minimax(board, depth - 1, alpha, beta, True)
                
                # Undo the move
                board.undo_move()
                
                # Update min score
                min_score = min(min_score, score)
                
                # Update beta
                beta = min(beta, min_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return min_score
    
    def _evaluate_board(self, board):
        """
        Evaluate the board position.
        
        Args:
            board: The chess board
            
        Returns:
            float: Evaluation score (positive for white advantage, negative for black)
        """
        # Check for checkmate
        if board.checkmate:
            # If white is checkmated, return a large negative score
            if board.white_to_move:
                return -10000
            # If black is checkmated, return a large positive score
            else:
                return 10000
        
        # Check for stalemate
        if board.stalemate:
            return 0
        
        # Material evaluation
        material_score = self._evaluate_material(board)
        
        # Position evaluation
        position_score = self._evaluate_position(board)
        
        # Mobility evaluation (number of legal moves)
        mobility_score = self._evaluate_mobility(board)
        
        # Combine scores
        total_score = material_score + position_score + mobility_score
        
        # Return score from white's perspective
        return total_score if board.white_to_move else -total_score
    
    def _evaluate_material(self, board):
        """
        Evaluate material balance.
        
        Args:
            board: The chess board
            
        Returns:
            float: Material score
        """
        score = 0
        
        # Sum up piece values
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece:
                    score += self.piece_values.get(piece.symbol, 0)
        
        return score
    
    def _evaluate_position(self, board):
        """
        Evaluate piece positions.
        
        Args:
            board: The chess board
            
        Returns:
            float: Position score
        """
        score = 0
        
        # Check if we're in endgame (few pieces left)
        is_endgame = self._is_endgame(board)
        
        # Sum up position values
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece:
                    symbol = piece.symbol
                    
                    # Use endgame table for king in endgame
                    if symbol.upper() == 'K' and is_endgame:
                        if symbol == 'K':
                            score += self.position_values['K_endgame'][row][col]
                        else:
                            score += self.position_values['k_endgame'][row][col]
                    else:
                        # Use regular position tables
                        position_table = self.position_values.get(symbol)
                        if position_table:
                            score += position_table[row][col]
        
        return score * 0.1  # Scale down position score
    
    def _evaluate_mobility(self, board):
        """
        Evaluate piece mobility (number of legal moves).
        
        Args:
            board: The chess board
            
        Returns:
            float: Mobility score
        """
        # Save current turn
        current_turn = board.white_to_move
        
        # Count white moves
        board.white_to_move = True
        white_moves = len(board.get_all_valid_moves())
        
        # Count black moves
        board.white_to_move = False
        black_moves = len(board.get_all_valid_moves())
        
        # Restore current turn
        board.white_to_move = current_turn
        
        # Return mobility difference
        return (white_moves - black_moves) * 0.1  # Scale down mobility score
    
    def _is_endgame(self, board):
        """
        Check if the position is in endgame.
        
        Args:
            board: The chess board
            
        Returns:
            bool: Whether the position is in endgame
        """
        # Count material
        white_material = 0
        black_material = 0
        
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece:
                    if piece.symbol.upper() != 'K':  # Exclude kings
                        if piece.is_white():
                            white_material += abs(self.piece_values.get(piece.symbol, 0))
                        else:
                            black_material += abs(self.piece_values.get(piece.symbol, 0))
        
        # Endgame if both sides have less than a queen + rook worth of material
        return white_material < 140 and black_material < 140