# chess_engine/pieces.py
"""
This file contains the classes for all chess pieces.
Each piece knows its position and how it can move on the board.
"""

class Piece:
    """Base class for all chess pieces."""
    
    def __init__(self, row, col, is_white):
        """
        Initialize a chess piece.
        
        Args:
            row (int): The row position (0-7)
            col (int): The column position (0-7)
            is_white (bool): True if the piece is white, False if black
        """
        self.row = row
        self.col = col
        self.is_white = is_white
        self.piece_type = None  # To be set by subclasses
        self.symbol = None  # FEN symbol to be set by subclasses
        self.moved = False  # Track if the piece has moved (for castling, pawn double move)
    
    def get_valid_moves(self, board):
        """
        Get all valid moves for this piece on the current board.
        To be implemented by subclasses.
        
        Args:
            board: The current chess board
            
        Returns:
            list: List of valid Move objects
        """
        pass
    
    def __repr__(self):
        """String representation of the piece."""
        color = "White" if self.is_white else "Black"
        return f"{color} {self.piece_type} at {self.get_position()}"
    
    def get_position(self):
        """Get algebraic notation for current position."""
        files = "abcdefgh"
        ranks = "87654321"
        return files[self.col] + ranks[self.row]


class Pawn(Piece):
    """Pawn chess piece."""
    
    def __init__(self, row, col, is_white):
        """Initialize a pawn."""
        super().__init__(row, col, is_white)
        self.piece_type = 'P'
        self.symbol = 'P' if is_white else 'p'
    
    def get_valid_moves(self, board):
        """Get all valid moves for a pawn."""
        from chess_engine.board import Move
        
        moves = []
        direction = -1 if self.is_white else 1  # White pawns move up (decreasing row), black pawns move down
        
        # One square forward
        if 0 <= self.row + direction < 8 and board.squares[self.row + direction][self.col] is None:
            moves.append(Move((self.row, self.col), (self.row + direction, self.col), board))
            
            # Two squares forward from starting position
            if ((self.is_white and self.row == 6) or (not self.is_white and self.row == 1)) and \
               board.squares[self.row + 2 * direction][self.col] is None:
                moves.append(Move((self.row, self.col), (self.row + 2 * direction, self.col), board))
        
        # Captures to the left
        if 0 <= self.row + direction < 8 and 0 <= self.col - 1 < 8:
            # Normal capture
            if board.squares[self.row + direction][self.col - 1] is not None and \
               board.squares[self.row + direction][self.col - 1].is_white != self.is_white:
                moves.append(Move((self.row, self.col), (self.row + direction, self.col - 1), board))
            
            # En passant capture
            elif (self.row + direction, self.col - 1) == board.en_passant_possible:
                moves.append(Move(
                    (self.row, self.col), 
                    (self.row + direction, self.col - 1), 
                    board, 
                    is_en_passant_move=True
                ))
        
        # Captures to the right
        if 0 <= self.row + direction < 8 and 0 <= self.col + 1 < 8:
            # Normal capture
            if board.squares[self.row + direction][self.col + 1] is not None and \
               board.squares[self.row + direction][self.col + 1].is_white != self.is_white:
                moves.append(Move((self.row, self.col), (self.row + direction, self.col + 1), board))
            
            # En passant capture
            elif (self.row + direction, self.col + 1) == board.en_passant_possible:
                moves.append(Move(
                    (self.row, self.col), 
                    (self.row + direction, self.col + 1), 
                    board, 
                    is_en_passant_move=True
                ))
        
        return moves


class Knight(Piece):
    """Knight chess piece."""
    
    def __init__(self, row, col, is_white):
        """Initialize a knight."""
        super().__init__(row, col, is_white)
        self.piece_type = 'N'
        self.symbol = 'N' if is_white else 'n'
    
    def get_valid_moves(self, board):
        """Get all valid moves for a knight."""
        from chess_engine.board import Move
        
        moves = []
        # Knight move offsets: all possible L shapes
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            end_row, end_col = self.row + dr, self.col + dc
            
            # Check if the move is on the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board.squares[end_row][end_col]
                
                # Empty square or opponent's piece
                if end_piece is None or end_piece.is_white != self.is_white:
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
        
        return moves


class Bishop(Piece):
    """Bishop chess piece."""
    
    def __init__(self, row, col, is_white):
        """Initialize a bishop."""
        super().__init__(row, col, is_white)
        self.piece_type = 'B'
        self.symbol = 'B' if is_white else 'b'
    
    def get_valid_moves(self, board):
        """Get all valid moves for a bishop."""
        from chess_engine.board import Move
        
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        
        for dr, dc in directions:
            for i in range(1, 8):  # Maximum 7 steps in any direction
                end_row, end_col = self.row + i * dr, self.col + i * dc
                
                # Check if we're still on the board
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                
                end_piece = board.squares[end_row][end_col]
                
                if end_piece is None:
                    # Empty square
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
                elif end_piece.is_white != self.is_white:
                    # Capture opponent's piece
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
                    break
                else:
                    # Own piece, can't move further
                    break
        
        return moves


class Rook(Piece):
    """Rook chess piece."""
    
    def __init__(self, row, col, is_white):
        """Initialize a rook."""
        super().__init__(row, col, is_white)
        self.piece_type = 'R'
        self.symbol = 'R' if is_white else 'r'
    
    def get_valid_moves(self, board):
        """Get all valid moves for a rook."""
        from chess_engine.board import Move
        
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Horizontal and vertical directions
        
        for dr, dc in directions:
            for i in range(1, 8):  # Maximum 7 steps in any direction
                end_row, end_col = self.row + i * dr, self.col + i * dc
                
                # Check if we're still on the board
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                
                end_piece = board.squares[end_row][end_col]
                
                if end_piece is None:
                    # Empty square
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
                elif end_piece.is_white != self.is_white:
                    # Capture opponent's piece
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
                    break
                else:
                    # Own piece, can't move further
                    break
        
        return moves


class Queen(Piece):
    """Queen chess piece."""
    
    def __init__(self, row, col, is_white):
        """Initialize a queen."""
        super().__init__(row, col, is_white)
        self.piece_type = 'Q'
        self.symbol = 'Q' if is_white else 'q'
    
    def get_valid_moves(self, board):
        """Get all valid moves for a queen (combination of rook and bishop moves)."""
        from chess_engine.board import Move
        
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Diagonals and straight
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):  # Maximum 7 steps in any direction
                end_row, end_col = self.row + i * dr, self.col + i * dc
                
                # Check if we're still on the board
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                
                end_piece = board.squares[end_row][end_col]
                
                if end_piece is None:
                    # Empty square
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
                elif end_piece.is_white != self.is_white:
                    # Capture opponent's piece
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
                    break
                else:
                    # Own piece, can't move further
                    break
        
        return moves


class King(Piece):
    """King chess piece."""
    
    def __init__(self, row, col, is_white):
        """Initialize a king."""
        super().__init__(row, col, is_white)
        self.piece_type = 'K'
        self.symbol = 'K' if is_white else 'k'
    
    def get_valid_moves(self, board):
        """Get all valid moves for a king."""
        from chess_engine.board import Move
        
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            end_row, end_col = self.row + dr, self.col + dc
            
            # Check if we're still on the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board.squares[end_row][end_col]
                
                # Empty square or opponent's piece
                if end_piece is None or end_piece.is_white != self.is_white:
                    moves.append(Move((self.row, self.col), (end_row, end_col), board))
        
        # Note: Castling moves are added in the Board class to avoid circular imports
        # and because castling depends on more complex board state
        
        return moves