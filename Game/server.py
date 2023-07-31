import socket
import threading
import pickle
from board import Board
from player import Player

# Server setup
SERVER_IP = '127.0.0.1'  # replace with your server's IP
SERVER_PORT = 5555  # replace with your server's port
ADDR = (SERVER_IP, SERVER_PORT)

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(ADDR)

# Set up the game board
board = Board()  # initialize with an empty board

# Dictionary to store the players
players = {}

def handle_client(client_address, player):
    while True:
        data, addr = server_socket.recvfrom(4096)
        # Update game state based on received data
        action, x, y = pickle.loads(data)  # deserialize the player's move

        if action == "start_drawing":
            player.start_drawing(board.get_current_box(x, y), x, y)
        elif action == "stop_drawing":
            player.stop_drawing()
        elif action == "continue_drawing":
            player.continue_drawing(board.get_current_box(x, y), x, y)

def broadcast_game_state():
    while True:
        # Serialize the game state and send it to all clients
        for client_address in players:
            server_socket.sendto(pickle.dumps(board), client_address)

# Start the game state broadcaster thread
broadcaster_thread = threading.Thread(target=broadcast_game_state)
broadcaster_thread.start()

while True:
    # Accept a new client connection
    data, client_address = server_socket.recvfrom(4096)
    action, x, y = pickle.loads(data)  # Deserialize the player's move

    if action == "new_player":
        color = x  # In this case, 'x' is the player's color
        players[client_address] = Player(color)  # Create a new player for this client

        # Start a new thread to handle this client
        client_thread = threading.Thread(target=handle_client, args=(client_address, players[client_address]))
        client_thread.start()