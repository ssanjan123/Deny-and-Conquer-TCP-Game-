import pygame
import socket
import threading
import pickle
from board import Board
from player import Player

SERVER_IP = '127.0.0.1'  # replace with your server's IP
SERVER_PORT = 5555  # replace with your server's port
ADDR = (SERVER_IP, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(ADDR)
print(f"Connected to server at {ADDR}")


def listen_for_updates():
    global board
    while True:
        try:
            data, addr = client_socket.recvfrom(4096)
            board = pickle.loads(data)  # deserialize the game state
        except Exception as e:
            print(f"[EXCEPTION] {e}")
            break

# start the listener thread
listener_thread = threading.Thread(target=listen_for_updates)
listener_thread.start()

# Initialize Pygame
pygame.init()
box_size = 50
screen_size = (8 * box_size, 8 * box_size)
screen = pygame.display.set_mode(screen_size)

# set up the game board
board = Board()  # initialize with an empty board

# set up the player
player = Player("R")  # replace with your player's color
 

# start the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            box = board.get_current_box(x, y)
            player.start_drawing(box,x, y)
            client_socket.sendall(pickle.dumps(("start_drawing", x, y)))  # send the player's move to the server
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            player.stop_drawing()
            client_socket.sendall(pickle.dumps(("stop_drawing", x, y)))  # send the player's move to the server
        elif event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            box = board.get_current_box(x, y)
            player.continue_drawing(box, x, y)
            client_socket.sendall(pickle.dumps(("continue_drawing", x, y)))  # send the player's move to the server

    # draw the game board
    screen.fill((255, 255, 255))
    board.draw_boxes(screen)
    pygame.display.flip()

# when the game is over, stop the listener thread
listener_thread.join()
