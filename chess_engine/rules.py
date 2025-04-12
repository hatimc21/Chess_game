# chess_engine/rules.py
"""
This file contains functions to handle chess rules like check detection,
checkmate, stalemate, and other special circumstances.
"""


def is_in_check(board, is_white):
    """
    Determine if the specified player is in check.
    
    Args:
        board: The current board state
        is_white (bool): True to check if white is in check, False for black
        
    Returns:
        bool: True if the player is in check, False otherwise
    """
    # Find king's position
    king_pos = board.white_king_location if is_white else board.black_king_location
    row, col = king_pos
    
    # Check if any opponent's piece can attack the king
    return is_square_attacked(board, row, col, is_white)


def is_square_attacked(board, row, col, is_white):
    """
    Determine if a square is attacked by any opponent piece.
    
    Args:
        board: The current board state
        row (int): Row of the square
        col (int): Column of the square
        is_white (bool): True if checking attacks against white, False for black
        
    Returns:
        bool: True if the square is attacked, False otherwise
    """
    # Check attacks from opponent pawns
    if is_white:
        # Black pawns attack diagonally downward
        if row > 0:
            if col > 0 and board.squares[row-1][col-1] is not None:
                piece = board.squares[row-1][col-1]
                if piece.piece_type == 'P' and not piece.is_white:
                    return True
            
            if col < 7 and board.squares[row-1][col+1] is not None:
                piece = board.squares[row-1][col+1]
                if piece.piece_type == 'P' and not piece.is_white:
                    return True
    else:
        # White pawns attack diagonally upward
        if row < 7:
            if col > 0 and board.squares[row+1][col-1] is not None:
                piece = board.squares[row+1][col-1]
                if piece.piece_type == 'P' and piece.is_white:
                    return True
            
            if col < 7 and board.squares[row+1][col+1] is not None:
                piece = board.squares[row+1][col+1]
                if piece.piece_type == 'P' and piece.is_white:
                    return True
    
    # Check attacks from knights
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board.squares[r][c] is not None:
            piece = board.squares[r][c]
            if piece.piece_type == 'N' and piece.is_white != is_white:
                return True
    
    # Check attacks from bishops, rooks, and queens
    directions = [
        # Horizontal and vertical (rook/queen)
        (-1, 0), (1, 0), (0, -1), (0, 1),
        # Diagonal (bishop/queen)
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    
    for dr, dc in directions:
        for i in range(1, 8):  # Maximum 7 steps in any direction
            r, c = row + i * dr, col + i * dc
            
            if not (0 <= r < 8 and 0 <= c < 8):
                break
            
            if board.squares[r][c] is not None:
                piece = board.squares[r][c]
                piece_type = piece.piece_type
                
                # If piece is an opponent's piece
                if piece.is_white != is_white:
                    # Check if the piece can attack in this direction
                    if (piece_type == 'Q' or 
                        (piece_type == 'R' and dr * dc == 0) or  # Rook on horizontal/vertical
                        (piece_type == 'B' and dr * dc != 0)):   # Bishop on diagonal
                        return True
                # Own piece, can't attack through it
                break
    
    # Check attacks from king
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for dr, dc in king_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board.squares[r][c] is not None:
            piece = board.squares[r][c]
            if piece.piece_type == 'K' and piece.is_white != is_white:
                return True
    
    return False


def is_checkmate(board):
    """
    Determine if the current player is in checkmate.
    
    Args:
        board: The current board state
        
    Returns:
        bool: True if the current player is in checkmate, False otherwise
    """
    # If not in check, it's not checkmate
    is_white = board.white_to_move
    if not is_in_check(board, is_white):
        return False
    
    # If there are any valid moves, it's not checkmate
    return len(board.get_valid_moves()) == 0


def is_stalemate(board):
    """
    Determine if the current position is a stalemate.
    
    Args:
        board: The current board state
        
    Returns:
        bool: True if the current player is in stalemate, False otherwise
    """
    # If in check, it's not stalemate
    is_white = board.white_to_move
    if is_in_check(board, is_white):
        return False
    
    # If there are any valid moves, it's not stalemate
    return len(board.get_valid_moves()) == 0


def is_insufficient_material(board):
    """
    Determine if there is insufficient material to checkmate.
    
    Args:
        board: The current board state
        
    Returns:
        bool: True if there is insufficient material to checkmate
    """
    # Count pieces
    white_knights = white_bishops = white_rooks = white_queens = white_pawns = 0
    black_knights = black_bishops = black_rooks = black_queens = black_pawns = 0
    
    # Square colors for bishops
    white_bishop_on_white = white_bishop_on_black = False
    black_bishop_on_white = black_bishop_on_black = False
    
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col]
            if piece is None:
                continue
            
            square_is_white = (row + col) % 2 == 0
            
            if piece.is_white:
                if piece.piece_type == 'P':
                    white_pawns += 1
                elif piece.piece_type == 'N':
                    white_knights += 1
                elif piece.piece_type == 'B':
                    if square_is_white:
                        white_bishop_on_white = True
                    else:
                        white_bishop_on_black = True
                    white_bishops += 1
                elif piece.piece_type == 'R':
                    white_rooks += 1
                elif piece.piece_type == 'Q':
                    white_queens += 1
            else:
                if piece.piece_type == 'P':
                    black_pawns += 1
                elif piece.piece_type == 'N':
                    black_knights += 1
                elif piece.piece_type == 'B':
                    if square_is_white:
                        black_bishop_on_white = True
                    else:
                        black_bishop_on_black = True
                    black_bishops += 1
                elif piece.piece_type == 'R':
                    black_rooks += 1
                elif piece.piece_type == 'Q':
                    black_queens += 1
    
    # King vs King
    if (white_knights == 0 and white_bishops == 0 and white_rooks == 0 and 
        white_queens == 0 and white_pawns == 0 and
        black_knights == 0 and black_bishops == 0 and black_rooks == 0 and 
        black_queens == 0 and black_pawns == 0):
        return True
    
    # King and Bishop vs King
    if ((white_knights == 0 and white_bishops == 1 and white_rooks == 0 and 
         white_queens == 0 and white_pawns == 0 and
         black_knights == 0 and black_bishops == 0 and black_rooks == 0 and 
         black_queens == 0 and black_pawns == 0) or
        (white_knights == 0 and white_bishops == 0 and white_rooks == 0 and 
         white_queens == 0 and white_pawns == 0 and
         black_knights == 0 and black_bishops == 1 and black_rooks == 0 and 
         black_queens == 0 and black_pawns == 0)):
        return True
    
    # King and Knight vs King
    if ((white_knights == 1 and white_bishops == 0 and white_rooks == 0 and 
         white_queens == 0 and white_pawns == 0 and
         black_knights == 0 and black_bishops == 0 and black_rooks == 0 and 
         black_queens == 0 and black_pawns == 0) or
        (white_knights == 0 and white_bishops == 0 and white_rooks == 0 and 
         white_queens == 0 and white_pawns == 0 and
         black_knights == 1 and black_bishops == 0 and black_rooks == 0 and 
         black_queens == 0 and black_pawns == 0)):
        return True
    
    # King and Bishop vs King and Bishop on same color squares
    if (white_knights == 0 and white_bishops == 1 and white_rooks == 0 and 
        white_queens == 0 and white_pawns == 0 and
        black_knights == 0 and black_bishops == 1 and black_rooks == 0 and 
        black_queens == 0 and black_pawns == 0):
        if ((white_bishop_on_white and black_bishop_on_white) or 
            (white_bishop_on_black and black_bishop_on_black)):
            return True
    
    return False


