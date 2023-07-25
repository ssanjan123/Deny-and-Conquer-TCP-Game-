BOX_SIZE = 100  # We'll need to adjust this value based on the actual size of the boxes on screen
class Player:
    def start_drawing(self, box, x, y):
        self.current_box = box
        box.scribble(self, x, y)

    def stop_drawing(self):
        if self.current_box:
            # Check if the box is 50% filled
            colored_pixels = sum(1 for pixel in self.current_box.image.getdata() if pixel == self.color)
            total_pixels = BOX_SIZE * BOX_SIZE
            self.current_box.percentage_filled = colored_pixels / total_pixels

            if self.current_box.percentage_filled >= 0.5:
                self.current_box.is_taken = True
                self.current_box.color = self.color
                self.current_box.owner = self

            self.current_box = None

    def continue_drawing(self, box, x, y):
        if self.current_box and box == self.current_box:
            self.current_box.scribble(self, x, y)

    def __init__(self, color):
        self.id = id
        self.color = COLORS[color]
        self.taken_boxes = 0
        self.current_box = None


# In the Player class
COLORS = {
    'R': (255, 0, 0),  # Red
    'G': (0, 255, 0),  # Green
    'B': (0, 0, 255),  # Blue
    'Y': (255, 255, 0)  # Yellow
}
