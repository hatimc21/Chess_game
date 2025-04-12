# chess_engine/board.py
"""
This file contains the Board class for representing a chess board,
and the Move class for representing chess moves.
"""


class Board:
    """
    Represents a chess board with pieces and game state.
    """
    
    def __init__(self):
        """Initialize a new chess board with standard setup."""
        # Create an 8x8 empty board
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        
        # Game state
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)  # Starting position (row, col)
        self.black_king_location = (0, 4)  # Starting position (row, col)
        
        # Castling rights
        self.white_king_side_castle = True
        self.white_queen_side_castle = True
        self.black_king_side_castle = True
        self.black_queen_side_castle = True
        
        # En passant possibility
        self.en_passant_possible = ()  # Coordinates for the square where en passant capture is possible
        
        # Game end flags
        self.checkmate = False
        self.stalemate = False
        
        # Load the standard chess position
        self.reset_board()
    
    def reset_board(self):
        """Set up the board with standard chess starting position."""
        from chess_engine.pieces import Rook, Knight, Bishop, Queen, King, Pawn
        
        # Place pawns
        for col in range(8):
            self.squares[1][col] = Pawn(1, col, False)  # Black pawns
            self.squares[6][col] = Pawn(6, col, True)   # White pawns
        
        # Place rooks
        self.squares[0][0] = Rook(0, 0, False)
        self.squares[0][7] = Rook(0, 7, False)
        self.squares[7][0] = Rook(7, 0, True)
        self.squares[7][7] = Rook(7, 7, True)
        
        # Place knights
        self.squares[0][1] = Knight(0, 1, False)
        self.squares[0][6] = Knight(0, 6, False)
        self.squares[7][1] = Knight(7, 1, True)
        self.squares[7][6] = Knight(7, 6, True)
        
        # Place bishops
        self.squares[0][2] = Bishop(0, 2, False)
        self.squares[0][5] = Bishop(0, 5, False)
        self.squares[7][2] = Bishop(7, 2, True)
        self.squares[7][5] = Bishop(7, 5, True)
        
        # Place queens
        self.squares[0][3] = Queen(0, 3, False)
        self.squares[7][3] = Queen(7, 3, True)
        
        # Place kings
        self.squares[0][4] = King(0, 4, False)
        self.squares[7][4] = King(7, 4, True)
        
        # Reset game state
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.white_king_side_castle = True
        self.white_queen_side_castle = True
        self.black_king_side_castle = True
        self.black_queen_side_castle = True
        self.en_passant_possible = ()
        self.checkmate = False
        self.stalemate = False
    
    def make_move(self, move):
        """
        Execute a move on the board.
        
        Args:
            move: A Move object representing the move to execute
            
        Returns:
            None
        """
        # Update the board: empty the source square
        self.squares[move.start_row][move.start_col] = None
        
        # Place the piece in the destination square
        self.squares[move.end_row][move.end_col] = move.piece_moved
        
        # Update the piece's position
        move.piece_moved.row = move.end_row
        move.piece_moved.col = move.end_col
        move.piece_moved.moved = True
        
        # Log the move with castle rights
        castle_rights = CastleRights(
            self.white_king_side_castle,
            self.white_queen_side_castle,
            self.black_king_side_castle,
            self.black_queen_side_castle
        )
        move.castle_rights = castle_rights
        move.en_passant_possible = self.en_passant_possible
        self.move_log.append(move)
        
        # Switch turns
        self.white_to_move = not self.white_to_move
        
        # Update king location if king was moved
        if move.piece_moved.piece_type == 'K':
            if move.piece_moved.is_white:
                self.white_king_location = (move.end_row, move.end_col)
            else:
                self.black_king_location = (move.end_row, move.end_col)
        
        # Handle pawn promotion
        if move.is_pawn_promotion:
            self.squares[move.end_row][move.end_col] = move.promotion_piece
            # Update the piece position
            move.promotion_piece.row = move.end_row
            move.promotion_piece.col = move.end_col
        
        # Handle en passant captures
        if move.is_en_passant_move:
            # Remove the captured pawn
            capture_row = move.start_row
            self.squares[capture_row][move.end_col] = None
        
        # Update en passant possibility
        if move.piece_moved.piece_type == 'P' and abs(move.start_row - move.end_row) == 2:
            # Set en passant square to the square the pawn skipped over
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_possible = ()
        
        # Handle castling move
        if move.is_castle_move:
            # Check if kingside or queenside castle
            if move.end_col - move.start_col == 2:  # Kingside castle
                # Move the rook from H1/H8 to F1/F8
                rook_start_col = 7
                rook_end_col = 5
            else:  # Queenside castle
                # Move the rook from A1/A8 to D1/D8
                rook_start_col = 0
                rook_end_col = 3
            
            # Move the rook
            rook = self.squares[move.end_row][rook_start_col]
            self.squares[move.end_row][rook_start_col] = None
            self.squares[move.end_row][rook_end_col] = rook
            rook.col = rook_end_col
            rook.moved = True
        
        # Update castling rights
        self._update_castle_rights(move)
    
    def undo_move(self):
        """
        Undo the last move made.
        
        Returns:
            bool: True if a move was undone, False if no moves to undo
        """
        if not self.move_log:
            return False
        
        # Get the last move
        move = self.move_log.pop()
        
        # Restore positions
        self.squares[move.start_row][move.start_col] = move.piece_moved
        self.squares[move.end_row][move.end_col] = move.piece_captured
        
        # Update the piece's position
        move.piece_moved.row = move.start_row
        move.piece_moved.col = move.start_col
        
        # Switch turns back
        self.white_to_move = not self.white_to_move
        
        # Update king location if king was moved
        if move.piece_moved.piece_type == 'K':
            if move.piece_moved.is_white:
                self.white_king_location = (move.start_row, move.start_col)
            else:
                self.black_king_location = (move.start_row, move.start_col)
        
        # Handle en passant captures
        if move.is_en_passant_move:
            # Put back the empty square where the piece moved
            self.squares[move.end_row][move.end_col] = None
            # Restore the captured pawn
            capture_row = move.start_row
            self.squares[capture_row][move.end_col] = move.piece_captured
        
        # Restore en passant possibility
        self.en_passant_possible = move.en_passant_possible
        
        # Restore castling rights
        self.white_king_side_castle = move.castle_rights.wks
        self.white_queen_side_castle = move.castle_rights.wqs
        self.black_king_side_castle = move.castle_rights.bks
        self.black_queen_side_castle = move.castle_rights.bqs
        
        # Handle castling move
        if move.is_castle_move:
            # Check if kingside or queenside castle
            if move.end_col - move.start_col == 2:  # Kingside castle
                # Move the rook back from F1/F8 to H1/H8
                rook = self.squares[move.end_row][5]
                self.squares[move.end_row][5] = None
                self.squares[move.end_row][7] = rook
                rook.col = 7
            else:  # Queenside castle
                # Move the rook back from D1/D8 to A1/A8
                rook = self.squares[move.end_row][3]
                self.squares[move.end_row][3] = None
                self.squares[move.end_row][0] = rook
                rook.col = 0
        
        # Reset checkmate and stalemate flags
        self.checkmate = False
        self.stalemate = False
        
        return True
    
    def get_valid_moves(self):
        """
        Get all valid moves for the current player considering checks.
        
        Returns:
            list: A list of valid Move objects
        """
        temp_en_passant_possible = self.en_passant_possible
        temp_castle_rights = CastleRights(
            self.white_king_side_castle, 
            self.white_queen_side_castle,
            self.black_king_side_castle, 
            self.black_queen_side_castle
        )
        
        # 1. Generate all possible moves
        moves = self._get_all_possible_moves()
        
        # 2. Make each move and check if it leaves the king in check
        for i in range(len(moves) - 1, -1, -1):
            move = moves[i]
            self.make_move(move)
            
            # 3. Generate opponent's moves and check if our king is attacked
            self.white_to_move = not self.white_to_move
            if self._is_in_check():
                # If we're in check, it's not a valid move
                moves.remove(move)
            
            # 4. Undo the move and switch back
            self.white_to_move = not self.white_to_move
            self.undo_move()
        
        # 5. Check for checkmate or stalemate
        if len(moves) == 0:
            if self._is_in_check():
                self.checkmate = True
                self.stalemate = False
                print("Checkmate detected - no valid moves and king is in check")
            else:
                self.checkmate = False
                self.stalemate = True
                print("Stalemate detected - no valid moves but king is not in check")
        else:
            self.checkmate = False
            self.stalemate = False
        
        # 6. Generate castling moves if possible and king is not in check
        if not self._is_in_check():
            if self.white_to_move:
                self._get_castle_moves(
                    self.white_king_location[0], 
                    self.white_king_location[1], 
                    moves
                )
            else:
                self._get_castle_moves(
                    self.black_king_location[0], 
                    self.black_king_location[1], 
                    moves
                )
        
        # Restore temporary variables
        self.en_passant_possible = temp_en_passant_possible
        self.white_king_side_castle = temp_castle_rights.wks
        self.white_queen_side_castle = temp_castle_rights.wqs
        self.black_king_side_castle = temp_castle_rights.bks
        self.black_queen_side_castle = temp_castle_rights.bqs
        
        return moves
    
    def _is_in_check(self):
        """
        Determine if the current player is in check.
        
        Returns:
            bool: True if in check, False otherwise
        """
        if self.white_to_move:
            king_row, king_col = self.white_king_location
        else:
            king_row, king_col = self.black_king_location
            
        # Temporarily switch turns to see if opponent can attack king
        self.white_to_move = not self.white_to_move
        opponent_moves = self._get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        
        # Check if any opponent move can capture the king
        for move in opponent_moves:
            if move.end_row == king_row and move.end_col == king_col:
                return True
                
        return False
    
    def _is_square_attacked(self, row, col):
        """
        Determine if a square is under attack by the opponent.
        
        Args:
            row (int): Row of the square
            col (int): Column of the square
            
        Returns:
            bool: True if the square is attacked, False otherwise
        """
        # Switch to opponent's perspective
        is_white_turn = self.white_to_move
        self.white_to_move = not is_white_turn
        
        # Generate all opponent's moves
        opponent_moves = self._get_all_possible_moves()
        
        # Switch back
        self.white_to_move = is_white_turn
        
        # Check if any opponent move targets this square
        for move in opponent_moves:
            if move.end_row == row and move.end_col == col:
                return True
        
        return False
    
    def _get_all_possible_moves(self):
        """
        Get all possible moves without considering checks.
        
        Returns:
            list: A list of all possible Move objects
        """
        moves = []
        
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                
                if piece is not None:
                    # Only get moves for the current player's pieces
                    if (piece.is_white and self.white_to_move) or (not piece.is_white and not self.white_to_move):
                        # Get piece-specific moves
                        piece_moves = []
                        
                        # Pawns
                        if piece.piece_type == 'P':
                            piece_moves = self._get_pawn_moves(row, col)
                        # Knights
                        elif piece.piece_type == 'N':
                            piece_moves = self._get_knight_moves(row, col)
                        # Bishops
                        elif piece.piece_type == 'B':
                            piece_moves = self._get_bishop_moves(row, col)
                        # Rooks
                        elif piece.piece_type == 'R':
                            piece_moves = self._get_rook_moves(row, col)
                        # Queens (combines bishop + rook moves)
                        elif piece.piece_type == 'Q':
                            piece_moves = self._get_bishop_moves(row, col)
                            piece_moves.extend(self._get_rook_moves(row, col))
                        # Kings
                        elif piece.piece_type == 'K':
                            piece_moves = self._get_king_moves(row, col)
                        
                        # Add all valid piece moves
                        moves.extend(piece_moves)
        
        return moves
    
    def _get_pawn_moves(self, row, col):
        """Get all possible moves for a pawn at the given position."""
        moves = []
        piece = self.squares[row][col]
        
        if piece is None or piece.piece_type != 'P':
            return moves
            
        # Determine direction of movement based on color
        direction = -1 if piece.is_white else 1
        
        # Forward move - 1 square
        if 0 <= row + direction < 8 and self.squares[row + direction][col] is None:
            moves.append(Move((row, col), (row + direction, col), self))
            
            # Forward move - 2 squares (from starting position)
            start_row = 6 if piece.is_white else 1
            if row == start_row and self.squares[row + 2*direction][col] is None:
                moves.append(Move((row, col), (row + 2*direction, col), self))
        
        # Captures
        for col_offset in [-1, 1]:
            capture_col = col + col_offset
            if 0 <= capture_col < 8 and 0 <= row + direction < 8:
                # Regular capture
                capture_piece = self.squares[row + direction][capture_col]
                if capture_piece is not None and capture_piece.is_white != piece.is_white:
                    moves.append(Move((row, col), (row + direction, capture_col), self))
                
                # En passant capture
                elif (row + direction, capture_col) == self.en_passant_possible:
                    moves.append(Move((row, col), (row + direction, capture_col), self, is_en_passant_move=True))
        
        return moves
    
    def _get_knight_moves(self, row, col):
        """Get all possible moves for a knight at the given position."""
        moves = []
        piece = self.squares[row][col]
        
        if piece is None or piece.piece_type != 'N':
            return moves
            
        # Knight move offsets (L-shape)
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for offset_row, offset_col in offsets:
            end_row, end_col = row + offset_row, col + offset_col
            
            # Check if the target position is on the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.squares[end_row][end_col]
                
                # Empty square or opponent's piece
                if end_piece is None or end_piece.is_white != piece.is_white:
                    moves.append(Move((row, col), (end_row, end_col), self))
        
        return moves
    
    def _get_bishop_moves(self, row, col):
        """Get all possible moves for a bishop at the given position."""
        moves = []
        piece = self.squares[row][col]
        
        if piece is None or (piece.piece_type != 'B' and piece.piece_type != 'Q'):
            return moves
            
        # Direction offsets for diagonals
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for direction_row, direction_col in directions:
            for distance in range(1, 8):  # Maximum 7 squares in any direction
                end_row = row + direction_row * distance
                end_col = col + direction_col * distance
                
                # Check if the target position is on the board
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                
                end_piece = self.squares[end_row][end_col]
                
                # Empty square
                if end_piece is None:
                    moves.append(Move((row, col), (end_row, end_col), self))
                # Opponent's piece - can capture and then stop
                elif end_piece.is_white != piece.is_white:
                    moves.append(Move((row, col), (end_row, end_col), self))
                    break
                # Own piece - stop without capturing
                else:
                    break
        
        return moves
    
    def _get_rook_moves(self, row, col):
        """Get all possible moves for a rook at the given position."""
        moves = []
        piece = self.squares[row][col]
        
        if piece is None or (piece.piece_type != 'R' and piece.piece_type != 'Q'):
            return moves
            
        # Direction offsets for horizontals and verticals
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for direction_row, direction_col in directions:
            for distance in range(1, 8):  # Maximum 7 squares in any direction
                end_row = row + direction_row * distance
                end_col = col + direction_col * distance
                
                # Check if the target position is on the board
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                
                end_piece = self.squares[end_row][end_col]
                
                # Empty square
                if end_piece is None:
                    moves.append(Move((row, col), (end_row, end_col), self))
                # Opponent's piece - can capture and then stop
                elif end_piece.is_white != piece.is_white:
                    moves.append(Move((row, col), (end_row, end_col), self))
                    break
                # Own piece - stop without capturing
                else:
                    break
        
        return moves
    
    def _get_king_moves(self, row, col):
        """Get all possible moves for a king at the given position."""
        moves = []
        piece = self.squares[row][col]
        
        if piece is None or piece.piece_type != 'K':
            return moves
            
        # Direction offsets for all 8 surrounding squares
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for direction_row, direction_col in directions:
            end_row = row + direction_row
            end_col = col + direction_col
            
            # Check if the target position is on the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.squares[end_row][end_col]
                
                # Empty square or opponent's piece
                if end_piece is None or end_piece.is_white != piece.is_white:
                    moves.append(Move((row, col), (end_row, end_col), self))
        
        # Castling moves are handled separately in get_valid_moves
        
        return moves
    
    def _get_castle_moves(self, row, col, moves):
        """
        Generate valid castling moves for the king at the given position.
        
        Args:
            row (int): King's row
            col (int): King's column
            moves (list): List to append valid castle moves to
        """
        # Check kingside castling
        if (self.white_to_move and self.white_king_side_castle) or (not self.white_to_move and self.black_king_side_castle):
            self._get_kingside_castle_moves(row, col, moves)
        
        # Check queenside castling
        if (self.white_to_move and self.white_queen_side_castle) or (not self.white_to_move and self.black_queen_side_castle):
            self._get_queenside_castle_moves(row, col, moves)
    
    def _get_kingside_castle_moves(self, row, col, moves):
        """Check if kingside castling is valid and add to moves if so."""
        # Check if squares between king and rook are empty
        if self.squares[row][col+1] is None and self.squares[row][col+2] is None:
            # Check if king passes through or ends up on attacked squares
            if not self._is_square_attacked(row, col+1) and not self._is_square_attacked(row, col+2):
                moves.append(Move(
                    (row, col), 
                    (row, col+2), 
                    self,
                    is_castle_move=True
                ))
    
    def _get_queenside_castle_moves(self, row, col, moves):
        """Check if queenside castling is valid and add to moves if so."""
        # Check if squares between king and rook are empty
        if (self.squares[row][col-1] is None and 
            self.squares[row][col-2] is None and 
            self.squares[row][col-3] is None):
            # Knight square (b1/b8) can be attacked, but not the king's path
            if not self._is_square_attacked(row, col-1) and not self._is_square_attacked(row, col-2):
                moves.append(Move(
                    (row, col), 
                    (row, col-2), 
                    self,
                    is_castle_move=True
                ))
    
    def _update_castle_rights(self, move):
        """Update castling rights based on the move."""
        # If king moves, lose all castling rights
        if move.piece_moved.piece_type == 'K':
            if move.piece_moved.is_white:
                self.white_king_side_castle = False
                self.white_queen_side_castle = False
            else:
                self.black_king_side_castle = False
                self.black_queen_side_castle = False
        
        # If rook moves or is captured, lose that castling right
        elif move.piece_moved.piece_type == 'R':
            # White rook moves
            if move.piece_moved.is_white:
                if move.start_row == 7:
                    if move.start_col == 0:  # Queen's rook
                        self.white_queen_side_castle = False
                    elif move.start_col == 7:  # King's rook
                        self.white_king_side_castle = False
            # Black rook moves
            else:
                if move.start_row == 0:
                    if move.start_col == 0:  # Queen's rook
                        self.black_queen_side_castle = False
                    elif move.start_col == 7:  # King's rook
                        self.black_king_side_castle = False
        
        # If a rook is captured
        if move.piece_captured is not None and move.piece_captured.piece_type == 'R':
            # White rook captured
            if not move.piece_captured.is_white:
                if move.end_row == 0:
                    if move.end_col == 0:  # Queen's rook
                        self.black_queen_side_castle = False
                    elif move.end_col == 7:  # King's rook
                        self.black_king_side_castle = False
            # Black rook captured
            else:
                if move.end_row == 7:
                    if move.end_col == 0:  # Queen's rook
                        self.white_queen_side_castle = False
                    elif move.end_col == 7:  # King's rook
                        self.white_king_side_castle = False
    
    def algebraic_to_coords(self, algebraic):
        """
        Convert algebraic notation (e.g., 'e4') to board coordinates.
        
        Args:
            algebraic (str): Position in algebraic notation
            
        Returns:
            tuple: (row, col) coordinates
        """
        col = ord(algebraic[0].lower()) - ord('a')
        row = 8 - int(algebraic[1])
        return row, col
    
    def coords_to_algebraic(self, row, col):
        """
        Convert board coordinates to algebraic notation.
        
        Args:
            row (int): Row coordinate
            col (int): Column coordinate
            
        Returns:
            str: Position in algebraic notation
        """
        return chr(col + ord('a')) + str(8 - row)
    
    def get_fen(self):
        """
        Generate FEN (Forsyth-Edwards Notation) for the current board position.
        
        Returns:
            str: FEN string
        """
        fen = ""
        
        # Board position
        for row in range(8):
            empty_count = 0
            for col in range(8):
                piece = self.squares[row][col]
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    
                    symbol = piece.symbol
                    fen += symbol
            
            if empty_count > 0:
                fen += str(empty_count)
            
            if row < 7:
                fen += "/"
        
        # Active color
        fen += " w " if self.white_to_move else " b "
        
        # Castling availability
        castling = ""
        if self.white_king_side_castle:
            castling += "K"
        if self.white_queen_side_castle:
            castling += "Q"
        if self.black_king_side_castle:
            castling += "k"
        if self.black_queen_side_castle:
            castling += "q"
        
        fen += castling if castling else "-"
        
        # En passant target square
        if self.en_passant_possible:
            fen += " " + self.coords_to_algebraic(self.en_passant_possible[0], self.en_passant_possible[1])
        else:
            fen += " -"
        
        # Halfmove clock (not implemented)
        fen += " 0"
        
        # Fullmove number (not implemented)
        fen += " 1"
        
        return fen
    
    def load_from_fen(self, fen):
        """
        Load a position from FEN notation.
        
        Args:
            fen (str): FEN string
        """
        from chess_engine.pieces import Pawn, Knight, Bishop, Rook, Queen, King
        
        # Clear the board
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        
        # Split FEN parts
        parts = fen.split(' ')
        board_str = parts[0]
        
        # Parse board position
        rows = board_str.split('/')
        for row_idx, row_str in enumerate(rows):
            col_idx = 0
            for char in row_str:
                if char.isdigit():
                    col_idx += int(char)
                else:
                    is_white = char.isupper()
                    char = char.upper()
                    
                    if char == 'P':
                        self.squares[row_idx][col_idx] = Pawn(row_idx, col_idx, is_white)
                    elif char == 'N':
                        self.squares[row_idx][col_idx] = Knight(row_idx, col_idx, is_white)
                    elif char == 'B':
                        self.squares[row_idx][col_idx] = Bishop(row_idx, col_idx, is_white)
                    elif char == 'R':
                        self.squares[row_idx][col_idx] = Rook(row_idx, col_idx, is_white)
                    elif char == 'Q':
                        self.squares[row_idx][col_idx] = Queen(row_idx, col_idx, is_white)
                    elif char == 'K':
                        self.squares[row_idx][col_idx] = King(row_idx, col_idx, is_white)
                        if is_white:
                            self.white_king_location = (row_idx, col_idx)
                        else:
                            self.black_king_location = (row_idx, col_idx)
                    
                    col_idx += 1
        
        # Active color
        self.white_to_move = parts[1] == 'w'
        
        # Castling availability
        castling = parts[2]
        self.white_king_side_castle = 'K' in castling
        self.white_queen_side_castle = 'Q' in castling
        self.black_king_side_castle = 'k' in castling
        self.black_queen_side_castle = 'q' in castling
        
        # En passant target square
        if parts[3] != '-':
            self.en_passant_possible = self.algebraic_to_coords(parts[3])
        else:
            self.en_passant_possible = ()
        
        # Reset game state
        self.checkmate = False
        self.stalemate = False
        self.move_log = []


