# box.py
from PIL import Image
from PIL import ImageDraw
BOX_SIZE = 100  # Define the box size here, or get it from elsewhere in your program

class Box:
    def __init__(self, top_left_corner):
        self.is_taken = False 
        self.owner = None
        self.color = None
        self.top_left_corner = top_left_corner

        # Create a new image for this box
        self.image = Image.new('RGB', (BOX_SIZE, BOX_SIZE))



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
        draw.rectangle([left, top, right, bottom], fill=player.color)






