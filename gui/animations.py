"""
This file contains animation functions for the chess game.
"""

import pygame
import time

def fade_transition(screen, draw_function, to_surface=None):
    """
    Perform a fade transition between screens.
    
    Args:
        screen: The pygame screen
        draw_function: Function to draw the destination state
        to_surface: Optional pre-rendered destination surface
    """
    # Create a copy of the current screen as the source
    from_surface = screen.copy()
    
    # If no destination surface is provided, create one
    if to_surface is None:
        to_surface = pygame.Surface(screen.get_size())
        draw_function()  # Draw the destination state
        to_surface = screen.copy()  # Capture it
        # Reset the screen to the original state
        screen.blit(from_surface, (0, 0))
    
    # Create a surface for the fade effect
    fade_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    
    # Transition parameters
    fade_duration = 0.5  # seconds
    start_time = time.time()
    
    # Perform the fade transition
    running = True
    while running:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Calculate alpha based on elapsed time
        if elapsed >= fade_duration:
            alpha = 255
            running = False
        else:
            alpha = int(255 * (elapsed / fade_duration))
        
        # Draw the transition
        screen.blit(from_surface, (0, 0))
        
        # Create a faded version of the destination
        fade_surface.fill((0, 0, 0, 0))  # Clear with transparent
        fade_surface.blit(to_surface, (0, 0))
        fade_surface.set_alpha(alpha)
        
        # Overlay the faded destination
        screen.blit(fade_surface, (0, 0))
        
        # Update the display
        pygame.display.flip()
        
        # Handle events during transition to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
    # Ensure the final state is displayed
    screen.blit(to_surface, (0, 0))
    pygame.display.flip()

def animate_piece_movement(screen, draw_background, start_pos, end_pos, piece_img, duration=0.3):
    """
    Animate a chess piece moving from start to end position.
    
    Args:
        screen: The pygame screen
        draw_background: Function to draw the background
        start_pos: Starting position (x, y)
        end_pos: Ending position (x, y)
        piece_img: The piece image to animate
        duration: Animation duration in seconds
    """
    # Animation parameters
    start_time = time.time()
    
    # Get piece dimensions
    piece_width, piece_height = piece_img.get_size()
    
    # Perform the animation
    running = True
    while running:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Calculate progress (0.0 to 1.0)
        if elapsed >= duration:
            progress = 1.0
            running = False
        else:
            progress = elapsed / duration
            
            # Apply easing for smoother motion
            # Ease out cubic: progress = 1 - (1 - progress)^3
            progress = 1 - (1 - progress) ** 3
        
        # Calculate current position
        current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        
        # Draw the background
        draw_background()
        
        # Draw the piece at the current position
        screen.blit(
            piece_img, 
            (current_x, current_y, piece_width, piece_height)
        )
        
        # Update the display
        pygame.display.flip()
        
        # Handle events during animation to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
    # Ensure the final state is displayed
    draw_background()
    screen.blit(piece_img, (end_pos[0], end_pos[1], piece_width, piece_height))
    pygame.display.flip()