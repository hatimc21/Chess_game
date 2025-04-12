"""
This file contains the BoardDisplay class for rendering the chess board.
"""

import pygame
from gui.theme import colors
from gui.ui_components import draw_rounded_rect, draw_shadow

class PieceSprites:
    """Class for loading and managing chess piece sprites."""
    
    def __init__(self, square_size):
        """
        Initialize piece sprites.
        
        Args:
            square_size (int): Size of a board square in pixels
        """
        self.square_size = square_size
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Load piece sprites from files or create them."""
        # Define piece symbols
        white_pieces = {'P': 'pawn', 'R': 'rook', 'N': 'knight', 
                        'B': 'bishop', 'Q': 'queen', 'K': 'king'}
        black_pieces = {'p': 'pawn', 'r': 'rook', 'n': 'knight', 
                        'b': 'bishop', 'q': 'queen', 'k': 'king'}
        
        # Try to load sprites from files
        try:
            for symbol, name in white_pieces.items():
                sprite = pygame.image.load(f"assets/pieces/white_{name}.png")
                self.sprites[symbol] = pygame.transform.scale(
                    sprite, (self.square_size, self.square_size)
                )
            
            for symbol, name in black_pieces.items():
                sprite = pygame.image.load(f"assets/pieces/black_{name}.png")
                self.sprites[symbol] = pygame.transform.scale(
                    sprite, (self.square_size, self.square_size)
                )
        except:
            # If loading fails, create simple piece representations
            self._create_fallback_sprites(white_pieces, black_pieces)
    
    def _create_fallback_sprites(self, white_pieces, black_pieces):
        """Create simple piece representations if loading sprites fails."""
        # Create a font for piece symbols
        font_size = int(self.square_size * 0.7)
        try:
            font = pygame.font.Font(None, font_size)
        except:
            font = pygame.font.SysFont('arial', font_size)
        
        # Create white pieces
        for symbol, name in white_pieces.items():
            # Create surface
            surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            
            # Draw piece symbol
            text = font.render(symbol, True, (240, 240, 240))
            text_rect = text.get_rect(center=(self.square_size/2, self.square_size/2))
            
            # Draw a circle background
            pygame.draw.circle(
                surf, 
                (200, 200, 200, 200), 
                (self.square_size/2, self.square_size/2), 
                self.square_size/2 - 5
            )
            pygame.draw.circle(
                surf, 
                (240, 240, 240), 
                (self.square_size/2, self.square_size/2), 
                self.square_size/2 - 5, 
                2
            )
            
            surf.blit(text, text_rect)
            self.sprites[symbol] = surf
        
        # Create black pieces
        for symbol, name in black_pieces.items():
            # Create surface
            surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            
            # Draw piece symbol
            text = font.render(symbol.upper(), True, (60, 60, 60))
            text_rect = text.get_rect(center=(self.square_size/2, self.square_size/2))
            
            # Draw a circle background
            pygame.draw.circle(
                surf, 
                (100, 100, 100, 200), 
                (self.square_size/2, self.square_size/2), 
                self.square_size/2 - 5
            )
            pygame.draw.circle(
                surf, 
                (60, 60, 60), 
                (self.square_size/2, self.square_size/2), 
                self.square_size/2 - 5, 
                2
            )
            
            surf.blit(text, text_rect)
            self.sprites[symbol] = surf
    
    def resize(self, square_size):
        """
        Resize all piece sprites.
        
        Args:
            square_size (int): New square size in pixels
        """
        self.square_size = square_size
        
        # Reload sprites with new size
        self.load_sprites()
    
    def get_sprite(self, symbol):
        """
        Get sprite for a piece symbol.
        
        Args:
            symbol (str): Piece symbol (e.g., 'P' for white pawn)
            
        Returns:
            Surface: Piece sprite
        """
        return self.sprites.get(symbol)


class BoardDisplay:
    """Class for rendering the chess board."""
    
    def __init__(self, screen, board_size, margin):
        """
        Initialize the board display.
        
        Args:
            screen: Pygame screen to draw on
            board_size (int): Size of the board in pixels
            margin (int): Margin around the board in pixels
        """
        self.screen = screen
        self.board_size = board_size
        self.margin = margin
        self.square_size = board_size // 8
        
        # Colors
        self.light_square_color = colors['board_light']
        self.dark_square_color = colors['board_dark']
        self.highlight_color = colors['highlight']
        self.move_indicator_color = colors['move_indicator']
        self.check_color = colors['check']
        
        # Load piece sprites
        self.piece_sprites = PieceSprites(self.square_size)
        
        # State
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
    
    def resize(self, board_size, margin):
        """
        Resize the board display.
        
        Args:
            board_size (int): New board size in pixels
            margin (int): New margin around the board in pixels
        """
        self.board_size = board_size
        self.margin = margin
        self.square_size = board_size // 8
        
        # Resize piece sprites
        self.piece_sprites.resize(self.square_size)
    
    def draw_board(self, chess_board, skip_piece=None):
        """
        Draw the chess board with pieces.
        
        Args:
            chess_board: The chess board object
            skip_piece: Optional (row, col) of a piece to skip drawing
        """
        # Draw board background with shadow
        board_rect = pygame.Rect(
            self.margin - 5, 
            self.margin - 5, 
            self.board_size + 10, 
            self.board_size + 10
        )
        
        # Draw shadow
        draw_shadow(self.screen, board_rect)
        
        # Draw board background
        pygame.draw.rect(
            self.screen,
            colors['board_border'],
            board_rect,
            border_radius=5
        )
        
        # Draw rank and file labels
        self._draw_board_labels()
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                # Calculate square position
                x = self.margin + col * self.square_size
                y = self.margin + row * self.square_size
                
                # Determine square color
                is_light = (row + col) % 2 == 0
                square_color = self.light_square_color if is_light else self.dark_square_color
                
                # Draw square
                pygame.draw.rect(
                    self.screen,
                    square_color,
                    (x, y, self.square_size, self.square_size)
                )
                
                # Highlight selected square
                if self.selected_square == (row, col):
                    pygame.draw.rect(
                        self.screen,
                        self.highlight_color,
                        (x, y, self.square_size, self.square_size),
                        3
                    )
                
                # Highlight last move
                if self.last_move:
                    if isinstance(self.last_move, tuple):
                        # The format is ((start_row, start_col), (end_row, end_col))
                        (start_row, start_col), (end_row, end_col) = self.last_move
                    else:
                        # It's a Move object
                        start_row, start_col = self.last_move.start_row, self.last_move.start_col
                        end_row, end_col = self.last_move.end_row, self.last_move.end_col
                    
                    if (row, col) in [(start_row, start_col), (end_row, end_col)]:
                        highlight_surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                        highlight_surf.fill((255, 255, 0, 50))  # Semi-transparent yellow
                        self.screen.blit(highlight_surf, (x, y))
                
                # Draw valid move indicators
                if (row, col) in self.valid_moves:
                    # Draw a circle in the center of the square
                    center_x = x + self.square_size // 2
                    center_y = y + self.square_size // 2
                    radius = self.square_size // 6
                    
                    pygame.draw.circle(
                        self.screen,
                        self.move_indicator_color,
                        (center_x, center_y),
                        radius
                    )
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                # Skip the specified piece if any
                if skip_piece and skip_piece == (row, col):
                    continue
                
                # Get piece at this position
                piece = chess_board.squares[row][col]
                if piece:
                    # Calculate piece position
                    x = self.margin + col * self.square_size
                    y = self.margin + row * self.square_size
                    
                    # Get piece sprite
                    sprite = self.piece_sprites.get_sprite(piece.symbol)
                    if sprite:
                        self.screen.blit(sprite, (x, y))
        
        # Highlight king in check
        if chess_board.is_in_check():
            king_pos = chess_board.white_king_location if chess_board.white_to_move else chess_board.black_king_location
            if king_pos:
                row, col = king_pos
                x = self.margin + col * self.square_size
                y = self.margin + row * self.square_size
                
                # Draw a red glow around the king
                check_surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                
                # Draw multiple circles with decreasing alpha for glow effect
                for i in range(10, 0, -1):
                    alpha = 150 - i * 10
                    pygame.draw.circle(
                        check_surf,
                        (self.check_color[0], self.check_color[1], self.check_color[2], alpha),
                        (self.square_size // 2, self.square_size // 2),
                        self.square_size // 2 - i
                    )
                
                self.screen.blit(check_surf, (x, y))
    
    def _draw_board_labels(self):
        """Draw rank and file labels around the board."""
        # Create font for labels
        try:
            label_font = pygame.font.Font(None, int(self.square_size * 0.4))
        except:
            label_font = pygame.font.SysFont('arial', int(self.square_size * 0.4))
        
        # Draw file labels (a-h)
        for col in range(8):
            file_label = chr(97 + col)  # 'a' through 'h'
            
            # Create text surface
            text_surf = label_font.render(file_label, True, colors['text_primary'])
            text_rect = text_surf.get_rect(
                center=(
                    self.margin + col * self.square_size + self.square_size // 2,
                    self.margin + 8 * self.square_size + 15
                )
            )
            
            # Draw text
            self.screen.blit(text_surf, text_rect)
        
        # Draw rank labels (1-8)
        for row in range(8):
            rank_label = str(8 - row)  # '8' through '1'
            
            # Create text surface
            text_surf = label_font.render(rank_label, True, colors['text_primary'])
            text_rect = text_surf.get_rect(
                center=(
                    self.margin - 15,
                    self.margin + row * self.square_size + self.square_size // 2
                )
            )
            
            # Draw text
            self.screen.blit(text_surf, text_rect)
    
    def handle_click(self, chess_board, pos):
        """
        Handle a click on the board.
        
        Args:
            chess_board: The chess board object
            pos (tuple): (x, y) position of the click
            
        Returns:
            Move or None: The move made, or None if no move was made
        """
        # Check if click is on the board
        board_rect = pygame.Rect(
            self.margin, 
            self.margin, 
            self.board_size, 
            self.board_size
        )
        
        if not board_rect.collidepoint(pos):
            return None
        
        # Convert click position to board coordinates
        col = (pos[0] - self.margin) // self.square_size
        row = (pos[1] - self.margin) // self.square_size
        
        # Ensure coordinates are valid
        if not (0 <= row < 8 and 0 <= col < 8):
            return None
        
        # If a square is already selected
        if self.selected_square:
            # Check if the clicked square is a valid move
            selected_row, selected_col = self.selected_square
            
            # Find the move in valid moves
            move = None
            for valid_move in self.valid_moves:
                if valid_move == (row, col):
                    # Create a move
                    move = chess_board.get_move(selected_row, selected_col, row, col)
                    break
            
            # If a valid move was found, make it
            if move:
                chess_board.make_move(move)
                self.last_move = move
                self.selected_square = None
                self.valid_moves = []
                return move
            else:
                # If not a valid move, select the new square if it has a piece
                piece = chess_board.squares[row][col]
                if piece and ((piece.is_white() and chess_board.white_to_move) or 
                             (not piece.is_white() and not chess_board.white_to_move)):
                    self.selected_square = (row, col)
                    self.valid_moves = chess_board.get_valid_moves_for_piece(row, col)
                else:
                    # Deselect if clicking on an empty square or opponent's piece
                    self.selected_square = None
                    self.valid_moves = []
        else:
            # Select the square if it has a piece of the current player's color
            piece = chess_board.squares[row][col]
            if piece and ((piece.is_white() and chess_board.white_to_move) or 
                         (not piece.is_white() and not chess_board.white_to_move)):
                self.selected_square = (row, col)
                self.valid_moves = chess_board.get_valid_moves_for_piece(row, col)
        
        return None