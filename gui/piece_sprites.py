# gui/piece_sprites.py
"""
This file contains the PieceSprites class for managing chess piece images.
"""

import pygame
import os


class PieceSprites:
    """
    Class for managing chess piece sprites.
    """
    
    def __init__(self, square_size):
        """
        Initialize the piece sprites manager.
        
        Args:
            square_size (int): Size of the chess square in pixels
        """
        self.square_size = square_size
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Load all chess piece sprites."""
        # Define piece types and colors
        pieces = {
            'P': ['p', 'pawn'],  # Pawn
            'N': ['n', 'knight'],  # Knight
            'B': ['b', 'bishop'],  # Bishop
            'R': ['r', 'rook'],  # Rook
            'Q': ['q', 'queen'],  # Queen
            'K': ['k', 'king']   # King
        }
        colors = ['white', 'black']
        
        # Create directory for pieces if it doesn't exist
        if not os.path.exists('assets/pieces'):
            os.makedirs('assets/pieces', exist_ok=True)
            print("Created assets/pieces directory")
        
        sprites_loaded = 0
        
        # For each piece type and color, try to load the image with different naming conventions
        for color in colors:
            for piece_type, piece_names in pieces.items():
                # Try different naming conventions
                possible_filenames = []
                
                # Full name (white_pawn.png)
                for name in piece_names:
                    possible_filenames.append(f'{color}_{name}.png')
                
                # Abbreviated name (white_p.png)
                for name in piece_names:
                    if len(name) >= 1:
                        possible_filenames.append(f'{color}_{name[0]}.png')
                
                # Try each possible filename
                piece_loaded = False
                for filename in possible_filenames:
                    image_path = f'assets/pieces/{filename}'
                    if os.path.exists(image_path):
                        try:
                            # Load and scale the image
                            image = pygame.image.load(image_path)
                            image = pygame.transform.scale(image, (self.square_size, self.square_size))
                            
                            # Store the image
                            key = piece_type if color == 'white' else piece_type.lower()
                            self.sprites[key] = image
                            
                            print(f"Loaded sprite: {image_path}")
                            piece_loaded = True
                            sprites_loaded += 1
                            break  # Stop trying other filenames for this piece
                        except pygame.error as e:
                            print(f"Error loading {image_path}: {e}")
                
                # If no valid filename was found, create a placeholder
                if not piece_loaded:
                    print(f"No sprite found for {color} {piece_type}, creating placeholder")
                    image = self._create_placeholder_piece(piece_type, color == 'white')
                    
                    # Store the image
                    key = piece_type if color == 'white' else piece_type.lower()
                    self.sprites[key] = image
        
        print(f"Loaded {sprites_loaded} sprites successfully")
    
    def _create_placeholder_piece(self, piece_type, is_white):
        """
        Create a placeholder image for a chess piece.
        
        Args:
            piece_type (str): The type of piece (P, N, B, R, Q, K)
            is_white (bool): Whether the piece is white
            
        Returns:
            Surface: A pygame surface with a simple representation of the piece
        """
        # Create a surface for the piece
        surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        
        # Choose colors
        bg_color = (200, 200, 200) if is_white else (50, 50, 50)
        fg_color = (0, 0, 0) if is_white else (255, 255, 255)
        
        # Draw a circle for the piece
        circle_radius = self.square_size // 2 - 4
        circle_center = (self.square_size // 2, self.square_size // 2)
        pygame.draw.circle(surface, bg_color, circle_center, circle_radius)
        pygame.draw.circle(surface, fg_color, circle_center, circle_radius, 2)
        
        # Add the piece letter
        font = pygame.font.SysFont('Arial', self.square_size // 2)
        text = font.render(piece_type, True, fg_color)
        text_rect = text.get_rect(center=circle_center)
        surface.blit(text, text_rect)
        
        return surface
    
    def get_sprite(self, piece_symbol):
        """
        Get the sprite for a piece.
        
        Args:
            piece_symbol (str): The FEN symbol for the piece (P, N, B, R, Q, K or lowercase)
            
        Returns:
            Surface: The sprite for the piece, or None if not found
        """
        return self.sprites.get(piece_symbol)
    
    def resize(self, new_square_size):
        """
        Resize all sprites to match a new square size.
        
        Args:
            new_square_size (int): The new square size
        """
        self.square_size = new_square_size
        self.load_sprites()