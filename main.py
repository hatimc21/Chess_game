# main.py
"""
Main entry point for the chess game.
"""

import os
import sys
import pygame
import pickle
from chess_engine.board import Board
from gui.game_screen import GameScreen
from ai.model import ChessAI


class ChessGame:
    """
    Main class for the chess game.
    """
    
    def __init__(self, width=960, height=640):
        """
        Initialize the chess game.
        
        Args:
            width (int): Window width
            height (int): Window height
        """
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Chess Game with AI")
        
        # Create the window
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.width = width
        self.height = height
        
        # Create game components
        self.board = Board()
        self.game_screen = GameScreen(self.screen, width, height)
        
        # Game state
        self.running = True
        self.game_over = False
        self.player_vs_player = True  # True for PvP, False for PvE
        self.player_color = True      # True for white, False for black
        
        # AI
        self.ai = ChessAI(difficulty=3)
        self.ai_thinking = False
        
        # Game mode
        self.current_mode = "menu"  # "menu", "game", "options"
        
        # Create directories
        os.makedirs("saves", exist_ok=True)
        os.makedirs("assets/pieces", exist_ok=True)
    
    def run(self):
        """Run the main game loop."""
        clock = pygame.time.Clock()
        
        while self.running:
            # Process events
            self._handle_events()
            
            # Update game state
            self._update()
            
            # Render the game
            self._render()
            
            # Cap the frame rate
            clock.tick(60)
        
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
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left mouse button clicked
                pos = pygame.mouse.get_pos()
                
                if self.current_mode == "game":
                    # Handle board click
                    if not self.game_over and (self.player_vs_player or (self.board.white_to_move == self.player_color)):
                        move_result = self.game_screen.board_display.handle_click(self.board, pos)
                        
                        # Check if a move was made
                        if move_result:
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
                    button_width, button_height = 200, 50
                    button_margin = 20
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
                        self.current_mode = "game"
                        self.board.reset_board()
                        self.game_over = False
                    
                    elif pve_white_button.collidepoint(pos):
                        print("Selected: Play as White")
                        self.player_vs_player = False
                        self.player_color = True  # White
                        self.current_mode = "game"
                        self.board.reset_board()
                        self.game_over = False
                    
                    elif pve_black_button.collidepoint(pos):
                        print("Selected: Play as Black")
                        self.player_vs_player = False
                        self.player_color = False  # Black
                        self.current_mode = "game"
                        self.board.reset_board()
                        self.game_over = False
                    
                    elif options_button.collidepoint(pos):
                        print("Selected: Options")
                        self.current_mode = "options"
                    
                    elif quit_button.collidepoint(pos):
                        print("Selected: Quit")
                        self.running = False
                
                elif self.current_mode == "options":
                    # Handle options click
                    diff_font = pygame.font.SysFont('Arial', 24)
                    diff_text = diff_font.render(f"AI Difficulty: {self.ai.difficulty}", True, (0, 0, 0))
                    diff_rect = diff_text.get_rect(center=(self.width // 2, 200))
                    
                    # Difficulty buttons
                    button_width, button_height = 30, 30
                    button_margin = 10
                    
                    # Define options buttons
                    dec_button = pygame.Rect(diff_rect.left - button_width - button_margin, 
                                          diff_rect.centery - button_height // 2, 
                                          button_width, button_height)
                    inc_button = pygame.Rect(diff_rect.right + button_margin, 
                                          diff_rect.centery - button_height // 2, 
                                          button_width, button_height)
                    back_button = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)
                    
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
    
    def _update(self):
        """Update game state."""
        # If playing against AI and it's AI's turn
        if not self.player_vs_player and not self.game_over and (self.board.white_to_move != self.player_color):
            if not self.ai_thinking:
                # Start AI thinking
                self.ai_thinking = True
                
                # Choose and make the AI move
                ai_move = self.ai.choose_move(self.board)
                
                if ai_move:
                    self.board.make_move(ai_move)
                    
                    # Check for game end
                    if self.board.checkmate:
                        winner = "Black" if self.board.white_to_move else "White"
                        print(f"Checkmate! {winner} wins!")
                        self.game_over = True
                    elif self.board.stalemate:
                        print("Stalemate! Game is a draw.")
                        self.game_over = True
                
                self.ai_thinking = False
    
    def _render(self):
        """Render the game screen."""
        if self.current_mode == "game":
            # Draw the game screen
            self.game_screen.draw(self.board)
        
        elif self.current_mode == "menu":
            # Draw the menu screen
            self.screen.fill((240, 240, 240))
            
            # Draw title
            font = pygame.font.SysFont('Arial', 48, bold=True)
            title = font.render("Chess Game", True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Draw buttons
            button_font = pygame.font.SysFont('Arial', 28)
            button_width, button_height = 200, 50
            button_margin = 20
            button_x = self.width // 2 - button_width // 2
            
            # PvP button
            pvp_button = pygame.Rect(button_x, 200, button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), pvp_button)
            pygame.draw.rect(self.screen, (0, 0, 0), pvp_button, 2)
            pvp_text = button_font.render("Player vs Player", True, (0, 0, 0))
            pvp_text_rect = pvp_text.get_rect(center=pvp_button.center)
            self.screen.blit(pvp_text, pvp_text_rect)
            
            # PvE (White) button
            pve_white_button = pygame.Rect(button_x, 200 + button_height + button_margin, 
                                         button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), pve_white_button)
            pygame.draw.rect(self.screen, (0, 0, 0), pve_white_button, 2)
            pve_white_text = button_font.render("Play as White", True, (0, 0, 0))
            pve_white_text_rect = pve_white_text.get_rect(center=pve_white_button.center)
            self.screen.blit(pve_white_text, pve_white_text_rect)
            
            # PvE (Black) button
            pve_black_button = pygame.Rect(button_x, 200 + 2 * (button_height + button_margin), 
                                         button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), pve_black_button)
            pygame.draw.rect(self.screen, (0, 0, 0), pve_black_button, 2)
            pve_black_text = button_font.render("Play as Black", True, (0, 0, 0))
            pve_black_text_rect = pve_black_text.get_rect(center=pve_black_button.center)
            self.screen.blit(pve_black_text, pve_black_text_rect)
            
            # Options button
            options_button = pygame.Rect(button_x, 200 + 3 * (button_height + button_margin), 
                                       button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), options_button)
            pygame.draw.rect(self.screen, (0, 0, 0), options_button, 2)
            options_text = button_font.render("Options", True, (0, 0, 0))
            options_text_rect = options_text.get_rect(center=options_button.center)
            self.screen.blit(options_text, options_text_rect)
            
            # Quit button
            quit_button = pygame.Rect(button_x, 200 + 4 * (button_height + button_margin), 
                                     button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), quit_button)
            pygame.draw.rect(self.screen, (0, 0, 0), quit_button, 2)
            quit_text = button_font.render("Quit", True, (0, 0, 0))
            quit_text_rect = quit_text.get_rect(center=quit_button.center)
            self.screen.blit(quit_text, quit_text_rect)
        
        elif self.current_mode == "options":
            # Draw the options screen
            self.screen.fill((240, 240, 240))
            
            # Draw title
            font = pygame.font.SysFont('Arial', 48, bold=True)
            title = font.render("Options", True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Draw difficulty selection
            diff_font = pygame.font.SysFont('Arial', 24)
            diff_text = diff_font.render(f"AI Difficulty: {self.ai.difficulty}", True, (0, 0, 0))
            diff_rect = diff_text.get_rect(center=(self.width // 2, 200))
            self.screen.blit(diff_text, diff_rect)
            
            # Difficulty buttons
            button_width, button_height = 30, 30
            button_margin = 10
            
            # Decrease difficulty button
            dec_button = pygame.Rect(diff_rect.left - button_width - button_margin, 
                                    diff_rect.centery - button_height // 2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), dec_button)
            pygame.draw.rect(self.screen, (0, 0, 0), dec_button, 2)
            dec_text = diff_font.render("-", True, (0, 0, 0))
            dec_text_rect = dec_text.get_rect(center=dec_button.center)
            self.screen.blit(dec_text, dec_text_rect)
            
            # Increase difficulty button
            inc_button = pygame.Rect(diff_rect.right + button_margin, 
                                    diff_rect.centery - button_height // 2, 
                                    button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), inc_button)
            pygame.draw.rect(self.screen, (0, 0, 0), inc_button, 2)
            inc_text = diff_font.render("+", True, (0, 0, 0))
            inc_text_rect = inc_text.get_rect(center=inc_button.center)
            self.screen.blit(inc_text, inc_text_rect)
            
            # Back button
            back_button = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)
            pygame.draw.rect(self.screen, (180, 180, 180), back_button)
            pygame.draw.rect(self.screen, (0, 0, 0), back_button, 2)
            back_text = pygame.font.SysFont('Arial', 28).render("Back", True, (0, 0, 0))
            back_text_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_text_rect)
        
        # Update the display
        pygame.display.flip()
    
    def _process_button_action(self, action):
        """Process button actions."""
        if action == "new_game":
            # Fully reset the game state
            self.board = Board()  # Create a completely new board object
            self.game_over = False
            
            # Reset selection and valid moves in the board display
            self.game_screen.board_display.selected_square = None
            self.game_screen.board_display.valid_moves = []
            
            print("Started new game")
        
        elif action == "undo":
            # Undo last move (and AI move if playing against AI)
            if self.board.undo_move():
                self.game_over = False
                if not self.player_vs_player:
                    self.board.undo_move()
        
        elif action == "ai_move":
            # Make an AI move regardless of game mode
            if not self.game_over:
                ai_move = self.ai.choose_move(self.board)
                if ai_move:
                    self.board.make_move(ai_move)
                    
                    # Check for game end
                    if self.board.checkmate:
                        winner = "Black" if self.board.white_to_move else "White"
                        print(f"Checkmate! {winner} wins!")
                        self.game_over = True
                    elif self.board.stalemate:
                        print("Stalemate! Game is a draw.")
                        self.game_over = True
        
        elif action == "save":
            self._save_game()
        
        elif action == "load":
            self._load_game()
        
        elif action == "quit":
            self.current_mode = "menu"
    
    def _save_game(self):
        """Save the current game state."""
        try:
            save_data = {
                'board': self.board,
                'player_vs_player': self.player_vs_player,
                'player_color': self.player_color,
                'game_over': self.game_over
            }
            
            with open("saves/game_save.pkl", 'wb') as f:
                pickle.dump(save_data, f)
            
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def _load_game(self):
        """Load a saved game state."""
        try:
            if os.path.exists("saves/game_save.pkl"):
                with open("saves/game_save.pkl", 'rb') as f:
                    save_data = pickle.load(f)
                
                self.board = save_data['board']
                self.player_vs_player = save_data['player_vs_player']
                self.player_color = save_data['player_color']
                self.game_over = save_data['game_over']
                
                # Reset selection and valid moves in the board display
                self.game_screen.board_display.selected_square = None
                self.game_screen.board_display.valid_moves = []
                
                print("Game loaded successfully!")
            else:
                print("No saved game found!")
        except Exception as e:
            print(f"Error loading game: {e}")


# Run the game if this script is executed directly
if __name__ == "__main__":
    game = ChessGame()
    game.run()