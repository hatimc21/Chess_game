# create_sprites.py (FIXED)
#!/usr/bin/env python3
"""
Script to create modern chess piece sprites.
"""

import os
import pygame

def create_modern_piece_sprite(piece_type, is_white, size=64):
    """
    Create a modern-looking sprite for a chess piece.
    
    Args:
        piece_type (str): Type of piece (P, N, B, R, Q, K)
        is_white (bool): Whether the piece is white
        size (int): Size of the sprite in pixels
        
    Returns:
        pygame.Surface: The created sprite
    """
    # Initialize pygame if not already initialized
    if not pygame.get_init():
        pygame.init()
        
    # Create a surface with alpha channel
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Choose colors - more subtle and modern
    bg_color = (240, 240, 240) if is_white else (60, 60, 70)
    fg_color = (40, 40, 50) if is_white else (220, 220, 230)
    outline_color = (20, 20, 30, 150)  # Semi-transparent outline
    
    # Add subtle shadow
    shadow_radius = size // 2 - 3
    shadow_center = (size // 2 + 2, size // 2 + 2)
    pygame.draw.circle(surface, (0, 0, 0, 40), shadow_center, shadow_radius)
    
    # Draw the main piece body
    center = (size // 2, size // 2)
    radius = size // 2 - 5
    
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
        font = pygame.font.SysFont('Arial', size // 2, bold=True)
        text = font.render(piece_type.upper(), True, fg_color)
        text_rect = text.get_rect(center=center)
        surface.blit(text, text_rect)
    
    return surface

def create_all_sprites(size=64):
    """
    Create and save all chess piece sprites with modern styling.
    
    Args:
        size (int): Size of the sprites in pixels
    """
    # Create directory if it doesn't exist
    if not os.path.exists('assets/pieces'):
        os.makedirs('assets/pieces', exist_ok=True)
        print("Created assets/pieces directory")
    
    piece_types = ['p', 'n', 'b', 'r', 'q', 'k']
    colors = [True, False]  # White and black
    color_names = {True: 'white', False: 'black'}
    
    for is_white in colors:
        for piece_type in piece_types:
            color = color_names[is_white]
            filename = f"assets/pieces/{color}_{piece_type}.png"
            
            if not os.path.exists(filename):
                print(f"Creating modern sprite: {filename}")
                
                # Create the sprite
                sprite = create_modern_piece_sprite(piece_type, is_white, size)
                
                # Save to file
                pygame.image.save(sprite, filename)
            else:
                print(f"Sprite already exists: {filename}")
    
    print("All modern sprites created successfully!")

if __name__ == "__main__":
    pygame.init()
    create_all_sprites()
    pygame.quit()