"""
This file contains UI components for the chess game.
"""

import pygame
from gui.theme import colors, get_body_font, get_subtitle_font

class PromotionSelector:
    """UI component for selecting a piece for pawn promotion."""
    
    def __init__(self, screen, theme, square_size):
        """
        Initialize the promotion selector.
        
        Args:
            screen: Pygame screen
            theme: Theme object
            square_size: Size of a chess square
        """
        self.screen = screen
        self.theme = theme
        self.square_size = square_size
        self.active = False
        self.is_white = True
        self.col = 0
        self.row = 0
        self.selected_piece = None
        
        # Load piece images
        self.piece_images = {}
        self._load_piece_images()
    
    def _load_piece_images(self):
        """Load piece images for the promotion selector."""
        # Map piece codes to filenames with correct paths
        piece_filenames = {
            'wQ': 'assets/pieces/white_queen.png',
            'wR': 'assets/pieces/white_rook.png',
            'wB': 'assets/pieces/white_bishop.png',
            'wN': 'assets/pieces/white_knight.png',
            'bQ': 'assets/pieces/black_queen.png',
            'bR': 'assets/pieces/black_rook.png',
            'bB': 'assets/pieces/black_bishop.png',
            'bN': 'assets/pieces/black_knight.png'
        }
        
        # Load each piece image with error handling
        for piece_code, filename in piece_filenames.items():
            try:
                self.piece_images[piece_code] = pygame.transform.scale(
                    pygame.image.load(filename),
                    (self.square_size, self.square_size)
                )
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
                # Create a fallback colored rectangle with text
                surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                color = (255, 255, 255) if piece_code.startswith('w') else (0, 0, 0)
                pygame.draw.rect(surf, color, (0, 0, self.square_size, self.square_size))
                font = pygame.font.SysFont('Arial', int(self.square_size * 0.7))
                text = font.render(piece_code[1], True, (0, 0, 0) if piece_code.startswith('w') else (255, 255, 255))
                text_rect = text.get_rect(center=(self.square_size//2, self.square_size//2))
                surf.blit(text, text_rect)
                self.piece_images[piece_code] = surf
    
    def show(self, row, col, is_white):
        """
        Show the promotion selector.
        
        Args:
            row (int): Row of the pawn
            col (int): Column of the pawn
            is_white (bool): Whether the pawn is white
        """
        self.active = True
        self.is_white = is_white
        self.col = col
        self.row = row
        self.selected_piece = None
    
    def hide(self):
        """Hide the promotion selector."""
        self.active = False
    
    def draw(self):
        """Draw the promotion selector with modern styling."""
        if not self.active:
            return
        
        # Determine the position of the selector
        # For white pawns (moving up), show above the pawn
        # For black pawns (moving down), show below the pawn
        start_row = self.row - 4 if self.is_white else self.row
        if start_row < 0:
            start_row = 0
        if start_row > 4:
            start_row = 4
        
        # Calculate selector dimensions and position
        selector_height = 4 * self.square_size
        selector_width = self.square_size
        
        # Calculate board offset to center the board on screen
        screen_width, screen_height = self.screen.get_size()
        board_size = 8 * self.square_size
        board_offset_x = (screen_width - board_size) // 2
        board_offset_y = (screen_height - board_size) // 2
        
        # Apply board offset to selector position
        selector_x = board_offset_x + self.col * self.square_size
        selector_y = board_offset_y + start_row * self.square_size
        
        # Draw shadow effect
        shadow_offset = 5
        shadow_rect = pygame.Rect(
            selector_x + shadow_offset, 
            selector_y + shadow_offset, 
            selector_width, 
            selector_height
        )
        pygame.draw.rect(
            self.screen,
            (0, 0, 0, 128),  # Semi-transparent black
            shadow_rect,
            border_radius=10
        )
        
        # Draw main background
        main_rect = pygame.Rect(
            selector_x, 
            selector_y, 
            selector_width, 
            selector_height
        )
        pygame.draw.rect(
            self.screen,
            (240, 240, 240),  # Light background
            main_rect,
            border_radius=10
        )
        
        # Draw border
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),  # Dark border
            main_rect,
            2,
            border_radius=10
        )
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 14)
        title_text = title_font.render("Promote to:", True, (0, 0, 0))
        title_rect = title_text.get_rect(midtop=(selector_x + selector_width//2, selector_y + 5))
        self.screen.blit(title_text, title_rect)
        
        # Draw pieces
        pieces = ['Q', 'R', 'B', 'N']
        prefix = 'w' if self.is_white else 'b'
        
        for i, piece in enumerate(pieces):
            piece_key = f'{prefix}{piece}'
            piece_y = selector_y + 25 + i * self.square_size
            
            # Draw piece background
            piece_rect = pygame.Rect(
                selector_x + 5,
                piece_y,
                selector_width - 10,
                self.square_size - 5
            )
            
            # Highlight on hover
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = piece_rect.collidepoint(mouse_pos)
            
            # Draw piece background
            bg_color = (220, 220, 220) if is_hovered else (240, 240, 240)
            pygame.draw.rect(
                self.screen,
                bg_color,
                piece_rect,
                border_radius=5
            )
            
            # Draw piece image centered in the rect
            img_x = selector_x + (selector_width - self.square_size) // 2
            self.screen.blit(self.piece_images[piece_key], (img_x, piece_y))
    
    def handle_click(self, pos):
        """
        Handle a click on the promotion selector.
        
        Args:
            pos (tuple): (x, y) position of the click
            
        Returns:
            str or None: The selected piece ('Q', 'R', 'B', 'N') or None if no selection
        """
        if not self.active:
            return None
        
        # Determine the position of the selector
        start_row = self.row - 4 if self.is_white else self.row
        if start_row < 0:
            start_row = 0
        if start_row > 4:
            start_row = 4
        
        # Calculate selector dimensions and position
        selector_height = 4 * self.square_size
        selector_width = self.square_size
        
        # Calculate board offset to center the board on screen
        screen_width, screen_height = self.screen.get_size()
        board_size = 8 * self.square_size
        board_offset_x = (screen_width - board_size) // 2
        board_offset_y = (screen_height - board_size) // 2
        
        # Apply board offset to selector position
        selector_x = board_offset_x + self.col * self.square_size
        selector_y = board_offset_y + start_row * self.square_size
        
        # Check if click is within selector
        x, y = pos
        if not (selector_x <= x < selector_x + selector_width and
                selector_y <= y < selector_y + selector_height):
            return None
        
        # Account for the title space
        y_offset = 25
        
        # Determine which piece was clicked
        pieces = ['Q', 'R', 'B', 'N']
        for i, piece in enumerate(pieces):
            piece_y = selector_y + y_offset + i * self.square_size
            piece_rect = pygame.Rect(
                selector_x + 5,
                piece_y,
                selector_width - 10,
                self.square_size - 5
            )
            
            if piece_rect.collidepoint(x, y):
                self.selected_piece = piece
                self.hide()
                return piece
        
        return None

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
