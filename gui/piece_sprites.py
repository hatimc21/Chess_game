# gui/piece_sprites.py
"""
This file contains the PieceSprites class for managing chess piece images.
"""

import pygame
import os
from gui.theme import colors

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
        """Load all chess piece sprites with modern styling."""
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
                
                # If no valid filename was found, create a modern placeholder
                if not piece_loaded:
                    print(f"No sprite found for {color} {piece_type}, creating modern placeholder")
                    image = self._create_modern_piece(piece_type, color == 'white')
                    
                    # Store the image
                    key = piece_type if color == 'white' else piece_type.lower()
                    self.sprites[key] = image
        
        print(f"Loaded {sprites_loaded} sprites successfully")
    
    def _create_modern_piece(self, piece_type, is_white):
        """
        Create a modern-looking placeholder image for a chess piece.
        
        Args:
            piece_type (str): The type of piece (P, N, B, R, Q, K)
            is_white (bool): Whether the piece is white
            
        Returns:
            Surface: A pygame surface with a modern representation of the piece
        """
        # Create a surface for the piece
        surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        
        # Choose colors - more subtle and modern
        bg_color = (240, 240, 240) if is_white else (60, 60, 70)
        fg_color = (40, 40, 50) if is_white else (220, 220, 230)
        outline_color = (20, 20, 30, 150)  # Semi-transparent outline
        
        # Add subtle shadow
        shadow_radius = self.square_size // 2 - 3
        shadow_center = (self.square_size // 2 + 2, self.square_size // 2 + 2)
        pygame.draw.circle(surface, (0, 0, 0, 40), shadow_center, shadow_radius)
        
        # Draw the main piece body
        center = (self.square_size // 2, self.square_size // 2)
        radius = self.square_size // 2 - 5
        
        # Draw with anti-aliasing if possible
        pygame.draw.circle(surface, bg_color, center, radius)
        
        # Add subtle gradient for 3D effect
        for i in range(radius):
            alpha = 10 - i * 10 / radius
            if alpha > 0:
                pygame.draw.circle(
                    surface, 
                    (255, 255, 255, int(alpha)) if is_white else (0, 0, 0, int(alpha)), 
                    (center[0], center[1] - radius//4), 
                    radius - i,
                    1
                )
        
        # Draw piece-specific details with more refined shapes
        if piece_type.upper() == 'P':  # Pawn
            # Draw a small circle for the head
            head_radius = radius // 2.5
            head_center = (center[0], center[1] - radius // 3)
            pygame.draw.circle(surface, fg_color, head_center, head_radius)
            pygame.draw.circle(surface, outline_color, head_center, head_radius, 1)
            
            # Draw a base
            base_rect = pygame.Rect(
                center[0] - radius // 2, 
                center[1] + radius // 3, 
                radius, 
                radius // 2
            )
            pygame.draw.rect(surface, fg_color, base_rect, border_radius=radius//4)
            pygame.draw.rect(surface, outline_color, base_rect, 1, border_radius=radius//4)
        
        elif piece_type.upper() == 'N':  # Knight
            # Draw a more refined horse head shape
            points = [
                (center[0] - radius // 2, center[1] + radius // 2),  # Bottom left
                (center[0] - radius // 4, center[1] - radius // 4),  # Middle left
                (center[0] - radius // 2, center[1] - radius // 2),  # Top left
                (center[0], center[1] - radius // 1.5),             # Top middle
                (center[0] + radius // 3, center[1] - radius // 3),  # Top right
                (center[0] + radius // 2, center[1] + radius // 4),  # Middle right
                (center[0] + radius // 4, center[1] + radius // 2),  # Bottom right
            ]
            pygame.draw.polygon(surface, fg_color, points)
            pygame.draw.polygon(surface, outline_color, points, 2)
            
            # Draw an eye
            eye_pos = (center[0] - radius // 6, center[1] - radius // 6)
            pygame.draw.circle(surface, outline_color, eye_pos, radius // 8)
        
        elif piece_type.upper() == 'B':  # Bishop
            # Draw a bishop hat with smoother edges
            points = [
                (center[0] - radius // 2, center[1] + radius // 2),  # Bottom left
                (center[0] - radius // 3, center[1]),                # Middle left
                (center[0], center[1] - radius // 1.5),             # Top
                (center[0] + radius // 3, center[1]),                # Middle right
                (center[0] + radius // 2, center[1] + radius // 2),  # Bottom right
            ]
            pygame.draw.polygon(surface, fg_color, points)
            pygame.draw.polygon(surface, outline_color, points, 2)
            
            # Draw a cross on top
            pygame.draw.line(surface, outline_color, 
                            (center[0], center[1] - radius // 1.5), 
                            (center[0], center[1] - radius), 3)
            pygame.draw.line(surface, outline_color, 
                            (center[0] - radius // 6, center[1] - radius // 1.2), 
                            (center[0] + radius // 6, center[1] - radius // 1.2), 2)
        
        elif piece_type.upper() == 'R':  # Rook
            # Draw a castle tower with rounded corners
            tower_rect = pygame.Rect(
                center[0] - radius // 2, 
                center[1] - radius // 2, 
                radius, 
                radius
            )
            pygame.draw.rect(surface, fg_color, tower_rect, border_radius=radius//8)
            pygame.draw.rect(surface, outline_color, tower_rect, 2, border_radius=radius//8)
            
            # Draw battlements
            for i in range(3):
                x = center[0] - radius // 2 + (i * radius // 2)
                battlement_rect = pygame.Rect(
                    x, 
                    center[1] - radius // 2 - radius // 6, 
                    radius // 6, 
                    radius // 6
                )
                pygame.draw.rect(surface, outline_color, battlement_rect, border_radius=2)
        
        elif piece_type.upper() == 'Q':  # Queen
            # Draw a crown with smoother edges
            crown_points = [
                (center[0] - radius // 2, center[1] + radius // 4),  # Bottom left
                (center[0] - radius // 2, center[1] - radius // 4),  # Middle left
                (center[0] - radius // 4, center[1] - radius // 2),  # Top left
                (center[0], center[1] - radius // 3),               # Top middle
                (center[0] + radius // 4, center[1] - radius // 2),  # Top right
                (center[0] + radius // 2, center[1] - radius // 4),  # Middle right
                (center[0] + radius // 2, center[1] + radius // 4),  # Bottom right
            ]
            pygame.draw.polygon(surface, fg_color, crown_points)
            pygame.draw.polygon(surface, outline_color, crown_points, 2)
            
            # Draw points on the crown
            for i in range(3):
                x = center[0] - radius // 3 + (i * radius // 3)
                y = center[1] - radius // 2
                pygame.draw.circle(surface, outline_color, (x, y), radius // 10)
        
        elif piece_type.upper() == 'K':  # King
            # Draw a crown similar to queen but with different top
            crown_points = [
                (center[0] - radius // 2, center[1] + radius // 4),  # Bottom left
                (center[0] - radius // 2, center[1] - radius // 4),  # Middle left
                (center[0] - radius // 4, center[1] - radius // 2),  # Top left
                (center[0], center[1] - radius // 3),               # Top middle
                (center[0] + radius // 4, center[1] - radius // 2),  # Top right
                (center[0] + radius // 2, center[1] - radius // 4),  # Middle right
                (center[0] + radius // 2, center[1] + radius // 4),  # Bottom right
            ]
            pygame.draw.polygon(surface, fg_color, crown_points)
            pygame.draw.polygon(surface, outline_color, crown_points, 2)
            
            # Draw a cross on top
            pygame.draw.line(surface, outline_color, 
                            (center[0], center[1] - radius // 2), 
                            (center[0], center[1] - radius), 3)
            pygame.draw.line(surface, outline_color, 
                            (center[0] - radius // 4, center[1] - radius // 1.3), 
                            (center[0] + radius // 4, center[1] - radius // 1.3), 2)
        
        else:
            # Default: just add the letter with a nicer font
            font = pygame.font.SysFont('Arial', self.square_size // 2, bold=True)
            text = font.render(piece_type.upper(), True, fg_color)
            text_rect = text.get_rect(center=center)
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