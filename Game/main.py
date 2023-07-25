from board import Board
from player import Player
from player import COLORS
import pygame
import sys

def main():
    # Initialize the game
    board = Board()
    for i in range(4):
        player_color = input("Choose your color (R/G/B/Y): ")
        players = [Player(player_color) ]  # Let's say we have four players

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Board Game")
    screen.fill((255,255,255))

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

        # Draw the boxes on the screen
        board.draw_boxes(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
