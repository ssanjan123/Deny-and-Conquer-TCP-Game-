from board import Board
from player import Player
from player import COLORS
from player import color_selection

import pygame
import sys

def num_players_selection(screen):
    font = pygame.font.Font(None, 36)

    num_players = 0

    # Create rectangles for player number selection
    player_num_rects = {}
    for i in range(1, 5):
        player_num_rects[i] = pygame.Rect(100 + i * 40, 100, 30, 30)

    while not num_players:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1, 5):
                    if player_num_rects[i].collidepoint(event.pos):
                        num_players = i

        screen.fill((255, 255, 255))
        for i in range(1, 5):
            pygame.draw.rect(screen, (0, 0, 0), player_num_rects[i], 2)
            text = font.render(str(i), True, (0, 0, 0))
            text_rect = text.get_rect(center=player_num_rects[i].center)
            screen.blit(text, text_rect)

        text = font.render("Choose the number of players:", True, (0, 0, 0))
        screen.blit(text, (50, 50))

        pygame.display.flip()

    print('Number of Players:', num_players)
    return num_players

def display_game_over_message(screen):
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display the message for 3 seconds
    
def main():
   # Initialize the game
    board = Board()
    pygame.init()
    # Set up the screen
    box_size = 50
    screen_size = (8 * box_size, 8 * box_size)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Board Game')

    # Choose the number of players
    num_players = num_players_selection(screen)
    
    # Choose the player colors
    player_color = color_selection(screen, num_players)
    players = [Player(color) for _, color in player_color.items()]
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
        # Check if the game is over
        # Draw the game board and update the display outside of the event loop
        screen.fill((255, 255, 255))
        board.draw_boxes(screen)
        pygame.display.flip()
        clock.tick(60)

    # Display "Game Over" message on the screen
    display_game_over_message(screen)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
