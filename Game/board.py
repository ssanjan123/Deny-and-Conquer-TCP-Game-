from box import Box
import pygame

BOX_SIZE = 100  # We'll need to adjust this value based on the actual size of the boxes on screen
class Board:
    def __init__(self):
        self.boxes = [[Box((x*BOX_SIZE, y*BOX_SIZE)) for x in range(2)] for y in range(2)]

    def is_game_over(self):
        return all(box.is_taken for row in self.boxes for box in row)

    def get_current_box(self, x, y):
        if 0 <= x < 2*BOX_SIZE and 0 <= y < 2*BOX_SIZE:
            box_x = x // BOX_SIZE
            box_y = y // BOX_SIZE
            return self.boxes[box_y][box_x]
        else:
            return None

    def draw_boxes(self, screen):
        for y, row in enumerate(self.boxes):
            for x, box in enumerate(row):
                outline_rect = pygame.Rect(x * BOX_SIZE, y * BOX_SIZE, BOX_SIZE, BOX_SIZE)
                pygame.draw.rect(screen, (0,0,0), outline_rect, 1)
                
                box_rect = outline_rect.inflate(-4, -4) 
                pygame.draw.rect(screen, box.color if box.is_taken else (255, 255, 255), box_rect)
