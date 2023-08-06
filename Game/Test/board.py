from box import Box
import pygame

class Board:
    BOX_SIZE = 100
    COLS = 4
    ROWS = 4
    def __init__(self):
        self.boxes = [[Box((x*Board.BOX_SIZE, y*Board.BOX_SIZE)) for x in range(Board.COLS)] for y in range(Board.ROWS)]

    # True if all boxes are taken; false otherwise
    def is_game_over(self):
        return all(box.is_taken for row in self.boxes for box in row)

    # copy board without reassigning box references
    def deep_copy(self, other_board):
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                self.boxes[y][x].deep_copy(other_board.boxes[y][x])

    # return box based on x,y mouse position
    def get_current_box(self, x, y):
        if 0 <= x < Board.COLS*Board.BOX_SIZE and 0 <= y < Board.ROWS*Board.BOX_SIZE:
            box_x = x // Board.BOX_SIZE
            box_y = y // Board.BOX_SIZE
            return self.boxes[box_y][box_x]
        else:
            return None

    # turn board info into a row * col length string
    def board_to_string(self):
        serial = ""
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                if self.boxes[y][x].color == None:
                    serial += '0'
                elif self.boxes[y][x].color == (255, 0, 0):
                    serial += 'R'
                elif self.boxes[y][x].color == (0, 255, 0):
                    serial += 'G'
                elif self.boxes[y][x].color == (0, 0, 255):
                    serial += 'B'
                else:
                    serial += 'Y'
        return serial

    # turn string into board information
    def string_to_board(self, serial):
        index = 0
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                if serial[index] == '0':
                    self.boxes[y][x].color = None
                    self.boxes[y][x].is_taken = False
                elif serial[index] == 'R':
                    self.boxes[y][x].color = (255, 0, 0)
                    self.boxes[y][x].is_taken = True
                elif serial[index] == 'G':
                    self.boxes[y][x].color = (0, 255, 0)
                    self.boxes[y][x].is_taken = True
                elif serial[index] == 'B':
                    self.boxes[y][x].color = (0, 0, 255)
                    self.boxes[y][x].is_taken = True
                else:
                    self.boxes[y][x].color = (255, 255, 0)
                    self.boxes[y][x].is_taken = True
                index += 1

    def draw_boxes(self, screen):
        for y, row in enumerate(self.boxes):
            for x, box in enumerate(row):
                outline_rect = pygame.Rect(x * Board.BOX_SIZE, y * Board.BOX_SIZE, Board.BOX_SIZE, Board.BOX_SIZE)
                pygame.draw.rect(screen, (0,0,0), outline_rect, 1)
                
                box_rect = outline_rect.inflate(-4, -4) 
                pygame.draw.rect(screen, box.color if box.is_taken else (255, 255, 255), box_rect)
