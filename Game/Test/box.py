# box.py
from PIL import Image
from PIL import ImageDraw
import threading
BOX_SIZE = 100  # Define the box size here, or get it from elsewhere in your program

class Box:
    def __init__(self, top_left_corner):
        self.lock = threading.Lock()
        self.is_taken = False 
        self.owner = None
        self.color = None

        self.top_left_corner = top_left_corner

        # Create a new image for this box
        self.image = Image.new('RGB', (BOX_SIZE, BOX_SIZE))


    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']  # don't include the lock when pickling
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()  # add the lock back after unpickling



    def scribble(self, player, x, y):
        # Convert the coordinates to be relative to the top-left corner of the box
        relative_x = x - self.top_left_corner[0]
        relative_y = y - self.top_left_corner[1]

        # Create a draw object
        draw = ImageDraw.Draw(self.image)

        # Draw a small square around the scribble point
        square_size = 10  # Change this value to adjust the size of the square
        left = max(0, relative_x - square_size // 2)
        top = max(0, relative_y - square_size // 2)
        right = min(BOX_SIZE, relative_x + square_size // 2)
        bottom = min(BOX_SIZE, relative_y + square_size // 2)
        right = max(right, left + 1)
        bottom = max(bottom, top + 1)
        draw.rectangle([left, top, right, bottom], fill=player.color)
        #draw.rectangle([left, top, right, bottom], fill=(0,255,0, 255), outline=(255, 0, 0))
        





