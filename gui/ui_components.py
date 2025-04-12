"""
This file contains UI components for the chess game.
"""

import pygame
from gui.theme import colors, get_body_font, get_subtitle_font

def draw_rounded_rect(surface, rect, color, radius=10, border_width=0, border_color=None):
    """
    Draw a rounded rectangle.
    
    Args:
        surface: Pygame surface to draw on
        rect: Rectangle to draw
        color: Color of the rectangle
        radius: Corner radius
        border_width: Width of the border (0 for filled)
        border_color: Color of the border (None for same as fill)
    """
    if border_width > 0 and border_color is None:
        border_color = color
    
    # Ensure radius is not too large
    radius = min(radius, rect.width // 2, rect.height // 2)
    
    # Create rect for each corner
    top_left = pygame.Rect(rect.left, rect.top, radius, radius)
    top_right = pygame.Rect(rect.right - radius, rect.top, radius, radius)
    bottom_left = pygame.Rect(rect.left, rect.bottom - radius, radius, radius)
    bottom_right = pygame.Rect(rect.right - radius, rect.bottom - radius, radius, radius)
    
    # Draw filled rounded rect
    if border_width == 0:
        # Draw main rect
        pygame.draw.rect(
            surface, 
            color, 
            (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height)
        )
        pygame.draw.rect(
            surface, 
            color, 
            (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius)
        )
        
        # Draw corner circles
        pygame.draw.circle(surface, color, top_left.bottomright, radius)
        pygame.draw.circle(surface, color, top_right.bottomleft, radius)
        pygame.draw.circle(surface, color, bottom_left.topright, radius)
        pygame.draw.circle(surface, color, bottom_right.topleft, radius)
    else:
        # Draw border
        inner_rect = rect.inflate(-2 * border_width, -2 * border_width)
        inner_radius = max(0, radius - border_width)
        
        # Draw outer rounded rect
        draw_rounded_rect(surface, rect, border_color, radius)
        
        # Draw inner rounded rect (hole)
        draw_rounded_rect(surface, inner_rect, surface.get_at((0, 0)), inner_radius)

def draw_shadow(surface, rect, offset=(4, 4), blur_radius=5, alpha=50):
    """
    Draw a shadow behind a rectangle.
    
    Args:
        surface: Pygame surface to draw on
        rect: Rectangle to draw shadow for
        offset: Shadow offset (x, y)
        blur_radius: Blur radius for the shadow
        alpha: Shadow opacity (0-255)
    """
    # Create shadow rect
    shadow_rect = pygame.Rect(
        rect.left + offset[0],
        rect.top + offset[1],
        rect.width,
        rect.height
    )
    
    # Create shadow surface with alpha
    shadow_surf = pygame.Surface((shadow_rect.width + 2 * blur_radius, 
                                 shadow_rect.height + 2 * blur_radius), 
                                pygame.SRCALPHA)
    
    # Draw shadow with blur
    for i in range(blur_radius):
        alpha_i = alpha * (blur_radius - i) / blur_radius
        expanded_rect = pygame.Rect(
            blur_radius - i,
            blur_radius - i,
            shadow_rect.width + 2 * i,
            shadow_rect.height + 2 * i
        )
        pygame.draw.rect(
            shadow_surf,
            (0, 0, 0, alpha_i),
            expanded_rect,
            border_radius=10
        )
    
    # Blit shadow to main surface
    surface.blit(
        shadow_surf,
        (shadow_rect.left - blur_radius, shadow_rect.top - blur_radius)
    )

def modern_button(surface, rect, text, color, hover_color, text_color=(255, 255, 255)):
    """
    Draw a modern button with hover effect.
    
    Args:
        surface: Pygame surface to draw on
        rect: Button rectangle
        text: Button text
        color: Button color
        hover_color: Button color when hovered
        text_color: Text color
    """
    # Check if mouse is over button
    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse_pos)
    
    # Draw button shadow
    draw_shadow(surface, rect)
    
    # Draw button
    draw_rounded_rect(
        surface,
        rect,
        hover_color if is_hover else color,
        radius=8
    )
    
    # Draw text
    try:
        font = pygame.font.Font(None, 24)
    except:
        font = pygame.font.SysFont('arial', 24)
    
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    
    surface.blit(text_surf, text_rect)

def draw_panel(surface, rect, title=None):
    """
    Draw a modern panel with optional title.
    
    Args:
        surface: Pygame surface to draw on
        rect: Panel rectangle
        title: Optional panel title
    """
    # Draw panel shadow
    draw_shadow(surface, rect)
    
    # Draw panel background
    draw_rounded_rect(
        surface,
        rect,
        colors['bg_secondary'],
        radius=10
    )
    
    # Draw title if provided
    if title:
        # Get title font
        try:
            title_font = get_subtitle_font()
        except:
            title_font = pygame.font.SysFont('arial', 24)
        
        # Create title text
        title_surf = title_font.render(title, True, colors['text_primary'])
        title_rect = title_surf.get_rect(
            midtop=(rect.centerx, rect.top + 10)
        )
        
        # Draw title
        surface.blit(title_surf, title_rect)
        
        # Draw separator line
        pygame.draw.line(
            surface,
            colors['text_secondary'],
            (rect.left + 20, title_rect.bottom + 5),
            (rect.right - 20, title_rect.bottom + 5),
            1
        )