from box import Box
import pygame
class Board:
    BOX_SIZE = 100  # We'll need to adjust this value based on the actual size of the boxes on screen

    def get_current_box(self, pos):
        # Convert the mouse position to box coordinates
        x, y = pos
        box_x = x // self.BOX_SIZE
        box_y = y // self.BOX_SIZE
        return self.boxes[box_y][box_x]

    def __init__(self):
        self.boxes = [[Box() for _ in range(8)] for _ in range(8)]

    def is_game_over(self):
        # Check if all boxes have been taken over
        return all(box.is_taken for row in self.boxes for box in row)


    def draw_boxes(self, screen):
        # Draw the boxes on the screen
        for y, row in enumerate(self.boxes):
            for x, box in enumerate(row):
                # Draw box outline
                outline_rect = pygame.Rect(x * self.BOX_SIZE, y * self.BOX_SIZE, self.BOX_SIZE, self.BOX_SIZE)
                pygame.draw.rect(screen, (0,0,0), outline_rect, 1)
                
                # Draw filled box  
                box_rect = outline_rect.inflate(-4, -4) 
                pygame.draw.rect(screen, box.color or (255, 255, 255), box_rect)