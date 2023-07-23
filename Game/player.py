class Player:
    DRAWING_THRESHOLD = 0.5  # The fraction of a box that needs to be drawn over for it to be considered taken

    def start_drawing(self, box):
        # If the player starts drawing in a box, we'll need to record which box they're drawing in
        self.current_box = box

    def stop_drawing(self):
        # If the player stops drawing, we'll need to check if they've drawn over more than the threshold of the current box
        if self.current_box.percentage_filled > self.DRAWING_THRESHOLD:
            self.current_box.is_taken = True
            self.current_box.owner = self

            # Set color
            self.current_box.color = self.color
        if self.current_box and self.current_box.percentage_filled > self.DRAWING_THRESHOLD:
            self.current_box.is_taken = True
            self.current_box.owner = self
            self.taken_boxes += 1
            # Set color
            self.current_box.color = self.color

            self.current_box.color = self.color  # Set the color of the box
        self.current_box = None

    def continue_drawing(self, box):

        # If the player continues drawing, we'll need to update the percentage_filled of the current box
        if self.current_box and box == self.current_box:
            self.current_box.scribble()

    def __init__(self, color):
        self.id = id
        self.color = COLORS[color]  # We'll have to define COLORS somewhere
        self.taken_boxes = 0
        self.current_box = None

COLORS = {
  'R': (255, 0, 0), # Red
  'G': (0, 255, 0), # Green
  'B': (0, 0, 255), # Blue
  'Y': (255, 255, 0) # Yellow
}