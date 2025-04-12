"""
This file contains the GameScreen class for managing the main game display.
"""

import pygame
import time
from gui.board_display import BoardDisplay
from gui.theme import colors, get_title_font, get_subtitle_font, get_body_font, get_small_font
from gui.ui_components import modern_button, draw_panel, draw_rounded_rect, draw_shadow
from gui.effects import draw_gradient_background, draw_glow_effect
from gui.animations import animate_piece_movement, fade_transition

class GameScreen:
    """
    Class for managing the main game display and user interface.
    """
    
    def __init__(self, screen, width, height):
        """
        Initialize the game screen.
        
        Args:
            screen: Pygame screen to draw on
            width (int): Screen width
            height (int): Screen height
        """
        self.screen = screen
        self.width = width
        self.height = height
        
        # Colors from theme
        self.bg_color = colors['bg_primary']
        self.text_color = colors['text_primary']
        self.button_color = colors['accent']
        self.button_hover_color = colors['accent_light']
        
        # Fonts
        self.title_font = get_title_font()
        self.subtitle_font = get_subtitle_font()
        self.info_font = get_body_font()
        self.button_font = get_body_font()
        self.small_font = get_small_font()
        
        # Determine board size
        self.board_size = min(width - 300, height - 100)
        self.board_margin = 30
        
        # Initialize board display
        self.board_display = BoardDisplay(screen, self.board_size, self.board_margin)
        
        # Game state information
        self.game_state = "ongoing"
        self.current_player = "White"
        
        # Animation state
        self.animating = False
        self.animation_start = None
        self.animation_end = None
        
        # Buttons
        self.buttons = {}
        self.buttons_bottom = 0  # Will be set in init_buttons
        self.init_buttons()
        
        # Move history scrolling
        self.move_scroll_offset = 0
        self.max_visible_moves = 8
        self.scroll_up_rect = None
        self.scroll_down_rect = None
        
        # Checkmate notification
        self.show_checkmate_notification = False
        self.checkmate_notification_time = 0
        self.checkmate_notification_duration = 3.0  # seconds
        self.winner = None
    
    def init_buttons(self):
        """Initialize UI buttons with modern styling."""
        # Button dimensions
        button_width = 180
        button_height = 45
        button_margin = 12
        
        # Button positions - right side of the board
        buttons_x = self.board_margin + self.board_size + 40
        
        # Position buttons at the top part of the side panel
        # Start buttons closer to the top to leave space for move history
        buttons_y = self.board_margin + 120
        
        # Calculate total height needed for all buttons
        total_buttons_height = 6 * button_height + 5 * button_margin
        
        # New Game button
        self.buttons["new_game"] = {
            "rect": pygame.Rect(buttons_x, buttons_y, button_width, button_height),
            "text": "New Game",
            "action": "new_game",
            "color": colors['accent'],
            "hover_color": colors['accent_light']
        }
        
        # Undo Move button
        self.buttons["undo"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + button_height + button_margin, 
                                button_width, button_height),
            "text": "Undo Move",
            "action": "undo",
            "color": colors['accent'],
            "hover_color": colors['accent_light']
        }
        
        # AI Move button
        self.buttons["ai_move"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 2 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "AI Move",
            "action": "ai_move",
            "color": colors['accent'],
            "hover_color": colors['accent_light']
        }
        
        # Save Game button
        self.buttons["save"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 3 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "Save Game",
            "action": "save",
            "color": colors['accent'],
            "hover_color": colors['accent_light']
        }
        
        # Load Game button
        self.buttons["load"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 4 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "Load Game",
            "action": "load",
            "color": colors['accent'],
            "hover_color": colors['accent_light']
        }
        
        # Quit button
        self.buttons["quit"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 5 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "Quit",
            "action": "quit",
            "color": colors['accent_dark'],
            "hover_color": colors['accent']
        }
        
        # Store the bottom position of the last button for reference in draw_game_info
        self.buttons_bottom = buttons_y + 5 * (button_height + button_margin) + button_height
    
    def draw(self, chess_board):
        """
        Draw the game screen.
        
        Args:
            chess_board: The chess board object containing the game state
        """
        # Fill the background with gradient
        draw_gradient_background(
            self.screen, 
            colors['bg_primary'], 
            (colors['bg_primary'][0]-10, colors['bg_primary'][1]-10, colors['bg_primary'][2]-10)
        )
        
        # Draw the chess board
        self.board_display.draw_board(chess_board)
        
        # Draw game information
        self.draw_game_info(chess_board)
        
        # Draw buttons
        self.draw_buttons()
        
        # Draw checkmate notification if active
        if self.show_checkmate_notification:
            self.draw_checkmate_notification()
            
            # Check if notification duration has passed
            current_time = time.time()
            if current_time - self.checkmate_notification_time > self.checkmate_notification_duration:
                self.show_checkmate_notification = False
        
        # Update the display
        pygame.display.flip()
    
    def draw_game_info(self, chess_board):
        """Draw modern game information panel."""
        # Create panel for game info
        panel_rect = pygame.Rect(
            self.board_margin + self.board_size + 20,
            self.board_margin,
            self.width - (self.board_margin + self.board_size + 40),
            100
        )
        
        draw_panel(self.screen, panel_rect, "Chess Game")
        
        # Current player with colored indicator
        player = "White" if chess_board.white_to_move else "Black"
        player_color = (240, 240, 240) if chess_board.white_to_move else (60, 60, 70)
        
        # Player indicator circle
        pygame.draw.circle(
            self.screen,
            player_color,
            (panel_rect.x + 30, panel_rect.y + 70),
            10
        )
        pygame.draw.circle(
            self.screen,
            colors['text_primary'],
            (panel_rect.x + 30, panel_rect.y + 70),
            10,
            1
        )
        
        player_text = self.info_font.render(f"Current Player: {player}", True, colors['text_primary'])
        self.screen.blit(player_text, (panel_rect.x + 50, panel_rect.y + 62))
        
        # Game state with appropriate styling
        state = "Checkmate" if chess_board.checkmate else "Stalemate" if chess_board.stalemate else "Ongoing"
        state_color = colors['check'] if state == "Checkmate" else colors['text_secondary']
        state_text = self.info_font.render(f"Game State: {state}", True, state_color)
        self.screen.blit(state_text, (panel_rect.x + 20, panel_rect.y + 95))
        
        # Check for checkmate and show notification
        if chess_board.checkmate and not self.show_checkmate_notification:
            self.show_checkmate_notification = True
            self.checkmate_notification_time = time.time()
            self.winner = "Black" if chess_board.white_to_move else "White"
        
        # Move history in a scrollable-looking area
        # Position it below the buttons with some margin
        history_rect = pygame.Rect(
            panel_rect.x,
            self.buttons_bottom + 20,  # Position it below the last button with margin
            panel_rect.width,
            self.height - (self.buttons_bottom + 40)  # Use remaining space with margins
        )
        
        # Make sure the history panel isn't too small
        if history_rect.height < 100:
            history_rect.height = 100
        
        draw_panel(self.screen, history_rect, "Move History")
        
        # Draw scrollable move history
        self.draw_scrollable_move_history(chess_board, history_rect)
    
    def draw_scrollable_move_history(self, chess_board, history_rect):
        """
        Draw a scrollable move history panel.
        
        Args:
            chess_board: The chess board object
            history_rect: Rectangle for the history panel
        """
        # Calculate visible area for moves
        visible_area_rect = pygame.Rect(
            history_rect.x + 10,
            history_rect.y + 40,
            history_rect.width - 20,
            history_rect.height - 50
        )
        
        # Draw a subtle background for the scrollable area
        draw_rounded_rect(
            self.screen,
            visible_area_rect,
            (colors['bg_secondary'][0] - 10, colors['bg_secondary'][1] - 10, colors['bg_secondary'][2] - 10),
            radius=8
        )
        
        # Calculate max scroll offset based on number of moves
        move_count = len(chess_board.move_log)
        max_scroll = max(0, move_count - self.max_visible_moves)
        
        # Clamp scroll offset
        self.move_scroll_offset = max(0, min(self.move_scroll_offset, max_scroll))
        
        # Draw scroll buttons if needed
        button_size = 24
        button_margin = 5
        
        # Only show scroll buttons if there are more moves than can be displayed
        if move_count > self.max_visible_moves:
            # Up scroll button
            self.scroll_up_rect = pygame.Rect(
                history_rect.right - button_size - button_margin,
                history_rect.y + 40,
                button_size,
                button_size
            )
            
            # Down scroll button
            self.scroll_down_rect = pygame.Rect(
                history_rect.right - button_size - button_margin,
                history_rect.y + 40 + visible_area_rect.height - button_size,
                button_size,
                button_size
            )
            
            # Draw up button
            up_enabled = self.move_scroll_offset > 0
            up_color = colors['accent'] if up_enabled else colors['text_secondary']
            draw_rounded_rect(self.screen, self.scroll_up_rect, up_color, radius=5)
            
            # Draw up arrow
            arrow_points = [
                (self.scroll_up_rect.centerx, self.scroll_up_rect.y + 8),
                (self.scroll_up_rect.x + 6, self.scroll_up_rect.centery),
                (self.scroll_up_rect.right - 6, self.scroll_up_rect.centery)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 255), arrow_points)
            
            # Draw down button
            down_enabled = self.move_scroll_offset < max_scroll
            down_color = colors['accent'] if down_enabled else colors['text_secondary']
            draw_rounded_rect(self.screen, self.scroll_down_rect, down_color, radius=5)
            
            # Draw down arrow
            arrow_points = [
                (self.scroll_down_rect.centerx, self.scroll_down_rect.bottom - 8),
                (self.scroll_down_rect.x + 6, self.scroll_down_rect.centery),
                (self.scroll_down_rect.right - 6, self.scroll_down_rect.centery)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 255), arrow_points)
        else:
            # No scroll buttons needed
            self.scroll_up_rect = None
            self.scroll_down_rect = None
        
        # Display moves in a more structured format
        if move_count > 0:
            # Calculate visible range
            start_index = self.move_scroll_offset
            end_index = min(move_count, start_index + self.max_visible_moves)
            
            # Draw scroll position indicator
            if move_count > self.max_visible_moves:
                # Calculate indicator position and size
                indicator_height = (visible_area_rect.height - 2 * button_size - 20) * self.max_visible_moves / move_count
                indicator_y = visible_area_rect.y + button_size + 10 + (visible_area_rect.height - 2 * button_size - 20 - indicator_height) * self.move_scroll_offset / max_scroll
                
                indicator_rect = pygame.Rect(
                    history_rect.right - button_size//2 - button_margin,
                    indicator_y,
                    button_size//4,
                    max(10, indicator_height)
                )
                
                # Draw indicator
                draw_rounded_rect(self.screen, indicator_rect, colors['accent_light'], radius=3)
            
            # Draw visible moves
            for i, move in enumerate(chess_board.move_log[start_index:end_index]):
                move_num = start_index + i + 1
                player_symbol = "W" if move_num % 2 == 1 else "B"
                move_color = colors['text_primary'] if player_symbol == "W" else colors['text_secondary']
                
                # Make sure the move has get_chess_notation method
                notation = move.get_chess_notation() if hasattr(move, 'get_chess_notation') else f"{move.start_row},{move.start_col} → {move.end_row},{move.end_col}"
                
                # Check if this move resulted in check or checkmate
                is_check = False
                is_checkmate = False
                
                # This is a simplification - in a real implementation, you'd need to check the board state after this move
                if i + 1 == len(chess_board.move_log) and chess_board.checkmate:
                    is_checkmate = True
                    notation += "#"  # Chess notation for checkmate
                elif hasattr(move, 'is_check') and move.is_check:
                    is_check = True
                    notation += "+"  # Chess notation for check
                
                # Create move text
                move_text = self.small_font.render(
                    f"{move_num}. {player_symbol}: {notation}", 
                    True, 
                    colors['check'] if is_checkmate else (colors['accent'] if is_check else move_color)
                )
                
                # Calculate position
                move_y = visible_area_rect.y + 10 + i * 24
                
                # Draw move background if it's checkmate or check
                if is_checkmate or is_check:
                    move_bg_rect = pygame.Rect(
                        visible_area_rect.x + 5,
                        move_y - 2,
                        visible_area_rect.width - 10 - (button_size + button_margin if self.scroll_up_rect else 0),
                        24
                    )
                    bg_color = colors['check'] if is_checkmate else colors['accent_light']
                    bg_color = (bg_color[0], bg_color[1], bg_color[2], 100)  # Add transparency
                    
                    # Create a surface with per-pixel alpha
                    bg_surf = pygame.Surface((move_bg_rect.width, move_bg_rect.height), pygame.SRCALPHA)
                    bg_surf.fill(bg_color)
                    self.screen.blit(bg_surf, move_bg_rect)
                
                # Draw move text
                self.screen.blit(
                    move_text, 
                    (visible_area_rect.x + 10, move_y)
                )
        else:
            # Display a message when no moves have been made
            no_moves_text = self.small_font.render(
                "No moves yet", 
                True, 
                colors['text_secondary']
            )
            self.screen.blit(
                no_moves_text, 
                (history_rect.x + 15, history_rect.y + 50)
            )
    
    def handle_scroll(self, pos, is_wheel=False, wheel_dir=0):
        """
        Handle scrolling of the move history.
        
        Args:
            pos: Mouse position (x, y)
            is_wheel: Whether this is a mouse wheel event
            wheel_dir: Direction of wheel scroll (1 for up, -1 for down)
            
        Returns:
            bool: True if scroll was handled
        """
        # If using mouse wheel
        if is_wheel:
            # Scroll up (wheel up)
            if wheel_dir > 0:
                self.move_scroll_offset = max(0, self.move_scroll_offset - 1)
                return True
            # Scroll down (wheel down)
            elif wheel_dir < 0:
                self.move_scroll_offset += 1
                return True
            return False
        
        # If using scroll buttons
        if self.scroll_up_rect and self.scroll_up_rect.collidepoint(pos):
            self.move_scroll_offset = max(0, self.move_scroll_offset - 1)
            return True
        elif self.scroll_down_rect and self.scroll_down_rect.collidepoint(pos):
            self.move_scroll_offset += 1
            return True
        
        return False
    
    def draw_checkmate_notification(self):
        """Draw a notification when checkmate occurs."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Create notification panel
        panel_width = 400
        panel_height = 200
        panel_rect = pygame.Rect(
            (self.width - panel_width) // 2,
            (self.height - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Draw shadow
        draw_shadow(self.screen, panel_rect, alpha=60)
        
        # Draw panel with glow effect
        draw_glow_effect(self.screen, panel_rect, colors['check'], radius=20)
        draw_rounded_rect(self.screen, panel_rect, colors['bg_primary'], radius=15)
        
        # Draw title
        title_text = self.title_font.render("Checkmate!", True, colors['check'])
        title_rect = title_text.get_rect(centerx=panel_rect.centerx, top=panel_rect.y + 30)
        self.screen.blit(title_text, title_rect)
        
        # Draw winner
        winner_text = self.subtitle_font.render(f"{self.winner} wins!", True, colors['text_primary'])
        winner_rect = winner_text.get_rect(centerx=panel_rect.centerx, top=title_rect.bottom + 20)
        self.screen.blit(winner_text, winner_rect)
        
        # Draw button
        button_rect = pygame.Rect(
            panel_rect.centerx - 75,
            panel_rect.bottom - 60,
            150,
            40
        )
        
        modern_button(
            self.screen,
            button_rect,
            "New Game",
            colors['accent'],
            colors['accent_light'],
            text_color=(255, 255, 255)
        )
    
    def handle_checkmate_click(self, pos):
        """
        Handle clicks on the checkmate notification.
        
        Args:
            pos: Mouse position (x, y)
            
        Returns:
            str: Action to perform, or None
        """
        if not self.show_checkmate_notification:
            return None
        
        # Check if New Game button was clicked
        button_rect = pygame.Rect(
            self.width // 2 - 75,
            self.height // 2 + 40,
            150,
            40
        )
        
        if button_rect.collidepoint(pos):
            self.show_checkmate_notification = False
            return "new_game"
        
        return None
    
    def draw_buttons(self):
        """Draw modern UI buttons."""
        for button_info in self.buttons.values():
            modern_button(
                self.screen,
                button_info["rect"],
                button_info["text"],
                button_info["color"],
                button_info["hover_color"],
                text_color=(255, 255, 255)
            )
    
    def handle_button_click(self, pos):
        """
        Handle button clicks.
        
        Args:
            pos (tuple): (x, y) position of the click
            
        Returns:
            str: The action to perform, or None if no button was clicked
        """
        # Check for checkmate notification clicks first
        checkmate_action = self.handle_checkmate_click(pos)
        if checkmate_action:
            return checkmate_action
        
        # Check for scroll button clicks
        if self.handle_scroll(pos):
            return None
        
        # Check regular buttons
        for button_info in self.buttons.values():
            if button_info["rect"].collidepoint(pos):
                return button_info["action"]
        
        return None
    
    def resize(self, width, height):
        """
        Resize the game screen with responsive layout.
        
        Args:
            width (int): New screen width
            height (int): New screen height
        """
        self.width = width
        self.height = height
        
        # Calculate optimal board size based on screen dimensions
        # Ensure the board is square and fits comfortably
        min_dimension = min(width * 0.7, height * 0.9)
        self.board_size = int(min_dimension)
        self.board_margin = int(min((width - self.board_size) * 0.1, (height - self.board_size) * 0.5))
        
        # Ensure the board margin is at least 20 pixels
        self.board_margin = max(20, self.board_margin)
        
        # Resize board display
        self.board_display.resize(self.board_size, self.board_margin)
        
        # Reinitialize buttons
        self.init_buttons()
    
    def animate_move(self, chess_board, move):
        """
        Animate a chess piece moving from start to end position.
        
        Args:
            chess_board: The chess board object
            move: The move to animate (can be a Move object or a tuple)
        """
        # Check if move is a tuple or a Move object
        if isinstance(move, tuple):
            # The format is ((start_row, start_col), (end_row, end_col))
            (start_row, start_col), (end_row, end_col) = move
        else:
            # It's a Move object
            start_row, start_col = move.start_row, move.start_col
            end_row, end_col = move.end_row, move.end_col
        
        # Get piece and positions
        piece = chess_board.squares[end_row][end_col]
        if not piece:
            return
            
        start_x = self.board_margin + start_col * self.board_display.square_size
        start_y = self.board_margin + start_row * self.board_display.square_size
        end_x = self.board_margin + end_col * self.board_display.square_size
        end_y = self.board_margin + end_row * self.board_display.square_size
        
        # Get piece sprite
        piece_img = self.board_display.piece_sprites.get_sprite(piece.symbol)
        if not piece_img:
            return
            
        # Define a function to draw the background (board without the moving piece)
        def draw_background():
            # Fill background
            self.screen.fill(self.bg_color)
            
            # Draw board without the moving piece
            self.board_display.draw_board(chess_board, skip_piece=(end_row, end_col))
            
            # Draw game info
            self.draw_game_info(chess_board)
            
            # Draw buttons
            self.draw_buttons()
        
        # Animate the piece movement
        animate_piece_movement(
            self.screen,
            draw_background,
            (start_x, start_y),
            (end_x, end_y),
            piece_img,
            duration=0.2
        )
    
    def draw_menu(self):
        """Draw a modern menu screen."""
        # Gradient background
        draw_gradient_background(
            self.screen, 
            colors['bg_primary'], 
            (colors['bg_primary'][0]-15, colors['bg_primary'][1]-15, colors['bg_primary'][2]-15)
        )
        
        # Title with shadow
        title_surf = self.title_font.render("Chess Game", True, colors['accent'])
        shadow_surf = self.title_font.render("Chess Game", True, (0, 0, 0, 100))
        
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        shadow_rect = shadow_surf.get_rect(center=(self.width // 2 + 2, 102))
        
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)
        
        # Draw modern buttons
        button_width, button_height = 220, 50
        button_margin = 16
        button_x = self.width // 2 - button_width // 2
        
        buttons = [
            {"text": "Player vs Player", "action": "pvp", "color": colors['accent']},
            {"text": "Play as White", "action": "white", "color": colors['accent']},
            {"text": "Play as Black", "action": "black", "color": colors['accent']},
            {"text": "Options", "action": "options", "color": colors['accent']},
            {"text": "Quit", "action": "quit", "color": colors['accent_dark']}
        ]
        
        for i, button in enumerate(buttons):
            button_rect = pygame.Rect(
                button_x, 
                200 + i * (button_height + button_margin),
                button_width, 
                button_height
            )
            modern_button(
                self.screen,
                button_rect,
                button["text"],
                button["color"],
                colors['accent_light'],
                text_color=(255, 255, 255)
            )
        
        pygame.display.flip()
    
    def draw_options(self, ai_difficulty):
        """Draw a modern options screen."""
        # Gradient background
        draw_gradient_background(
            self.screen, 
            colors['bg_primary'], 
            (colors['bg_primary'][0]-15, colors['bg_primary'][1]-15, colors['bg_primary'][2]-15)
        )
        
        # Title
        title_surf = self.title_font.render("Options", True, colors['accent'])
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_surf, title_rect)
        
        # Difficulty panel
        diff_panel = pygame.Rect(self.width // 2 - 150, 200, 300, 100)
        draw_panel(self.screen, diff_panel, "AI Difficulty")
        
        # Difficulty display
        diff_text = self.subtitle_font.render(str(ai_difficulty), True, colors['text_primary'])
        diff_rect = diff_text.get_rect(center=(self.width // 2, 250))
        self.screen.blit(diff_text, diff_rect)
        
        # Difficulty buttons
        dec_button = pygame.Rect(diff_rect.left - 60, diff_rect.centery - 20, 40, 40)
        inc_button = pygame.Rect(diff_rect.right + 20, diff_rect.centery - 20, 40, 40)
        
        modern_button(self.screen, dec_button, "-", colors['accent'], colors['accent_light'])
        modern_button(self.screen, inc_button, "+", colors['accent'], colors['accent_light'])
        
        # Back button
        back_button = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)
        modern_button(
            self.screen, 
            back_button, 
            "Back", 
            colors['accent_dark'], 
            colors['accent'],
            text_color=(255, 255, 255)
        )
        
        pygame.display.flip()
        
        return dec_button, inc_button, back_button