def is_threefold_repetition(board):
    """
    Determine if the current position has been repeated three times.
    
    Args:
        board: The current board state
        
    Returns:
        bool: True if there is a threefold repetition
    """
    # Get FEN for current position without move counters
    current_fen = board.get_fen().split(' ')[:4]
    current_fen = ' '.join(current_fen)
    
    # Count occurrences of this position
    position_count = 1  # Current position
    
    # Check move log for identical positions
    for i in range(len(board.move_log) - 1, -1, -1):
        # Make a copy of the board and undo moves up to this point
        temp_board = board.copy()
        for _ in range(len(board.move_log) - i):
            temp_board.undo_move()
        
        # Get FEN for this historical position
        temp_fen = temp_board.get_fen().split(' ')[:4]
        temp_fen = ' '.join(temp_fen)
        
        if temp_fen == current_fen:
            position_count += 1
            
            if position_count >= 3:
                return True
    
    return False


def is_fifty_move_rule(board):
    """
    Determine if the fifty-move rule applies.
    
    Args:
        board: The current board state
        
    Returns:
        bool: True if fifty moves have been made without a pawn move or capture
    """
    # This would typically track a halfmove clock in the board state
    # For simplicity, we'll assume the rule is not triggered
    return False


def get_game_state(board):
    """
    Get the current state of the game.
    
    Args:
        board: The current board state
        
    Returns:
        str: 'checkmate', 'stalemate', 'insufficient_material', 
             'threefold_repetition', 'fifty_move_rule', or 'ongoing'
    """
    if is_checkmate(board):
        return 'checkmate'
    elif is_stalemate(board):
        return 'stalemate'
    elif is_insufficient_material(board):
        return 'insufficient_material'
    elif is_threefold_repetition(board):
        return 'threefold_repetition'
    elif is_fifty_move_rule(board):
        return 'fifty_move_rule'
    else:
        return 'ongoing'