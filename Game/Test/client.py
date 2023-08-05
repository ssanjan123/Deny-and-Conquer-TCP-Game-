import socket
import pickle
import pygame
from board import Board
from player import Player
from player import color_selection
import ctypes
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
#SERVER_IP = '127.0.0.1'  # replace with your server's IP
SERVER_PORT = 5555  # replace with your server's port
ADDR = (SERVER_IP, SERVER_PORT)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.setblocking(False)  # Set the socket to non-blocking


print(f"Connected to server at {ADDR}")


# Set up the game board
# Initialize the game
board = Board()
pygame.init()
# Set up the screen
box_size = 50
screen_size = (8 * box_size, 8 * box_size)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Board Game')

# Call the color selection function before the game loop starts
chosen_color = color_selection(screen)

# Create the player after color selection
player = Player(chosen_color)

# Send new player message to server
client_socket.sendall(pickle.dumps(("new_player", player.color_key)))


# Main game loop
while not board.is_game_over():
    # Handle incoming data from the server
    try:
        data = receive_data(client_socket)
        if data is not None:
            if data == "box_locked":
                # Display an error message on the screen
                print("The box you're trying to draw on is currently in use.")
            else:
                print("received board update")
                board = data
    except BlockingIOError:
        pass  # No data to receive
    except Exception as e:
        continue



    # Handle local events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.drawing_flag = True
            x, y = pygame.mouse.get_pos()
            #box = board.get_current_box(x // Board.BOX_SIZE, y // Board.BOX_SIZE)
            box = board.get_current_box(x, y)
            box_before_drawing = copy.deepcopy(box) # Make a copy of the box before drawing
            player.start_drawing(box, x, y)
            client_socket.sendall(pickle.dumps(("start_drawing", x, y)))



        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            print(f"Stop drawing at ({x}, {y})")
            player.stop_drawing()
            player.drawing_flag = False
            #client_socket.sendall(pickle.dumps(("stop_drawing", x, y)))
            if player.threshold_reached:
                client_socket.sendall(pickle.dumps(("stop_drawing_threshold", x, y)))
                print("I have sent out a filled box")
            else:
                client_socket.sendall(pickle.dumps(("stop_drawing", x, y)))
            player.threshold_reached = False
        elif event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            if player.drawing_flag:
                player.continue_drawing(board.get_current_box(x, y), x, y)
            
            #print(f"Continue drawing at ({x}, {y})")
            #client_socket.sendall(pickle.dumps(("continue_drawing", x, y)))

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          

    # Draw the game board and update the display outside of the event loop
    screen.fill((255, 255, 255))
    board.draw_boxes(screen)
    pygame.display.flip()

# Receive and process game over data
game_over_data = receive_data(client_socket)
if game_over_data is not None:
    game_over_data = pickle.loads(game_over_data)
    if game_over_data["action"] == "game_over":
        winner_color_key = game_over_data["winner_color_key"]
        ctypes.windll.user32.MessageBoxW(0, f"The game is over. {winner_color_key}", "Game Over", 1)
        print(f"The game is over. {winner_color_key}")
    else:
        print("Game over message received, but action is not recognized.")

# Clean up and exit
pygame.quit()
sys.exit()