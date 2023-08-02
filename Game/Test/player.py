import pygame
import sys


class Player:
    BOX_SIZE = 100
    def start_drawing(self, box, x, y):
        if box is None or not box.lock.acquire(blocking=False):
            print(f"Box is either invalid or currently in use: ({x}, {y})")
            return "box_locked"
        self.current_box = box
        box.scribble(self, x, y)
        return None

    def stop_drawing(self):
        if self.current_box:
            self.current_box.lock.release()
            # Check if the box is 50% filled
            colored_pixels = sum(1 for pixel in self.current_box.image.getdata() if pixel == self.color)
            total_pixels = Player.BOX_SIZE * Player.BOX_SIZE
            self.current_box.percentage_filled = colored_pixels / total_pixels

            if self.current_box.percentage_filled >= 0.5:
                self.current_box.is_taken = True
                self.current_box.color = self.color
                self.current_box.owner = self

            self.current_box = None

    def continue_drawing(self, box, x, y):
        if self.current_box and box == self.current_box:
            self.current_box.scribble(self, x, y)

    def __init__(self, color_key):
        self.color_key = color_key
        self.color = COLORS[color_key]
        self.taken_boxes = 0
        self.current_box = None

def color_selection(screen, num_players):
    player_colors = {}
    color_rects = {}
    font = pygame.font.Font(None, 36)

    while len(player_colors) < num_players:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for color in COLORS:
                    if color_rects[color].collidepoint(event.pos):
                        if color not in player_colors.values():
                            player_colors[len(player_colors) + 1] = color

        screen.fill((255, 255, 255))
        for i, color in enumerate(COLORS):
            pygame.draw.rect(screen, COLORS[color], (50 + i * 80, 50, 70, 70))
            color_rects[color] = pygame.Rect(50 + i * 80, 50, 70, 70)

        for player, color in player_colors.items():
            text = font.render(str(player), True, (255, 255, 255))  # Player number as white text
            text_rect = text.get_rect(center=color_rects[color].center)
            screen.blit(text, text_rect)

        pygame.display.flip()

    print('Player Colors:', player_colors)
    
    return player_colors # Return the color of the last selected player
   


# In the Player class
COLORS = {
    'R': (255, 0, 0),  # Red
    'G': (0, 255, 0),  # Green
    'B': (0, 0, 255),  # Blue
    'Y': (255, 255, 0)  # Yellow
}


