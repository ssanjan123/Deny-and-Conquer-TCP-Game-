import socket
import pickle
import pygame
from board import Board
from player import Player
from player import color_selection
import copy
import time
import sys
import threading

def receive_data(sock):
    try:
        length_bytes = sock.recv(4)
        length = int.from_bytes(length_bytes, 'big') # big endian
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('Socket closed while receiving data')
            data += more
        return pickle.loads(data)
    except BlockingIOError:
        return None

def listener(board):
    end_of_game = False
    while not end_of_game:
        # Handle incoming data from the server
        try:
            data = receive_data(client_socket)
            if data is not None:
                if type(data) is dict:
                    winner_color_key = data["winner_color_key"]
                    #ctypes.windll.user32.MessageBoxW(0, f"The game is over. {winner_color_key}", "Game Over", 1)
                    print(f"The game is over. {winner_color_key}")
                    global glob_string
                    glob_string = f"The game is over. {winner_color_key}"
                    end_of_game = True
                elif data == "box_locked":
                    # Display an error message on the screen
                    print("The box you're trying to draw on is currently in use.")
                else:
                    #print("serialized data is: ", data)
                    #board.deep_copy(data)
                    board.string_to_board(data)
        except BlockingIOError:
            pass  # No data to receive
        except Exception as e:
            continue
    
    # clients receieve winner message before the board completes
    # gets final board message to complete the board client side
    while True:
        try:
            data = receive_data(client_socket)
            if data is not None:
                board.string_to_board(data)
                break
        except BlockingIOError:
            pass  # No data to receive
        except Exception as e:
            continue


    return

# Server setup
BUFFER_SIZE = 2048
glob_string = ""
#SERVER_IP = '154.20.101.82'  # potential host
SERVER_IP = '24.80.198.173'  # potential host
#SERVER_IP = '127.0.0.1'  # localhost
SERVER_PORT = 5555
ADDR = (SERVER_IP, SERVER_PORT)
# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
print(f"Connected to server at {ADDR}")

# Set up the game board
# Initialize the game
board = Board()
pygame.init()
game_over = False
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
#start listener thread
client_listener = threading.Thread(target=listener, args=(board, ))
client_listener.start()

# Main game loop
while not game_over:
    # Handle local events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.drawing_flag = True # tracking mouse down
            x, y = pygame.mouse.get_pos()
            box = board.get_current_box(x, y)
            box_before_drawing = copy.deepcopy(box) # Make a copy of the box before drawing
            player.start_drawing(box, x, y)
            client_socket.sendall(pickle.dumps(("start_drawing", x, y)))



        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            print(f"Stop drawing at ({x}, {y})")
            player.stop_drawing()
            player.drawing_flag = False # mouse up
            if player.threshold_reached:
                client_socket.sendall(pickle.dumps(("stop_drawing_threshold", x, y)))
                print("I have sent out a filled box")
            else:
                client_socket.sendall(pickle.dumps(("stop_drawing", x, y)))
            player.threshold_reached = False
        elif event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            if player.drawing_flag: # only update when player has mouseclick held down
                player.continue_drawing(board.get_current_box(x, y), x, y)

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          
    # Draw the game board and update the display outside of the event loop
    screen.fill((255, 255, 255))
    board.draw_boxes(screen)
    pygame.display.flip()

    if board.is_game_over():
        game_over = True

# Clean up and exit
pygame.quit()

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Display Winner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font settings
font = pygame.font.SysFont('Arial', 32)

#display winner pop up
screen.fill(WHITE)
winner_text = font.render(f"{glob_string} Wins!", True, BLACK)
text_rect = winner_text.get_rect(center=(WIDTH/2, HEIGHT/2))
screen.blit(winner_text, text_rect)
pygame.display.flip()
time.sleep(10)

# exit window after winner message 
pygame.quit()

# close connections and threads
client_listener.join()
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.close()