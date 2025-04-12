# ai/features.py
"""
This file contains functions to extract features from chess positions for AI training.
"""

import numpy as np


def extract_features(board):
    """
    Extract features from a chess board position.
    
    Args:
        board: The chess board object
        
    Returns:
        np.array: Feature vector representing the position
    """
    features = []
    
    # Material count (12 features)
    material_features = get_material_features(board)
    features.extend(material_features)
    
    # Piece mobility (12 features)
    mobility_features = get_mobility_features(board)
    features.extend(mobility_features)
    
    # Board control (2 features)
    control_features = get_board_control_features(board)
    features.extend(control_features)
    
    # King safety (2 features)
    king_safety_features = get_king_safety_features(board)
    features.extend(king_safety_features)
    
    # Pawn structure (4 features)
    pawn_structure_features = get_pawn_structure_features(board)
    features.extend(pawn_structure_features)
    
    # Development (2 features)
    development_features = get_development_features(board)
    features.extend(development_features)
    
    # Center control (2 features)
    center_control_features = get_center_control_features(board)
    features.extend(center_control_features)
    
    # Return as numpy array
    return np.array(features)


def get_material_features(board):
    """
    Extract material count features.
    
    Returns 12 features: count of each piece type for each color
    """
    # Initialize counts
    white_pawn = white_knight = white_bishop = white_rook = white_queen = white_king = 0
    black_pawn = black_knight = black_bishop = black_rook = black_queen = black_king = 0
    
    # Count pieces
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col]
            if piece is None:
                continue
            
            if piece.is_white:
                if piece.piece_type == 'P':
                    white_pawn += 1
                elif piece.piece_type == 'N':
                    white_knight += 1
                elif piece.piece_type == 'B':
                    white_bishop += 1
                elif piece.piece_type == 'R':
                    white_rook += 1
                elif piece.piece_type == 'Q':
                    white_queen += 1
                elif piece.piece_type == 'K':
                    white_king += 1
            else:
                if piece.piece_type == 'P':
                    black_pawn += 1
                elif piece.piece_type == 'N':
                    black_knight += 1
                elif piece.piece_type == 'B':
                    black_bishop += 1
                elif piece.piece_type == 'R':
                    black_rook += 1
                elif piece.piece_type == 'Q':
                    black_queen += 1
                elif piece.piece_type == 'K':
                    black_king += 1
    
    return [
        white_pawn, white_knight, white_bishop, white_rook, white_queen, white_king,
        black_pawn, black_knight, black_bishop, black_rook, black_queen, black_king
    ]


def get_mobility_features(board):
    """
    Extract piece mobility features.
    
    Returns 12 features: mobility of each piece type for each color
    """
    # Save original turn
    original_turn = board.white_to_move
    
    # Initialize mobility counts
    white_pawn_mobility = white_knight_mobility = white_bishop_mobility = 0
    white_rook_mobility = white_queen_mobility = white_king_mobility = 0
    black_pawn_mobility = black_knight_mobility = black_bishop_mobility = 0
    black_rook_mobility = black_queen_mobility = black_king_mobility = 0
    
    # Count white piece mobility
    board.white_to_move = True
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col]
            if piece is None or not piece.is_white:
                continue
            
            # Get moves for this piece
            moves = piece.get_valid_moves(board)
            
            # Add to appropriate counter
            if piece.piece_type == 'P':
                white_pawn_mobility += len(moves)
            elif piece.piece_type == 'N':
                white_knight_mobility += len(moves)
            elif piece.piece_type == 'B':
                white_bishop_mobility += len(moves)
            elif piece.piece_type == 'R':
                white_rook_mobility += len(moves)
            elif piece.piece_type == 'Q':
                white_queen_mobility += len(moves)
            elif piece.piece_type == 'K':
                white_king_mobility += len(moves)
    
    # Count black piece mobility
    board.white_to_move = False
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col]
            if piece is None or piece.is_white:
                continue
            
            # Get moves for this piece
            moves = piece.get_valid_moves(board)
            
            # Add to appropriate counter
            if piece.piece_type == 'P':
                black_pawn_mobility += len(moves)
            elif piece.piece_type == 'N':
                black_knight_mobility += len(moves)
            elif piece.piece_type == 'B':
                black_bishop_mobility += len(moves)
            elif piece.piece_type == 'R':
                black_rook_mobility += len(moves)
            elif piece.piece_type == 'Q':
                black_queen_mobility += len(moves)
            elif piece.piece_type == 'K':
                black_king_mobility += len(moves)
    
    # Restore original turn
    board.white_to_move = original_turn
    
    return [
        white_pawn_mobility, white_knight_mobility, white_bishop_mobility,
        white_rook_mobility, white_queen_mobility, white_king_mobility,
        black_pawn_mobility, black_knight_mobility, black_bishop_mobility,
        black_rook_mobility, black_queen_mobility, black_king_mobility
    ]


def get_board_control_features(board):
    """
    Extract board control features.
    
    Returns 2 features: number of squares controlled by each player
    """
    white_control = 0
    black_control = 0
    
    # Check each square on the board
    for row in range(8):
        for col in range(8):
            # Save original turn
            original_turn = board.white_to_move
            
            # Check if white controls this square
            board.white_to_move = False  # Checking if white pieces attack
            if board._is_square_attacked(row, col):
                white_control += 1
            
            # Check if black controls this square
            board.white_to_move = True  # Checking if black pieces attack
            if board._is_square_attacked(row, col):
                black_control += 1
            
            # Restore original turn
            board.white_to_move = original_turn
    
    return [white_control, black_control]


