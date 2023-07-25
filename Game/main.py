from board import Board
from player import Player
from player import COLORS
from player import color_selection
import pygame
import sys

def main():
   # Initialize the game
    board = Board()
    pygame.init()

    # Set up the screen
    box_size = 50
    screen_size = (8 * box_size, 8 * box_size)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Board Game')

    
    # Choose the player colors
    player_color = color_selection(screen)
    players = [Player(player_color) ]

    clock = pygame.time.Clock()

    # Game loop
    while not board.is_game_over():
        for player in players:
            # Handle player input and update game state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the mouse button is pressed, start drawing in the current box
                    x, y = event.pos
                    player.start_drawing(board.get_current_box(x, y), x, y)
                elif event.type == pygame.MOUSEBUTTONUP:
                    # If the mouse button is released, stop drawing
                    player.stop_drawing()
                elif event.type == pygame.MOUSEMOTION:
                    # If the mouse is moving, continue drawing in the current box
                    x, y = event.pos
                    player.continue_drawing(board.get_current_box(x, y), x, y)

        # Draw the game board and update the display outside of the event loop
        screen.fill((255, 255, 255))
        board.draw_boxes(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
