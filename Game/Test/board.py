from box import Box
import pygame

class Board:
    BOX_SIZE = 100  # We'll need to adjust this value based on the actual size of the boxes on screen
    COLS = 4
    ROWS = 4
    def __init__(self):
        self.boxes = [[Box((x*Board.BOX_SIZE, y*Board.BOX_SIZE)) for x in range(Board.COLS)] for y in range(Board.ROWS)]

    def is_game_over(self):
        return all(box.is_taken for row in self.boxes for box in row)

    def deep_copy(self, other_board):
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                self.boxes[y][x].deep_copy(other_board.boxes[y][x])

    def get_current_box(self, x, y):
        if 0 <= x < Board.COLS*Board.BOX_SIZE and 0 <= y < Board.ROWS*Board.BOX_SIZE:
            box_x = x // Board.BOX_SIZE
            box_y = y // Board.BOX_SIZE
            #print("x is: ", box_y, " y is: ", box_x)
            return self.boxes[box_y][box_x]
        else:
            #print("passed in x and y: ", x, " ", y)
            return None

    def draw_boxes(self, screen):
        for y, row in enumerate(self.boxes):
            for x, box in enumerate(row):
                outline_rect = pygame.Rect(x * Board.BOX_SIZE, y * Board.BOX_SIZE, Board.BOX_SIZE, Board.BOX_SIZE)
                pygame.draw.rect(screen, (0,0,0), outline_rect, 1)
                
                box_rect = outline_rect.inflate(-4, -4) 
                pygame.draw.rect(screen, box.color if box.is_taken else (255, 255, 255), box_rect)
