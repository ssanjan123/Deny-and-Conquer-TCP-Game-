# box.py

class Box:
    def __init__(self):
        self.is_taken = False 
        self.owner = None
        self.percentage_filled = 0

        # Add color attribute
        self.color = None


    def scribble(self):
        # Increase the percentage_filled by a small amount
        self.percentage_filled += 0.01
        self.color = None  # The color of the box, which will be set to the player's color when the box is taken over
