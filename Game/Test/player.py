import pygame
import sys


class Player:
    BOX_SIZE = 100

    def start_drawing(self, box, x, y):
        if box is None or not box.lock.acquire(blocking=False): # only one player can access box
            print(f"Box is either invalid or currently in use: ({x}, {y})")
            return "box_locked"
        if box.is_taken: # do not draw over taken box
            return "box_taken"
        self.current_box = box
        print("current box set to: ", self.current_box.top_left_corner)
        box.scribble(self, x, y)
        return None

    # check filled status after lifting mousebutton
    def stop_drawing(self):
        if self.current_box:
            self.current_box.lock.release()
            # Check if the box is 20% filled
            colored_pixels = sum(1 for pixel in self.current_box.image.getdata() if pixel == self.color)
            total_pixels = Player.BOX_SIZE * Player.BOX_SIZE
            #print for debugging. Not needed but shows up in demo video
            print("total is: ", total_pixels)
            print("colored is: ", colored_pixels)
            print("box is: ", self.current_box.top_left_corner)
            self.current_box.percentage_filled = colored_pixels / total_pixels

            print(self.current_box.percentage_filled)

            if self.current_box.percentage_filled >= 0.2:
                self.threshold_reached = True

            self.current_box = None

    # server doesn't track continue_drawing, so needs it's own method
    def stop_drawing_server_colored(self):
        if self.current_box:
            self.current_box.lock.release()
            self.current_box.is_taken = True
            self.current_box.color = self.color
            self.current_box.owner = self
            self.taken_boxes += 1
            print("This should have increased: ", self.taken_boxes)
        
            self.current_box = None
        else:
            print("Current box is none")


    def continue_drawing(self, box, x, y):
        if self.current_box and box and box.top_left_corner == self.current_box.top_left_corner:
            self.current_box.scribble(self, x, y)

    def __init__(self, color_key):
        self.color_key = color_key
        self.color = COLORS[color_key] # player identifier
        self.taken_boxes = 0 # score
        self.current_box = None
        self.drawing_flag = False
        self.threshold_reached = False


# Player chooses color to join game
def color_selection(screen):
    player_colors = set(COLORS.keys())
    font = pygame.font.Font(None, 36)
    color_rects = {}  # Initialize color_rects dictionary to store color rectangles
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for color, rect in color_rects.items():
                    if rect.collidepoint(event.pos) and color in player_colors:
                        print("color picked: ", color)
                        player_colors.remove(color)
                        return color

        screen.fill((255, 255, 255))
        for i, color in enumerate(COLORS):
            pygame.draw.rect(screen, COLORS[color], (50 + i * 80, 50, 70, 70))
            color_rects[color] = pygame.Rect(50 + i * 80, 50, 70, 70)

        pygame.display.flip()
   


# syntactic sugar
COLORS = {
    'R': (255, 0, 0),  # Red
    'G': (0, 255, 0),  # Green
    'B': (0, 0, 255),  # Blue
    'Y': (255, 255, 0)  # Yellow
}


