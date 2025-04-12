"""
This file contains the Board class and related classes for the chess game.
"""

class Piece:
    """Base class for chess pieces."""
    
    def __init__(self, is_white):
        """
        Initialize a chess piece.
        
        Args:
            is_white (bool): Whether the piece is white
        """
        self.is_white_piece = is_white
        self.symbol = ' '  # Will be overridden by subclasses
        self.has_moved = False
    
    def is_white(self):
        """Return whether the piece is white."""
        return self.is_white_piece
    
    def get_possible_moves(self, board, row, col):
        """
        Get possible moves for this piece without checking if they leave the king in check.
        
        Args:
            board: The chess board
            row (int): Current row
            col (int): Current column
            
        Returns:
            list: List of possible moves
        """
        return []


class Pawn(Piece):
    """Pawn chess piece."""
    
    def __init__(self, is_white):
        """Initialize a pawn."""
        super().__init__(is_white)
        self.symbol = 'P' if is_white else 'p'
        self.en_passant_vulnerable = False
    
    def get_possible_moves(self, board, row, col):
        """Get possible moves for a pawn."""
        moves = []
        
        # Direction of movement (white moves up, black moves down)
        direction = -1 if self.is_white() else 1
        
        # Forward move
        if 0 <= row + direction < 8 and board.squares[row + direction][col] is None:
            moves.append((row + direction, col))
            
            # Double forward move from starting position
            if ((self.is_white() and row == 6) or (not self.is_white() and row == 1)) and \
               0 <= row + 2 * direction < 8 and board.squares[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
        
        # Captures
        for col_offset in [-1, 1]:
            if 0 <= col + col_offset < 8 and 0 <= row + direction < 8:
                # Regular capture
                target = board.squares[row + direction][col + col_offset]
                if target and target.is_white() != self.is_white():
                    moves.append((row + direction, col + col_offset))
                
                # En passant capture
                if board.en_passant_possible == (row, col + col_offset):
                    moves.append((row + direction, col + col_offset))
        
        return moves


class Rook(Piece):
    """Rook chess piece."""
    
    def __init__(self, is_white):
        """Initialize a rook."""
        super().__init__(is_white)
        self.symbol = 'R' if is_white else 'r'
    
    def get_possible_moves(self, board, row, col):
        """Get possible moves for a rook."""
        moves = []
        
        # Directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + i * dr, col + i * dc
                
                # Check if position is on the board
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                
                # Check if position is empty
                if board.squares[r][c] is None:
                    moves.append((r, c))
                else:
                    # Check if position has an enemy piece
                    if board.squares[r][c].is_white() != self.is_white():
                        moves.append((r, c))
                    break
        
        return moves


class Knight(Piece):
    """Knight chess piece."""
    
    def __init__(self, is_white):
        """Initialize a knight."""
        super().__init__(is_white)
        self.symbol = 'N' if is_white else 'n'
    
    def get_possible_moves(self, board, row, col):
        """Get possible moves for a knight."""
        moves = []
        
        # Knight moves in L-shape
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            
            # Check if position is on the board
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            
            # Check if position is empty or has an enemy piece
            if board.squares[r][c] is None or board.squares[r][c].is_white() != self.is_white():
                moves.append((r, c))
        
        return moves


class Bishop(Piece):
    """Bishop chess piece."""
    
    def __init__(self, is_white):
        """Initialize a bishop."""
        super().__init__(is_white)
        self.symbol = 'B' if is_white else 'b'
    
    def get_possible_moves(self, board, row, col):
        """Get possible moves for a bishop."""
        moves = []
        
        # Directions: up-left, up-right, down-right, down-left
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + i * dr, col + i * dc
                
                # Check if position is on the board
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                
                # Check if position is empty
                if board.squares[r][c] is None:
                    moves.append((r, c))
                else:
                    # Check if position has an enemy piece
                    if board.squares[r][c].is_white() != self.is_white():
                        moves.append((r, c))
                    break
        
        return moves


class Queen(Piece):
    """Queen chess piece."""
    
    def __init__(self, is_white):
        """Initialize a queen."""
        super().__init__(is_white)
        self.symbol = 'Q' if is_white else 'q'
    
    def get_possible_moves(self, board, row, col):
        """Get possible moves for a queen."""
        moves = []
        
        # Queen moves like a rook and bishop combined
        # Directions: all 8 directions
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + i * dr, col + i * dc
                
                # Check if position is on the board
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                
                # Check if position is empty
                if board.squares[r][c] is None:
                    moves.append((r, c))
                else:
                    # Check if position has an enemy piece
                    if board.squares[r][c].is_white() != self.is_white():
                        moves.append((r, c))
                    break
        
        return moves


class King(Piece):
    """King chess piece."""
    
    def __init__(self, is_white):
        """Initialize a king."""
        super().__init__(is_white)
        self.symbol = 'K' if is_white else 'k'
    
    def get_possible_moves(self, board, row, col):
        """Get possible moves for a king."""
        moves = []
        
        # King moves one square in any direction
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            
            # Check if position is on the board
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            
            # Check if position is empty or has an enemy piece
            if board.squares[r][c] is None or board.squares[r][c].is_white() != self.is_white():
                moves.append((r, c))
        
        # Castling - will be checked for validity separately
        if not self.has_moved:
            # Kingside castling
            if self._can_castle_kingside(board, row, col):
                moves.append((row, col + 2))
            
            # Queenside castling
            if self._can_castle_queenside(board, row, col):
                moves.append((row, col - 2))
        
        return moves
    
    def _can_castle_kingside(self, board, row, col):
        """Check if kingside castling is possible (without checking for check)."""
        # Check if rook is in place and hasn't moved
        rook = board.squares[row][7]
        if not rook or rook.symbol.upper() != 'R' or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for c in range(col + 1, 7):
            if board.squares[row][c] is not None:
                return False
        
        return True
    
    def _can_castle_queenside(self, board, row, col):
        """Check if queenside castling is possible (without checking for check)."""
        # Check if rook is in place and hasn't moved
        rook = board.squares[row][0]
        if not rook or rook.symbol.upper() != 'R' or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for c in range(1, col):
            if board.squares[row][c] is not None:
                return False
        
        return True


class Move:
    """Class to represent a chess move."""
    
    def __init__(self, start_square, end_square, board, is_enpassant=False, is_castle=False):
        """
        Initialize a move.
        
        Args:
            start_square (tuple): (row, col) of start square
            end_square (tuple): (row, col) of end square
            board: The chess board
            is_enpassant (bool): Whether this is an en passant move
            is_castle (bool): Whether this is a castling move
        """
        self.start_row, self.start_col = start_square
        self.end_row, self.end_col = end_square
        self.piece_moved = board.squares[self.start_row][self.start_col]
        self.piece_captured = board.squares[self.end_row][self.end_col]
        
        # Special moves
        self.is_enpassant = is_enpassant
        if is_enpassant:
            self.piece_captured = board.squares[self.start_row][self.end_col]
        
        self.is_castle = is_castle
        
        # Pawn promotion
        self.is_promotion = (self.piece_moved and self.piece_moved.symbol.upper() == 'P' and 
                            (self.end_row == 0 or self.end_row == 7))
        
        # Check and checkmate flags
        self.is_check = False
        self.is_checkmate = False
        
        # Move ID for hashing
        self.move_id = (self.start_row * 1000 + self.start_col * 100 + 
                       self.end_row * 10 + self.end_col)
    
    def get_chess_notation(self):
        """Get the move in chess notation."""
        # Convert to chess notation (e.g., e2e4)
        files = 'abcdefgh'
        ranks = '87654321'
        
        notation = files[self.start_col] + ranks[self.start_row] + files[self.end_col] + ranks[self.end_row]
        
        # Add promotion piece if applicable
        if self.is_promotion:
            notation += 'q'  # Default promote to queen
        
        return notation
    
    def __eq__(self, other):
        """Check if two moves are equal."""
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False


class Board:
    """Class to represent the chess board and game state."""
    
    def __init__(self):
        """Initialize the chess board."""
        # Board representation: 8x8 grid of pieces
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        
        # Game state
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.en_passant_possible = None
        self.castle_rights = {'wk': True, 'wq': True, 'bk': True, 'bq': True}
        self.castle_log = []
        
        # Flag to prevent recursive validation
        self.validating_move = False
        
        # Set up the initial board position
        self._init_board()
    
    def _init_board(self):
        """Set up the initial board position."""
        # Set up pawns
        for col in range(8):
            self.squares[1][col] = Pawn(False)  # Black pawns
            self.squares[6][col] = Pawn(True)   # White pawns
        
        # Set up rooks
        self.squares[0][0] = Rook(False)
        self.squares[0][7] = Rook(False)
        self.squares[7][0] = Rook(True)
        self.squares[7][7] = Rook(True)
        
        # Set up knights
        self.squares[0][1] = Knight(False)
        self.squares[0][6] = Knight(False)
        self.squares[7][1] = Knight(True)
        self.squares[7][6] = Knight(True)
        
        # Set up bishops
        self.squares[0][2] = Bishop(False)
        self.squares[0][5] = Bishop(False)
        self.squares[7][2] = Bishop(True)
        self.squares[7][5] = Bishop(True)
        
        # Set up queens
        self.squares[0][3] = Queen(False)
        self.squares[7][3] = Queen(True)
        
        # Set up kings
        self.squares[0][4] = King(False)
        self.squares[7][4] = King(True)
    
    def make_move(self, move, validate=True):
        """
        Make a move on the board.
        
        Args:
            move: The move to make
            validate (bool): Whether to validate check/checkmate/stalemate
        """
        # Update the board
        self.squares[move.start_row][move.start_col] = None
        self.squares[move.end_row][move.end_col] = move.piece_moved
        
        # Mark piece as moved
        move.piece_moved.has_moved = True
        
        # Handle en passant capture
        if move.is_enpassant:
            self.squares[move.start_row][move.end_col] = None
        
        # Update en passant possibility
        self.en_passant_possible = None
        if move.piece_moved.symbol.upper() == 'P' and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        
        # Handle castling
        if move.is_castle:
            # Kingside castling
            if move.end_col - move.start_col == 2:
                # Move rook
                self.squares[move.end_row][move.end_col - 1] = self.squares[move.end_row][7]
                self.squares[move.end_row][7] = None
            # Queenside castling
            else:
                # Move rook
                self.squares[move.end_row][move.end_col + 1] = self.squares[move.end_row][0]
                self.squares[move.end_row][0] = None
        
        # Handle pawn promotion
        if move.is_promotion:
            # Default promote to queen
            self.squares[move.end_row][move.end_col] = Queen(move.piece_moved.is_white())
        
        # Update castling rights
        self._update_castle_rights(move)
        self.castle_log.append((
            self.castle_rights['wk'],
            self.castle_rights['wq'],
            self.castle_rights['bk'],
            self.castle_rights['bq']
        ))
        
        # Log the move
        self.move_log.append(move)
        
        # Update king location if king moved
        if move.piece_moved.symbol.upper() == 'K':
            if move.piece_moved.is_white():
                self.white_king_location = (move.end_row, move.end_col)
            else:
                self.black_king_location = (move.end_row, move.end_col)
        
        # Switch turns
        self.white_to_move = not self.white_to_move
        
        # Only validate check/checkmate/stalemate if requested
        # This prevents recursion when validating moves
        if validate:
            # Check for check and checkmate
            if self.is_in_check():
                move.is_check = True
                
                # Check for checkmate
                if self.is_checkmate():
                    move.is_checkmate = True
                    self.checkmate = True
                else:
                    self.checkmate = False
            else:
                # Check for stalemate
                if self.is_stalemate():
                    self.stalemate = True
                else:
                    self.stalemate = False
    
    def undo_move(self):
        """Undo the last move."""
        if len(self.move_log) == 0:
            return
        
        # Get the last move
        move = self.move_log.pop()
        
        # Restore the board state
        self.squares[move.start_row][move.start_col] = move.piece_moved
        self.squares[move.end_row][move.end_col] = move.piece_captured
        
        # Mark piece as not moved if it was its first move
        if len(self.move_log) == 0 or self.move_log[-1].piece_moved != move.piece_moved:
            move.piece_moved.has_moved = False
        
        # Handle en passant capture
        if move.is_enpassant:
            self.squares[move.end_row][move.end_col] = None
            self.squares[move.start_row][move.end_col] = move.piece_captured
        
        # Restore en passant possibility
        if len(self.move_log) > 0:
            last_move = self.move_log[-1]
            if last_move.piece_moved.symbol.upper() == 'P' and abs(last_move.start_row - last_move.end_row) == 2:
                self.en_passant_possible = ((last_move.start_row + last_move.end_row) // 2, last_move.start_col)
        else:
            self.en_passant_possible = None
        
        # Handle castling
        if move.is_castle:
            # Kingside castling
            if move.end_col - move.start_col == 2:
                # Move rook back
                self.squares[move.end_row][7] = self.squares[move.end_row][move.end_col - 1]
                self.squares[move.end_row][move.end_col - 1] = None
            # Queenside castling
            else:
                # Move rook back
                self.squares[move.end_row][0] = self.squares[move.end_row][move.end_col + 1]
                self.squares[move.end_row][move.end_col + 1] = None
        
        # Restore castling rights
        self.castle_log.pop()
        if len(self.castle_log) > 0:
            rights = self.castle_log[-1]
            self.castle_rights = {
                'wk': rights[0],
                'wq': rights[1],
                'bk': rights[2],
                'bq': rights[3]
            }
        else:
            self.castle_rights = {'wk': True, 'wq': True, 'bk': True, 'bq': True}
        
        # Update king location if king moved
        if move.piece_moved.symbol.upper() == 'K':
            if move.piece_moved.is_white():
                self.white_king_location = (move.start_row, move.start_col)
            else:
                self.black_king_location = (move.start_row, move.start_col)
        
        # Switch turns back
        self.white_to_move = not self.white_to_move
        
        # Reset checkmate and stalemate flags
        self.checkmate = False
        self.stalemate = False
    
    def _update_castle_rights(self, move):
        """Update castling rights based on a move."""
        # If king moved, lose both castling rights
        if move.piece_moved.symbol.upper() == 'K':
            if move.piece_moved.is_white():
                self.castle_rights['wk'] = False
                self.castle_rights['wq'] = False
            else:
                self.castle_rights['bk'] = False
                self.castle_rights['bq'] = False
        
        # If rook moved, lose that side's castling right
        elif move.piece_moved.symbol.upper() == 'R':
            # White rook
            if move.piece_moved.is_white():
                if move.start_row == 7:
                    if move.start_col == 0:  # Queenside rook
                        self.castle_rights['wq'] = False
                    elif move.start_col == 7:  # Kingside rook
                        self.castle_rights['wk'] = False
            # Black rook
            else:
                if move.start_row == 0:
                    if move.start_col == 0:  # Queenside rook
                        self.castle_rights['bq'] = False
                    elif move.start_col == 7:  # Kingside rook
                        self.castle_rights['bk'] = False
        
        # If rook is captured, lose that side's castling right
        if move.piece_captured and move.piece_captured.symbol.upper() == 'R':
            # White rook
            if move.piece_captured.is_white():
                if move.end_row == 7:
                    if move.end_col == 0:  # Queenside rook
                        self.castle_rights['wq'] = False
                    elif move.end_col == 7:  # Kingside rook
                        self.castle_rights['wk'] = False
            # Black rook
            else:
                if move.end_row == 0:
                    if move.end_col == 0:  # Queenside rook
                        self.castle_rights['bq'] = False
                    elif move.end_col == 7:  # Kingside rook
                        self.castle_rights['bk'] = False
    
    def get_possible_moves(self, row, col):
        """
        Get possible moves for a piece without checking if they leave the king in check.
        
        Args:
            row (int): Piece row
            col (int): Piece column
            
        Returns:
            list: List of possible moves as (row, col) tuples
        """
        piece = self.squares[row][col]
        if not piece:
            return []
        
        return piece.get_possible_moves(self, row, col)
    
    def get_valid_moves_for_piece(self, row, col):
        """
        Get valid moves for a piece, filtering out moves that would leave the king in check.
        
        Args:
            row (int): Piece row
            col (int): Piece column
            
        Returns:
            list: List of valid moves as (row, col) tuples
        """
        piece = self.squares[row][col]
        if not piece:
            return []
        
        # Get all possible moves for the piece
        possible_moves = self.get_possible_moves(row, col)
        
        # Filter out moves that would leave the king in check
        valid_moves = []
        for end_pos in possible_moves:
            end_row, end_col = end_pos
            
            # Check for special moves
            is_enpassant = False
            if piece.symbol.upper() == 'P' and (end_row, end_col) == self.en_passant_possible:
                is_enpassant = True
            
            is_castle = False
            if piece.symbol.upper() == 'K' and abs(col - end_col) == 2:
                is_castle = True
                
                # For castling, check if the king is in check or would pass through check
                if self.is_in_check():
                    continue
                
                # Check if the king would pass through check
                if end_col > col:  # Kingside
                    if self.is_square_under_attack(row, col + 1, not piece.is_white()):
                        continue
                else:  # Queenside
                    if self.is_square_under_attack(row, col - 1, not piece.is_white()):
                        continue
            
            # Create a move object
            move_obj = Move((row, col), (end_row, end_col), self, is_enpassant, is_castle)
            
            # Simulate the move to check if it would leave the king in check
            self.make_move(move_obj, validate=False)
            
            # Check if the king is in check after the move
            king_in_check = self.is_in_check(not self.white_to_move)
            
            # Undo the move
            self.undo_move()
            
            # If the move doesn't leave the king in check, it's valid
            if not king_in_check:
                valid_moves.append(end_pos)
        
        return valid_moves
    
    def get_all_valid_moves(self):
        """
        Get all valid moves for the current player.
        
        Returns:
            list: List of valid Move objects
        """
        moves = []
        
        # If we're already validating a move, return an empty list to prevent recursion
        if self.validating_move:
            return moves
        
        # Set the validating flag to prevent recursion
        self.validating_move = True
        
        try:
            for row in range(8):
                for col in range(8):
                    piece = self.squares[row][col]
                    
                    # Check if piece belongs to current player
                    if piece and ((piece.is_white() and self.white_to_move) or 
                                (not piece.is_white() and not self.white_to_move)):
                        
                        # Get valid moves for this piece
                        valid_moves = self.get_valid_moves_for_piece(row, col)
                        
                        # Convert to Move objects
                        for end_pos in valid_moves:
                            end_row, end_col = end_pos
                            
                            # Check for special moves
                            is_enpassant = False
                            if piece.symbol.upper() == 'P' and (end_row, end_col) == self.en_passant_possible:
                                is_enpassant = True
                            
                            is_castle = False
                            if piece.symbol.upper() == 'K' and abs(col - end_col) == 2:
                                is_castle = True
                            
                            # Create move
                            move = Move((row, col), (end_row, end_col), self, is_enpassant, is_castle)
                            moves.append(move)
        finally:
            # Reset the validating flag
            self.validating_move = False
        
        return moves
    
    def get_move(self, start_row, start_col, end_row, end_col):
        """
        Create a Move object for the given move.
        
        Args:
            start_row (int): Starting row
            start_col (int): Starting column
            end_row (int): Ending row
            end_col (int): Ending column
            
        Returns:
            Move: The move object
        """
        # Check for special moves
        piece = self.squares[start_row][start_col]
        if not piece:
            return None
        
        is_enpassant = False
        if piece.symbol.upper() == 'P' and (end_row, end_col) == self.en_passant_possible:
            is_enpassant = True
        
        is_castle = False
        if piece.symbol.upper() == 'K' and abs(start_col - end_col) == 2:
            is_castle = True
        
        return Move((start_row, start_col), (end_row, end_col), self, is_enpassant, is_castle)
    
    def is_in_check(self, white_turn=None):
        """
        Check if the current player is in check.
        
        Args:
            white_turn (bool): Whether to check if white is in check (None for current player)
            
        Returns:
            bool: Whether the player is in check
        """
        if white_turn is None:
            white_turn = self.white_to_move
        
        # Get king location
        king_row, king_col = self.white_king_location if white_turn else self.black_king_location
        
        # Check if the king's square is under attack
        return self.is_square_under_attack(king_row, king_col, not white_turn)
    
    def is_square_under_attack(self, row, col, by_white):
        """
        Check if a square is under attack by a player.
        
        Args:
            row (int): Square row
            col (int): Square column
            by_white (bool): Whether to check if white is attacking
            
        Returns:
            bool: Whether the square is under attack
        """
        # Check attacks from all opponent pieces
        for r in range(8):
            for c in range(8):
                piece = self.squares[r][c]
                
                # Check if piece belongs to the attacking player
                if piece and piece.is_white() == by_white:
                    # Get possible moves without checking for check
                    possible_moves = self.get_possible_moves(r, c)
                    
                    # Check if the square is in the possible moves
                    if (row, col) in possible_moves:
                        return True
        
        return False
    
    def is_checkmate(self):
        """
        Check if the current player is in checkmate.
        
        Returns:
            bool: Whether the player is in checkmate
        """
        # If not in check, can't be checkmate
        if not self.is_in_check():
            return False
        
        # Check if any move gets out of check
        return len(self.get_all_valid_moves()) == 0
    
    def is_stalemate(self):
        """
        Check if the current player is in stalemate.
        
        Returns:
            bool: Whether the player is in stalemate
        """
        # If in check, can't be stalemate
        if self.is_in_check():
            return False
        
        # Check if any valid move exists
        return len(self.get_all_valid_moves()) == 0