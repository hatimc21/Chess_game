"""
This file contains visual effects for the chess game.
"""

import pygame

def draw_gradient_background(surface, color1, color2, direction='vertical'):
    """
    Draw a gradient background.
    
    Args:
        surface: Pygame surface to draw on
        color1: Start color (RGB tuple)
        color2: End color (RGB tuple)
        direction: 'vertical' or 'horizontal'
    """
    width, height = surface.get_size()
    
    if direction == 'vertical':
        for y in range(height):
            # Calculate color for this row
            r = color1[0] + (color2[0] - color1[0]) * y / height
            g = color1[1] + (color2[1] - color1[1]) * y / height
            b = color1[2] + (color2[2] - color1[2]) * y / height
            
            # Draw a line with this color
            pygame.draw.line(
                surface,
                (r, g, b),
                (0, y),
                (width, y)
            )
    else:  # horizontal
        for x in range(width):
            # Calculate color for this column
            r = color1[0] + (color2[0] - color1[0]) * x / width
            g = color1[1] + (color2[1] - color1[1]) * x / width
            b = color1[2] + (color2[2] - color1[2]) * x / width
            
            # Draw a line with this color
            pygame.draw.line(
                surface,
                (r, g, b),
                (x, 0),
                (x, height)
            )

def draw_glow_effect(surface, rect, color, radius=20):
    """
    Draw a glow effect around a rectangle.
    
    Args:
        surface: Pygame surface to draw on
        rect: Rectangle to draw glow around
        color: Glow color (RGB tuple)
        radius: Glow radius
    """
    # Create a surface for the glow
    glow_surf = pygame.Surface(
        (rect.width + 2 * radius, rect.height + 2 * radius),
        pygame.SRCALPHA
    )
    
    # Draw multiple circles with decreasing alpha for glow effect
    for i in range(radius, 0, -1):
        alpha = 150 * (1 - i / radius)
        expanded_rect = pygame.Rect(
            radius - i,
            radius - i,
            rect.width + 2 * i,
            rect.height + 2 * i
        )
        pygame.draw.rect(
            glow_surf,
            (color[0], color[1], color[2], alpha),
            expanded_rect,
            border_radius=10
        )
    
    # Blit glow to main surface
    surface.blit(
        glow_surf,
        (rect.left - radius, rect.top - radius)
    )