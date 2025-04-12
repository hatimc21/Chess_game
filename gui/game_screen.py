# gui/game_screen.py
"""
This file contains the GameScreen class for managing the main game display.
"""

import pygame
from gui.board_display import BoardDisplay


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
        
        # Colors
        self.bg_color = (240, 240, 240)  # Light gray
        self.text_color = (0, 0, 0)      # Black
        self.button_color = (180, 180, 180)  # Medium gray
        self.button_hover_color = (150, 150, 150)  # Darker gray
        self.button_text_color = (0, 0, 0)  # Black
        
        # Fonts
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.info_font = pygame.font.SysFont('Arial', 18)
        self.button_font = pygame.font.SysFont('Arial', 20)
        
        # Determine board size
        self.board_size = min(width - 200, height - 100)
        self.board_margin = 30
        
        # Initialize board display
        self.board_display = BoardDisplay(screen, self.board_size, self.board_margin)
        
        # Game state information
        self.game_state = "ongoing"
        self.current_player = "White"
        
        # Buttons
        self.buttons = {}
        self.init_buttons()
    
    def init_buttons(self):
        """Initialize UI buttons."""
        # Button dimensions
        button_width = 150
        button_height = 40
        button_margin = 10
        
        # Button positions - right side of the board
        buttons_x = self.board_margin + self.board_size + 30
        
        # Position buttons at the top part of the side panel
        # to leave space for move history at the bottom
        buttons_y = self.board_margin + 100
        
        # New Game button
        self.buttons["new_game"] = {
            "rect": pygame.Rect(buttons_x, buttons_y, button_width, button_height),
            "text": "New Game",
            "action": "new_game"
        }
        
        # Undo Move button
        self.buttons["undo"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + button_height + button_margin, 
                                button_width, button_height),
            "text": "Undo Move",
            "action": "undo"
        }
        
        # AI Move button
        self.buttons["ai_move"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 2 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "AI Move",
            "action": "ai_move"
        }
        
        # Save Game button
        self.buttons["save"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 3 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "Save Game",
            "action": "save"
        }
        
        # Load Game button
        self.buttons["load"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 4 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "Load Game",
            "action": "load"
        }
        
        # Quit button
        self.buttons["quit"] = {
            "rect": pygame.Rect(buttons_x, buttons_y + 5 * (button_height + button_margin), 
                                button_width, button_height),
            "text": "Quit",
            "action": "quit"
        }
    
    def draw(self, chess_board):
        """
        Draw the game screen.
        
        Args:
            chess_board: The chess board object containing the game state
        """
        # Fill the background
        self.screen.fill(self.bg_color)
        
        # Draw the chess board
        self.board_display.draw_board(chess_board)
        
        # Draw game information
        self.draw_game_info(chess_board)
        
        # Draw buttons
        self.draw_buttons()
        
        # Update the display
        pygame.display.flip()
    
    def draw_game_info(self, chess_board):
        """Draw game information panel."""
        # Title
        title = self.title_font.render("Chess Game", True, self.text_color)
        self.screen.blit(title, (self.board_margin + self.board_size + 30, self.board_margin))
        
        # Current player
        player = "White" if chess_board.white_to_move else "Black"
        player_text = self.info_font.render(f"Current Player: {player}", True, self.text_color)
        self.screen.blit(player_text, (self.board_margin + self.board_size + 30, self.board_margin + 40))
        
        # Game state
        state = "Checkmate" if chess_board.checkmate else "Stalemate" if chess_board.stalemate else "Ongoing"
        state_text = self.info_font.render(f"Game State: {state}", True, self.text_color)
        self.screen.blit(state_text, (self.board_margin + self.board_size + 30, self.board_margin + 65))
        
        # Calculate positions for move history
        # Position it at the bottom section of the side panel to avoid overlap with buttons
        history_y = self.height - 220  # Start the history from bottom of screen - 220 pixels
        history_title = self.info_font.render("Move History:", True, self.text_color)
        self.screen.blit(history_title, (self.board_margin + self.board_size + 30, history_y))
        
        # Display last 8 moves (reduced from 10 to ensure it fits)
        start_index = max(0, len(chess_board.move_log) - 8)
        for i, move in enumerate(chess_board.move_log[start_index:]):
            move_num = start_index + i + 1
            player_symbol = "W" if move_num % 2 == 1 else "B"
            move_text = self.info_font.render(
                f"{move_num}. {player_symbol}: {move.get_chess_notation()}", 
                True, 
                self.text_color
            )
            self.screen.blit(
                move_text, 
                (self.board_margin + self.board_size + 30, history_y + 25 + i * 20)
            )
    
    def draw_buttons(self):
        """Draw UI buttons."""
        mouse_pos = pygame.mouse.get_pos()
        
        for button_info in self.buttons.values():
            button_rect = button_info["rect"]
            button_text = button_info["text"]
            
            # Check if mouse is hovering over button
            if button_rect.collidepoint(mouse_pos):
                color = self.button_hover_color
            else:
                color = self.button_color
            
            # Draw button
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, self.text_color, button_rect, 2)  # Border
            
            # Draw button text
            text = self.button_font.render(button_text, True, self.button_text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
    
    def handle_button_click(self, pos):
        """
        Handle button clicks.
        
        Args:
            pos (tuple): (x, y) position of the click
            
        Returns:
            str: The action to perform, or None if no button was clicked
        """
        for button_info in self.buttons.values():
            if button_info["rect"].collidepoint(pos):
                return button_info["action"]
        return None
    
    def resize(self, width, height):
        """
        Resize the game screen.
        
        Args:
            width (int): New screen width
            height (int): New screen height
        """
        self.width = width
        self.height = height
        
        # Recalculate board size
        self.board_size = min(width - 200, height - 100)
        
        # Resize board display
        self.board_display = BoardDisplay(self.screen, self.board_size, self.board_margin)
        
        # Reinitialize buttons
        self.init_buttons()