def get_king_safety_features(board):
    """
    Extract king safety features.
    
    Returns 2 features: number of attackers near each king
    """
    white_king_attackers = 0
    black_king_attackers = 0
    
    # Get king positions
    white_king_row, white_king_col = board.white_king_location
    black_king_row, black_king_col = board.black_king_location
    
    # Save original turn
    original_turn = board.white_to_move
    
    # Check squares around white king
    board.white_to_move = False  # Checking black pieces attacking
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the king's square
            
            row, col = white_king_row + dr, white_king_col + dc
            if 0 <= row < 8 and 0 <= col < 8:
                if board._is_square_attacked(row, col):
                    white_king_attackers += 1
    
    # Check squares around black king
    board.white_to_move = True  # Checking white pieces attacking
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the king's square
            
            row, col = black_king_row + dr, black_king_col + dc
            if 0 <= row < 8 and 0 <= col < 8:
                if board._is_square_attacked(row, col):
                    black_king_attackers += 1
    
    # Restore original turn
    board.white_to_move = original_turn
    
    return [white_king_attackers, black_king_attackers]


def get_pawn_structure_features(board):
    """
    Extract pawn structure features.
    
    Returns 4 features: doubled, isolated, and advanced pawns for each color
    """
    # Count pawns in each file
    white_pawns_in_file = [0] * 8
    black_pawns_in_file = [0] * 8
    
    # Track pawn advancement
    white_pawn_advancement = 0
    black_pawn_advancement = 0
    
    # Count pawns in each file
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col]
            if piece is None or piece.piece_type != 'P':
                continue
            
            if piece.is_white:
                white_pawns_in_file[col] += 1
                # White pawns advance from rank 6 (index 6) towards rank 0
                white_pawn_advancement += (6 - row)  # How far the pawn has advanced
            else:
                black_pawns_in_file[col] += 1
                # Black pawns advance from rank 1 (index 1) towards rank 7
                black_pawn_advancement += (row - 1)  # How far the pawn has advanced
    
    # Count doubled and isolated pawns
    white_doubled = sum(1 for count in white_pawns_in_file if count > 1)
    black_doubled = sum(1 for count in black_pawns_in_file if count > 1)
    
    white_isolated = 0
    black_isolated = 0
    
    for col in range(8):
        # Check if there are pawns in this file
        if white_pawns_in_file[col] > 0:
            # Check if there are pawns in adjacent files
            left_support = col > 0 and white_pawns_in_file[col-1] > 0
            right_support = col < 7 and white_pawns_in_file[col+1] > 0
            
            if not (left_support or right_support):
                white_isolated += white_pawns_in_file[col]
        
        if black_pawns_in_file[col] > 0:
            # Check if there are pawns in adjacent files
            left_support = col > 0 and black_pawns_in_file[col-1] > 0
            right_support = col < 7 and black_pawns_in_file[col+1] > 0
            
            if not (left_support or right_support):
                black_isolated += black_pawns_in_file[col]
    
    return [white_doubled + white_isolated, white_pawn_advancement, 
            black_doubled + black_isolated, black_pawn_advancement]


def get_development_features(board):
    """
    Extract piece development features.
    
    Returns 2 features: development score for each player
    """
    white_development = 0
    black_development = 0
    
    # Check if pieces have moved from their starting positions
    # Knights and bishops contribute to development
    
    # White pieces
    if board.squares[7][1] is None or board.squares[7][1].moved:
        white_development += 1  # Knight moved
    if board.squares[7][6] is None or board.squares[7][6].moved:
        white_development += 1  # Knight moved
    if board.squares[7][2] is None or board.squares[7][2].moved:
        white_development += 1  # Bishop moved
    if board.squares[7][5] is None or board.squares[7][5].moved:
        white_development += 1  # Bishop moved
    
    # Black pieces
    if board.squares[0][1] is None or board.squares[0][1].moved:
        black_development += 1  # Knight moved
    if board.squares[0][6] is None or board.squares[0][6].moved:
        black_development += 1  # Knight moved
    if board.squares[0][2] is None or board.squares[0][2].moved:
        black_development += 1  # Bishop moved
    if board.squares[0][5] is None or board.squares[0][5].moved:
        black_development += 1  # Bishop moved
    
    return [white_development, black_development]


def get_center_control_features(board):
    """
    Extract center control features.
    
    Returns 2 features: center control score for each player
    """
    white_center_control = 0
    black_center_control = 0
    
    # Define center squares
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    
    # Check piece occupation and control of center squares
    for row, col in center_squares:
        piece = board.squares[row][col]
        
        # Piece occupation
        if piece is not None:
            if piece.is_white:
                white_center_control += 2
            else:
                black_center_control += 2
        
        # Square control
        original_turn = board.white_to_move
        
        # Check if white controls this square
        board.white_to_move = False
        if board._is_square_attacked(row, col):
            white_center_control += 1
        
        # Check if black controls this square
        board.white_to_move = True
        if board._is_square_attacked(row, col):
            black_center_control += 1
        
        # Restore original turn
        board.white_to_move = original_turn
    
    return [white_center_control, black_center_control]