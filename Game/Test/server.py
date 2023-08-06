import socket
import threading
import pickle
import time
from player import Player
from board import Board


def send_data(client, data):
    data_pickle = pickle.dumps(data)
    length = len(data_pickle)
    client.sendall(length.to_bytes(4, 'big')) # big endian
    client.sendall(data_pickle)

# determine winner and winner message
def display_game_over_message(players):
    max_taken_boxes = 0
    winner_color_key = None

    for color_key, player in players.items():
        if player.taken_boxes > max_taken_boxes:
            max_taken_boxes = player.taken_boxes
            winner_color_key = color_key

    if winner_color_key is not None:
        winner_color = players[winner_color_key].color  # Get the color from the player object
        if winner_color == (255, 0, 0):
            winner_message = f"The winner is Player Red"
        elif winner_color == (0, 255, 0):
            winner_message = f"The winner is Player Green"
        elif winner_color == (0, 0, 255):
            winner_message = f"The winner is Player Blue"
        elif winner_color == (255, 255, 0):
            winner_message = f"The winner is Player Yellow"
    else:
        winner_message = "It's a tie!"

    return winner_message

# thread function per client
# we only need 1 thread per client since the client only uses 1 thread for sending
def handle_client(client_socket, client_addr):
    print(f"Accepted new client connection from {client_addr}")
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            action, *params = pickle.loads(data)  # Deserialize the player's move

            # new player
            if action == "new_player":
                color = params[0]
                players[client_socket] = Player(color)
                print(f"New player connected with color {color}")

            # player has filled in a box
            elif action == "stop_drawing_threshold":
                players[client_socket].stop_drawing_server_colored()

            # player updates draw action
            # handle locking on server side
            elif action in ["start_drawing", "stop_drawing"]:
                x, y = params
                if action in ["start_drawing", "stop_drawing"]:
                    print(f"Received {action} action at ({x}, {y}) from client {client_addr}")
                # Update the game board
                box = board.get_current_box(x ,y)
                if action == "start_drawing":
                    result = players[client_socket].start_drawing(box, x, y) # tries to locks box
                    if result == "box_locked": # another player has the box
                        send_data(client_socket, "box_locked")
                elif action == "stop_drawing":
                    players[client_socket].stop_drawing() # unlocks box

            # Check for game over condition
            if board.is_game_over():
                print("====================board game over======================")
                break
        
        except Exception as _:
            return

    print("returning from handler")
    return

# syncs all player's boards
def handle_broadcast():
    while True:
        time.sleep(0.2)
        for client in players.keys():
            send_data(client, board.board_to_string())

        if board.is_game_over():
            for client in players.keys():
                winner_color_key = display_game_over_message(players)
                game_over_data = {"action": "game_over", "winner_color_key": winner_color_key}
                send_data(client, game_over_data)
            break
    
    # send final winning board so clients can finish game
    for client in players.keys():
        send_data(client, board.board_to_string())
    
    # wait for clients to receive and close their connections
    time.sleep(6)
    for client in players.keys():
        client.close()
    
    return

# Server setup
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555  
ADDR = (SERVER_IP, SERVER_PORT)
BUFFER_SIZE = 2048
MAX_PLAYERS = 3 # server listens for MAX_PLAYERS and only MAX_PLAYERS to join
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
#setup board broadcasting
client_broadcaster = threading.Thread(target=handle_broadcast)
client_broadcaster.start()

# Wait for client connections 
# Store client threads in a list
threads = []
num_players = 0
# only accepts MAX_PLAYERS number of players (no less either)
while num_players < MAX_PLAYERS:
    client_socket, client_addr = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_addr))
    client_handler.start()
    threads.append(client_handler)
    num_players += 1

# in game loop
while not board.is_game_over():
    time.sleep(1)
# After game is over join the client threads 
for thread in threads:
    thread.join()
# Join broadcasting thread
client_broadcaster.join()
# Close socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.close()