import socket
import pickle
import pygame
from board import Board
from player import Player
import copy
import time
import random
import sys

def receive_data(sock):
    try:
        length_bytes = sock.recv(4)
        length = int.from_bytes(length_bytes, 'big')
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('Socket closed while receiving data')
            data += more
        return pickle.loads(data)
    except BlockingIOError:
        return None

# Server setup
BUFFER_SIZE = 2048
SERVER_IP = '127.0.0.1'  # replace with your server's IP
SERVER_PORT = 5555  # replace with your server's port
ADDR = (SERVER_IP, SERVER_PORT)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.setblocking(False)  # Set the socket to non-blocking


print(f"Connected to server at {ADDR}")

# Set up the game board
board = Board()  # initialize with an empty board

# Create a player for this client
player = Player("G")  # replace with the player's color key

# Send new player message to server
client_socket.sendall(pickle.dumps(("new_player", player.color_key)))
# Initialize the game
board = Board()
pygame.init()
# Set up the screen
box_size = 50
screen_size = (8 * box_size, 8 * box_size)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Board Game')
# Initialize Pygame
pygame.init()

# Main game loop
while True:
    # Handle incoming data from the server
    try:
        data = receive_data(client_socket)
        if data is not None:
            if data == "box_locked":
                # Display an error message on the screen
                print("The box you're trying to draw on is currently in use.")
            else:
                board = data
    except BlockingIOError:
        pass  # No data to receive
    except Exception as e:
        continue



    # Handle local events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            box = board.get_current_box(x // Board.BOX_SIZE, y // Board.BOX_SIZE)
            box_before_drawing = copy.deepcopy(box) # Make a copy of the box before drawing
            player.start_drawing(box, x, y)
            client_socket.sendall(pickle.dumps(("start_drawing", x, y)))



        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            print(f"Stop drawing at ({x}, {y})")
            player.stop_drawing()
            client_socket.sendall(pickle.dumps(("stop_drawing", x, y)))
        elif event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            #print(f"Continue drawing at ({x}, {y})")
            player.continue_drawing(board.get_current_box(x // Board.BOX_SIZE, y // Board.BOX_SIZE), x, y)
            client_socket.sendall(pickle.dumps(("continue_drawing", x, y)))

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          

    # Draw the game board and update the display outside of the event loop
    screen.fill((255, 255, 255))
    board.draw_boxes(screen)
    pygame.display.flip()

