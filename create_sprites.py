#!/usr/bin/env python3
"""
Script to create simple placeholder chess piece sprites.
"""

import os
import pygame

def create_piece_sprite(piece_type, is_white, size=64):
    """
    Create a simple placeholder sprite for a chess piece.
    
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
    
    # Choose colors
    bg_color = (230, 230, 230) if is_white else (60, 60, 60)
    fg_color = (30, 30, 30) if is_white else (220, 220, 220)
    outline_color = (0, 0, 0)
    
    # Draw a circle for the piece
    center = (size // 2, size // 2)
    radius = size // 2 - 5
    pygame.draw.circle(surface, bg_color, center, radius)
    pygame.draw.circle(surface, outline_color, center, radius, 2)
    
    # Define piece shapes
    if piece_type.upper() == 'P':  # Pawn
        # Draw a small circle
        pygame.draw.circle(surface, fg_color, (center[0], center[1] - radius // 3), radius // 2.5)
        pygame.draw.circle(surface, outline_color, (center[0], center[1] - radius // 3), radius // 2.5, 1)
        # Draw a base
        pygame.draw.rect(surface, fg_color, (center[0] - radius // 2, center[1] + radius // 3, radius, radius // 2))
        pygame.draw.rect(surface, outline_color, (center[0] - radius // 2, center[1] + radius // 3, radius, radius // 2), 1)
    
    elif piece_type.upper() == 'N':  # Knight
        # Draw a horse head shape
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
        # Draw a bishop hat
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
        # Draw a castle tower
        tower_rect = pygame.Rect(center[0] - radius // 2, center[1] - radius // 2, 
                                 radius, radius)
        pygame.draw.rect(surface, fg_color, tower_rect)
        pygame.draw.rect(surface, outline_color, tower_rect, 2)
        
        # Draw battlements
        for i in range(3):
            x = center[0] - radius // 2 + (i * radius // 2)
            pygame.draw.rect(surface, outline_color, 
                            (x, center[1] - radius // 2 - radius // 6, 
                             radius // 6, radius // 6))
    
    elif piece_type.upper() == 'Q':  # Queen
        # Draw a crown
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
        
        # Draw a ball on top
        pygame.draw.circle(surface, outline_color, 
                          (center[0], center[1] - radius // 2), radius // 8)
    
    elif piece_type.upper() == 'K':  # King
        # Draw a crown similar to queen
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
        # Default: just add the letter
        font = pygame.font.SysFont('Arial', size // 2)
        text = font.render(piece_type.upper(), True, fg_color)
        text_rect = text.get_rect(center=center)
        surface.blit(text, text_rect)
    
    return surface

def create_all_sprites(size=64):
    """
    Create and save all chess piece sprites.
    
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
                print(f"Creating sprite: {filename}")
                
                # Create the sprite
                sprite = create_piece_sprite(piece_type, is_white, size)
                
                # Save to file
                pygame.image.save(sprite, filename)
            else:
                print(f"Sprite already exists: {filename}")
    
    print("All sprites created successfully!")

if __name__ == "__main__":
    pygame.init()
    create_all_sprites()
    pygame.quit()