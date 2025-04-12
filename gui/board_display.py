# gui/board_display.py
"""
This file contains the BoardDisplay class for rendering the chess board and pieces.
"""

import pygame
import os

class BoardDisplay:
    """
    Class for displaying the chess board and handling user interaction with the board.
    """
    
    def __init__(self, screen, board_size=512, margin=20):
        """
        Initialize the board display.
        
        Args:
            screen: Pygame screen to draw on
            board_size (int): Size of the board in pixels
            margin (int): Margin around the board
        """
        self.screen = screen
        self.board_size = board_size
        self.square_size = board_size // 8
        self.margin = margin
        
        # Board colors
        self.light_square = (238, 238, 210)  # Light green
        self.dark_square = (118, 150, 86)    # Dark green
        
        # Highlight colors
        self.selected_color = (100, 149, 237, 180)  # Cornflower blue with alpha
        self.valid_move_color = (255, 255, 0, 120)  # Yellow with alpha
        self.check_color = (255, 0, 0, 150)         # Red with alpha
        
        # Coordinates and labels
        self.show_coordinates = True
        self.coord_font = pygame.font.SysFont('Arial', 14)
        self.coord_color = (0, 0, 0)
        
        # Selected piece and valid moves
        self.selected_square = None
        self.valid_moves = []
        
        # Import and use PieceSprites for piece images
        from gui.piece_sprites import PieceSprites
        self.piece_sprites = PieceSprites(self.square_size)
    
    def draw_board(self, chess_board):
        """
        Draw the chess board with pieces.
        
        Args:
            chess_board: The chess board object containing the game state
        """
        # Draw the squares
        for row in range(8):
            for col in range(8):
                x = self.margin + col * self.square_size
                y = self.margin + row * self.square_size
                
                # Determine square color
                is_light = (row + col) % 2 == 0
                color = self.light_square if is_light else self.dark_square
                
                # Draw the square
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (x, y, self.square_size, self.square_size)
                )
                
                # Draw coordinates if enabled
                if self.show_coordinates:
                    self._draw_coordinates(row, col, x, y)
        
        # Highlight the selected square if any
        if self.selected_square:
            row, col = self.selected_square
            x = self.margin + col * self.square_size
            y = self.margin + row * self.square_size
            
            # Create a transparent surface for the highlight
            highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            highlight.fill(self.selected_color)
            self.screen.blit(highlight, (x, y))
        
        # Highlight valid moves if any
        for move in self.valid_moves:
            end_row, end_col = move.end_row, move.end_col
            x = self.margin + end_col * self.square_size
            y = self.margin + end_row * self.square_size
            
            # Create a transparent surface for the highlight
            highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            highlight.fill(self.valid_move_color)
            self.screen.blit(highlight, (x, y))
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                piece = chess_board.squares[row][col]
                if piece:
                    self._draw_piece(piece, row, col)
        
        # Highlight king in check
        if chess_board._is_in_check():
            king_row, king_col = chess_board.white_king_location if chess_board.white_to_move else chess_board.black_king_location
            x = self.margin + king_col * self.square_size
            y = self.margin + king_row * self.square_size
            
            # Create a transparent surface for the highlight
            highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            highlight.fill(self.check_color)
            self.screen.blit(highlight, (x, y))
    
    def _draw_coordinates(self, row, col, x, y):
        """Draw board coordinates."""
        # Draw file (column) labels at the bottom
        if row == 7:
            label = chr(ord('a') + col)
            text = self.coord_font.render(label, True, self.coord_color)
            self.screen.blit(
                text, 
                (x + self.square_size - 12, y + self.square_size - 15)
            )
        
        # Draw rank (row) labels on the left
        if col == 0:
            label = str(8 - row)
            text = self.coord_font.render(label, True, self.coord_color)
            self.screen.blit(text, (x + 5, y + 5))
    
    def _draw_piece(self, piece, row, col):
        """Draw a chess piece on the board."""
        x = self.margin + col * self.square_size
        y = self.margin + row * self.square_size
        
        # Get the appropriate piece image
        piece_symbol = piece.symbol
        piece_img = self.piece_sprites.get_sprite(piece_symbol)
        
        if piece_img:
            self.screen.blit(piece_img, (x, y))
        else:
            print(f"Warning: No sprite found for piece {piece_symbol}")
    
    def handle_click(self, chess_board, pos):
        """
        Handle a mouse click on the board.
        
        Args:
            chess_board: The chess board object containing the game state
            pos (tuple): (x, y) position of the click
            
        Returns:
            tuple: (from_square, to_square) if a move was made, otherwise None
        """
        # Check if click is within the board
        if not (self.margin <= pos[0] <= self.margin + self.board_size and
                self.margin <= pos[1] <= self.margin + self.board_size):
            return None
        
        # Convert click position to board coordinates
        col = (pos[0] - self.margin) // self.square_size
        row = (pos[1] - self.margin) // self.square_size
        
        # If a square is already selected
        if self.selected_square:
            previous_row, previous_col = self.selected_square
            
            # Check if the clicked square is a valid move
            move_made = False
            for move in self.valid_moves:
                if move.end_row == row and move.end_col == col:
                    # Make the move
                    chess_board.make_move(move)
                    move_made = True
                    
                    # Reset selection
                    result = (self.selected_square, (row, col))
                    self.selected_square = None
                    self.valid_moves = []
                    return result
            
            # If not a valid move, check if it's another piece of the same color
            if not move_made:
                piece = chess_board.squares[row][col]
                if piece and ((piece.is_white and chess_board.white_to_move) or
                              (not piece.is_white and not chess_board.white_to_move)):
                    # Select this piece instead
                    self.selected_square = (row, col)
                    self.valid_moves = self._get_valid_moves_for_piece(chess_board, row, col)
                else:
                    # Deselect if clicking on empty square or opponent's piece
                    self.selected_square = None
                    self.valid_moves = []
        else:
            # First selection - check if there's a piece of the correct color
            piece = chess_board.squares[row][col]
            if piece and ((piece.is_white and chess_board.white_to_move) or
                         (not piece.is_white and not chess_board.white_to_move)):
                self.selected_square = (row, col)
                self.valid_moves = self._get_valid_moves_for_piece(chess_board, row, col)
        
        return None
    
    def _get_valid_moves_for_piece(self, chess_board, row, col):
        """Get valid moves for the piece at the given position."""
        # Get all valid moves for the current player
        all_valid_moves = chess_board.get_valid_moves()
        
        # Filter moves for the selected piece
        piece_moves = []
        for move in all_valid_moves:
            if move.start_row == row and move.start_col == col:
                piece_moves.append(move)
        
        return piece_moves