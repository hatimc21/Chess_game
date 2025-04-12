"""
Main module for the chess game.
"""

import pygame
import sys
import time
from chess_engine.board import Board
from ai.model import ChessAI
from gui.game_screen import GameScreen
from gui.theme import colors
from gui.animations import fade_transition

class ChessGame:
    """
    Main class for the chess game.
    """
    
    def __init__(self, width=1024, height=768):
        """
        Initialize the chess game.
        
        Args:
            width (int): Window width
            height (int): Window height
        """
        # Initialize pygame
        pygame.init()
        
        # Initialize fonts
        pygame.font.init()
        
        # Set up the display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Modern Chess")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Create the chess board
        self.board = Board()
        
        # Create the AI
        self.ai = ChessAI()
        
        # Create the game screen
        self.game_screen = GameScreen(self.screen, width, height)
        
        # Game state
        self.running = True
        self.game_over = False
        self.player_vs_player = True
        self.player_color = True  # True for white, False for black
        self.current_mode = "menu"  # "menu", "game", "options"
        
        # Animation state
        self.animating = False
        self.animation_start_time = 0
        self.animation_duration = 0.3  # seconds
    
    def run(self):
        """Run the main game loop."""
        while self.running:
            # Handle events
            self._handle_events()
            
            # Update game state
            self._update()
            
            # Render the game
            self._render()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
        
        # Clean up
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                # Resize the window
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.game_screen.resize(self.width, self.height)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Handle left click (button 1)
                if event.button == 1:
                    if self.current_mode == "game":
                        # Handle board click
                        if not self.game_over and (self.player_vs_player or (self.board.white_to_move == self.player_color)):
                            move_result = self.game_screen.board_display.handle_click(self.board, pos)
                            
                            # Check if a move was made
                            if move_result:
                                # Animate the move
                                self._animate_last_move(move_result)
                                
                                # Check for game end
                                if self.board.checkmate:
                                    winner = "Black" if self.board.white_to_move else "White"
                                    print(f"Checkmate! {winner} wins!")
                                    self.game_over = True
                                elif self.board.stalemate:
                                    print("Stalemate! Game is a draw.")
                                    self.game_over = True
                        
                        # Handle button click
                        button_action = self.game_screen.handle_button_click(pos)
                        if button_action:
                            self._process_button_action(button_action)
                    
                    elif self.current_mode == "menu":
                        # Get menu button boundaries
                        button_width, button_height = 220, 50
                        button_margin = 16
                        button_x = self.width // 2 - button_width // 2
                        
                        # Define menu buttons
                        pvp_button = pygame.Rect(button_x, 200, button_width, button_height)
                        pve_white_button = pygame.Rect(button_x, 200 + button_height + button_margin, 
                                                   button_width, button_height)
                        pve_black_button = pygame.Rect(button_x, 200 + 2 * (button_height + button_margin), 
                                                   button_width, button_height)
                        options_button = pygame.Rect(button_x, 200 + 3 * (button_height + button_margin), 
                                                 button_width, button_height)
                        quit_button = pygame.Rect(button_x, 200 + 4 * (button_height + button_margin), 
                                              button_width, button_height)
                        
                        # Check which button was clicked
                        if pvp_button.collidepoint(pos):
                            print("Selected: Player vs Player")
                            self.player_vs_player = True
                            self._transition_to_game()
                        
                        elif pve_white_button.collidepoint(pos):
                            print("Selected: Play as White")
                            self.player_vs_player = False
                            self.player_color = True  # White
                            self._transition_to_game()
                        
                        elif pve_black_button.collidepoint(pos):
                            print("Selected: Play as Black")
                            self.player_vs_player = False
                            self.player_color = False  # Black
                            self._transition_to_game()
                        
                        elif options_button.collidepoint(pos):
                            print("Selected: Options")
                            self.current_mode = "options"
                        
                        elif quit_button.collidepoint(pos):
                            print("Selected: Quit")
                            self.running = False
                    
                    elif self.current_mode == "options":
                        # Draw options screen to get button positions
                        dec_button, inc_button, back_button = self.game_screen.draw_options(self.ai.difficulty)
                        
                        # Check which button was clicked
                        if dec_button.collidepoint(pos) and self.ai.difficulty > 1:
                            self.ai.difficulty -= 1
                            self.ai.search_depth = max(1, min(5, self.ai.difficulty))
                            print(f"AI Difficulty set to: {self.ai.difficulty}")
                        
                        elif inc_button.collidepoint(pos) and self.ai.difficulty < 5:
                            self.ai.difficulty += 1
                            self.ai.search_depth = max(1, min(5, self.ai.difficulty))
                            print(f"AI Difficulty set to: {self.ai.difficulty}")
                        
                        elif back_button.collidepoint(pos):
                            print("Returning to main menu")
                            self.current_mode = "menu"
                
                # Handle mouse wheel for scrolling (buttons 4 and 5)
                elif event.button == 4 or event.button == 5:  # 4 is scroll up, 5 is scroll down
                    if self.current_mode == "game":
                        # Pass to game screen for handling scrolling
                        wheel_dir = 1 if event.button == 4 else -1
                        self.game_screen.handle_scroll(pos, is_wheel=True, wheel_dir=wheel_dir)
    
    def _update(self):
        """Update game state."""
        if self.current_mode == "game" and not self.game_over:
            # If it's AI's turn
            if not self.player_vs_player and self.board.white_to_move != self.player_color:
                # Make AI move
                ai_move = self.ai.find_best_move(self.board)
                if ai_move:
                    self.board.make_move(ai_move)
                    self._animate_last_move(ai_move)
                    
                    # Check for game end
                    if self.board.checkmate:
                        winner = "Black" if self.board.white_to_move else "White"
                        print(f"Checkmate! {winner} wins!")
                        self.game_over = True
                    elif self.board.stalemate:
                        print("Stalemate! Game is a draw.")
                        self.game_over = True
    
    def _render(self):
        """Render the game."""
        if self.current_mode == "menu":
            self.game_screen.draw_menu()
        elif self.current_mode == "options":
            self.game_screen.draw_options(self.ai.difficulty)
        elif self.current_mode == "game":
            self.game_screen.draw(self.board)
    
    def _process_button_action(self, action):
        """
        Process a button action.
        
        Args:
            action (str): The action to perform
        """
        if action == "new_game":
            self._new_game()
        elif action == "undo":
            if len(self.board.move_log) > 0:
                self.board.undo_move()
                if not self.player_vs_player and len(self.board.move_log) > 0:
                    self.board.undo_move()  # Undo AI move as well
                self.game_over = False
        elif action == "ai_move":
            if not self.game_over:
                ai_move = self.ai.find_best_move(self.board)
                if ai_move:
                    self.board.make_move(ai_move)
                    self._animate_last_move(ai_move)
        elif action == "save":
            # Save game functionality would go here
            print("Save game")
        elif action == "load":
            # Load game functionality would go here
            print("Load game")
        elif action == "quit":
            self.current_mode = "menu"
    
    def _new_game(self):
        """Start a new game."""
        self.board = Board()
        self.game_over = False
        
        # If player is black, make AI move first
        if not self.player_vs_player and not self.player_color:
            ai_move = self.ai.find_best_move(self.board)
            if ai_move:
                self.board.make_move(ai_move)
    
    def _transition_to_game(self):
        """Transition from menu to game."""
        self.current_mode = "game"
        self._new_game()
        
        # Create a surface for the destination state
        to_surface = pygame.Surface((self.width, self.height))
        self.game_screen.draw(self.board)
        to_surface = self.screen.copy()  # Capture the current screen after drawing
        self.screen.fill(colors['bg_primary'])  # Reset screen
        
        # Perform a fade transition
        fade_transition(self.screen, lambda: self.game_screen.draw(self.board), to_surface)
    
    def _animate_last_move(self, move):
        """
        Animate the last move made.
        
        Args:
            move: The move to animate
        """
        self.game_screen.animate_move(self.board, move)


if __name__ == "__main__":
    # Create and run the game
    game = ChessGame()
    game.run()