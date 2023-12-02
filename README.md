
# Game Title

## Game Description

This game follows the same principles as Deny and Conquer. Players aim to fill as many squares as possible on a shared gameboard using their mouse. The server locks in a player’s color for a square once they color in the majority of it. The player with the most colored squares wins when all squares are filled.

## Game Mechanics

- **Access Control**: If multiple players contest the same square, it follows a first-come, first-serve basis. Others are locked out.
- **Square Control**: Players gain exclusive access to a square by left-clicking inside it. They must hold the click to fill it in. Releasing the click forfeits access. A square is permanently filled once a player colors over half of it.
- **Speed and Precision**: Players must be quick to contest and fill squares but also thorough enough to fill a significant portion. Incomplete filling leads to square reset.

## Application Dependencies

Before using the application, install external modules with the following command:

```bash
pip install -r requirements.txt
```

## Organization

The application consists of three base classes (`Box`, `Board`, and `Player`), a client file, and a server file. These components work together to simulate the game environment and adhere to its rules.

### Base Classes

#### Box
- **Dependencies**: Imports from Pillow (Image, ImageDraw) and Python's threading module.
- **Purpose**: Represents individual cells on the gameboard, allowing concurrent access and modifications.
- **Key Attributes**: `lock`, `is_taken`, `owner`, `color`.
- **Key Function**: `scribble`, which allows a player to color a square.

#### Board
- **Dependencies**: Imports Box class and Pygame module.
- **Purpose**: Creates and manages the gameboard.
- **Key Attributes**: `boxes` (2D array of Box elements).
- **Key Functions**: `get_current_box`, `is_game_over`, `string_to_board`, `board_to_string`.

#### Player
- **Purpose**: Represents and executes player actions.
- **Key Attributes**: `color_key`, `taken_boxes`, `current_box`, `drawing_flag`, `threshold_reached`.
- **Key Functions**: `start_drawing`, `stop_drawing`, `stop_drawing_server_colored`.

### Class Interactions

- **Box and Board**: Board manages a 2D array of Box elements.
- **Box and Player**: Player interacts with Box for drawing and locking.
- **Board Interactions**: Utilized in client and server files to access gameboard.

### Client and Server Files

- **Setup**: Any player can host the game. Players need to update the client file with the host's IP address.
- **Key Modules**: Uses Pygame for UI interaction, and socket, pickle, time, sys, and threading from Python's standard library.
- **Communication**: Implements a token-based system for client-server interactions.

## Overall Application Workflow

- **Server Setup**: Initializes and listens for incoming data.
- **Client Setup**: Connects to the server and chooses a color.
- **Game Progress**: Continuous updates, interactions, and checks for game completion.

## Design Considerations and Limitations

### Failed Implementations

1. **Non-Blocking Sockets**
   - Issue: Early return of socket functions.
   - Solution: Removed non-blocking setting, using dedicated listener thread.

2. **UDP Sockets for Communication**
   - Issue: Premature closing of sockets.
   - Solution: Switched to TCP sockets for reliability.

3. **Pickling for Board State Transfer**
   - Issue: Inconsistencies in client receiving board updates.
   - Solution: Manual serialization and streamlined data transfer.

For detailed explanations of each implementation and the reasons behind their failures, refer to the extended documentation.
