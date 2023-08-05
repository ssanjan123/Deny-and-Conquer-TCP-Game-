import socket
import threading
import pickle
import time
from player import Player
from board import Board


def send_data(client, data):
    data_pickle = pickle.dumps(data)
    length = len(data_pickle)
    client.sendall(length.to_bytes(4, 'big'))
    client.sendall(data_pickle)
# Server setup
SERVER_IP = '0.0.0.0' # replace with your server's IP
SERVER_PORT = 5555  # replace with your server's port
ADDR = (SERVER_IP, SERVER_PORT)
BUFFER_SIZE = 2048

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen()

print(f"Server started at {ADDR}")

# Set up the game board
board = Board()  # initialize with an empty board

# Player setup
players = {}  # dictionary to keep track of players
player_colors = ["RED", "GREEN", "BLUE", "YELLOW"]  # list of player colors

#broadcast sync board update
idle_broadcast = True


def handle_client(client_socket, client_addr):
    print(f"Accepted new client connection from {client_addr}")
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        action, *params = pickle.loads(data)  # Deserialize the player's move
        if action == "new_player":
            color = params[0]
            players[client_socket] = Player(color)
            print(f"New player connected with color {color}")
        elif action == "stop_drawing_threshold":
            players[client_socket].stop_drawing_server_colored()
        elif action in ["start_drawing", "stop_drawing", "continue_drawing"]:
            x, y = params
            if action in ["start_drawing", "stop_drawing"]:
                print(f"Received {action} action at ({x}, {y}) from client {client_addr}")
            # Update the game board
            box = board.get_current_box(x ,y)
            if action == "start_drawing":
                result = players[client_socket].start_drawing(box, x, y)
                if result == "box_locked":
                    send_data(client_socket, "box_locked")
            elif action == "stop_drawing":
                players[client_socket].stop_drawing()
            elif action == "continue_drawing":
                players[client_socket].continue_drawing(box, x, y)
        # Send the updated board to all connected clients
        board_pickle = pickle.dumps(board)
        length = len(board_pickle)
        for client in players.keys():
            send_data(client, board)
        idle_broadcast = False



    print(f"Client {client_addr} disconnected")
    client_socket.close()
    del players[client_socket]

# only broadcast if communication has been idle for a while
# syncs all player's boards in case players lose a board update message
def handle_broadcast():
    while True:
        time.sleep(0.7)
        if idle_broadcast:
            for client in players.keys():
                send_data(client, board)
            idle_broadcast = False
        else:
            idle_broadcast = True


client_broadcaster = threading.Thread(target=handle_broadcast)
client_broadcaster.start()

# Wait for client connections 
# Store client threads in a list
threads = []
while True:
    if board.is_game_over():
        break
    client_socket, client_addr = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_addr))
    client_handler.start()
    threads.append(client_handler)

# After game is over join the client threads 
for thread in threads:
    thread.join()

# Join broadcasting thread
client_broadcaster.join()