class CastleRights:
    """Class to store castling rights."""
    
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks  # White king side
        self.wqs = wqs  # White queen side
        self.bks = bks  # Black king side
        self.bqs = bqs  # Black queen side


class Move:
    """
    Class to represent a chess move.
    
    Attributes:
        start_row (int): Starting row
        start_col (int): Starting column
        end_row (int): Ending row
        end_col (int): Ending column
        piece_moved (Piece): The piece that was moved
        piece_captured (Piece): The piece that was captured, if any
        is_pawn_promotion (bool): Whether this move results in a pawn promotion
        promotion_piece (Piece): The piece to promote to, if applicable
        is_en_passant_move (bool): Whether this move is an en passant capture
        is_castle_move (bool): Whether this move is a castling move
    """
    
    # Map keys to values for chess notation
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
    
    def __init__(self, start_square, end_square, board, is_en_passant_move=False, is_castle_move=False):
        """
        Initialize a move.
        
        Args:
            start_square (tuple): (row, col) of the starting square
            end_square (tuple): (row, col) of the ending square
            board (Board): The current board state
            is_en_passant_move (bool): Whether this is an en passant move
            is_castle_move (bool): Whether this is a castling move
        """
        self.start_row, self.start_col = start_square
        self.end_row, self.end_col = end_square
        
        self.piece_moved = board.squares[self.start_row][self.start_col]
        self.piece_captured = board.squares[self.end_row][self.end_col]
        
        # Pawn promotion
        self.is_pawn_promotion = False
        if (self.piece_moved.piece_type == 'P' and 
           ((self.piece_moved.is_white and self.end_row == 0) or 
            (not self.piece_moved.is_white and self.end_row == 7))):
            self.is_pawn_promotion = True
            # Default promotion is to Queen
            from chess_engine.pieces import Queen
            self.promotion_piece = Queen(self.end_row, self.end_col, self.piece_moved.is_white)
        else:
            self.promotion_piece = None
        
        # En passant move
        self.is_en_passant_move = is_en_passant_move
        if self.is_en_passant_move:
            # In en passant, the captured pawn is on the same row as the moving pawn
            self.piece_captured = board.squares[self.start_row][self.end_col]
        
        # Castle move
        self.is_castle_move = is_castle_move
        
        # For convenience in move log
        self.castle_rights = None  # To be set when move is made
        self.en_passant_possible = None  # To be set when move is made
    
    def get_chess_notation(self):
        """
        Get the move in algebraic chess notation.
        
        Returns:
            str: The move in algebraic notation
        """
        # For now, return a simple notation like e2e4
        return (
            self.cols_to_files[self.start_col] +
            self.rows_to_ranks[self.start_row] +
            self.cols_to_files[self.end_col] +
            self.rows_to_ranks[self.end_row]
        )
    
    def __eq__(self, other):
        """
        Compare two moves for equality.
        
        Args:
            other (Move): Another move to compare with
            
        Returns:
            bool: True if the moves are the same
        """
        if isinstance(other, Move):
            return (
                self.start_row == other.start_row and
                self.start_col == other.start_col and
                self.end_row == other.end_row and
                self.end_col == other.end_col
            )
        return False
    
    def __str__(self):
        """String representation of the move."""
        return self.get_chess_notation()