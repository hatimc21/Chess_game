"""
This file contains theme settings for the chess game.
"""

import pygame

# Color scheme
colors = {
    'bg_primary': (30, 30, 40),
    'bg_secondary': (40, 40, 50),
    'text_primary': (230, 230, 240),
    'text_secondary': (180, 180, 190),
    'accent': (100, 120, 200),
    'accent_light': (120, 140, 220),
    'accent_dark': (80, 100, 180),
    'board_light': (240, 240, 240),
    'board_dark': (120, 120, 140),
    'board_border': (60, 60, 80),
    'highlight': (255, 255, 0),
    'move_indicator': (0, 200, 100, 150),
    'check': (220, 60, 60),
    'checkmate': (220, 60, 60),
    'stalemate': (180, 180, 60)
}

def init_fonts():
    """Initialize fonts for the game."""
    pygame.font.init()

def get_title_font():
    """Get the font for titles."""
    try:
        return pygame.font.Font(None, 48)
    except:
        return pygame.font.SysFont('arial', 48)

def get_subtitle_font():
    """Get the font for subtitles."""
    try:
        return pygame.font.Font(None, 36)
    except:
        return pygame.font.SysFont('arial', 36)

def get_body_font():
    """Get the font for body text."""
    try:
        return pygame.font.Font(None, 24)
    except:
        return pygame.font.SysFont('arial', 24)

def get_small_font():
    """Get the font for small text."""
    try:
        return pygame.font.Font(None, 18)
    except:
        return pygame.font.SysFont('arial', 18)