import random
import sqlite3
from itertools import combinations
from mazelib import Maze
from mazelib.generate.Prims import Prims
from robocorp.actions import action


class MazePlayer:
    def __init__(self, grid, position, end_position):
        """Initialize the maze player with the given maze and start position."""
        self.grid = grid
        self.position = position
        self.end_position = end_position
        self.directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1),
        }

    def move(self, direction: str) -> list[str]:
        dy, dx = self.directions[direction]
        y, x = self.position
        steps: list[str] = []

        while not self.is_blocked(y, x, direction):
            new_y, new_x = y + dy, x + dx
            if 0 <= new_y < len(self.grid) and 0 <= new_x < len(self.grid[0]):
                y, x = new_y, new_x
                self.position = (y, x)
                steps.append(f"Moved {direction} to ({y}, {x})")
            else:
                steps.append("Stopped: Out of bounds")  # Debug print
                return steps

            if self.is_end_nearby(y, x):
                steps.append("Stopped: At the end")
                return steps

            print(f"Moved to ({y}, {x})")
            if self.is_cross_section(y, x, direction):
                steps.append("Stopped: at a cross-section")
                steps.append(
                    f"From current location you may move: {self.free_directions().replace(':', ', ')}"
                )
                return steps

        steps.append("Stopped: Path is blocked")
        steps.append(
            f"From current location you may move: {self.free_directions().replace(':', ', ')}"
        )
        return steps

    def is_cross_section(self, y, x, direction):
        """Check if the current position is a cross-section or if the end 'E' is reached."""
        print(f"Checking cross-section at ({y}, {x}) in direction {direction}")

        # Check for openings directly adjacent in perpendicular directions
        perp_openings = False
        if direction in ["UP", "DOWN"]:
            # Check LEFT and RIGHT for perpendicular openings
            if x > 0 and self.grid[y][x - 1] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction LEFT at ({y}, {x - 1})")
            if x < len(self.grid[0]) - 1 and self.grid[y][x + 1] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction RIGHT at ({y}, {x + 1})")
        elif direction in ["LEFT", "RIGHT"]:
            # Check UP and DOWN for perpendicular openings
            if y > 0 and self.grid[y - 1][x] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction UP at ({y - 1}, {x})")
            if y < len(self.grid) - 1 and self.grid[y + 1][x] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction DOWN at ({y + 1}, {x})")

        if perp_openings:
            print("Cross-section found")
            return True

        print("No cross-section or dead end found")
        return False

    def is_end_nearby(self, y, x):
        """Check if the end 'E' is next to the player's position."""
        end_y, end_x = self.end_position
        return (abs(end_y - y) <= 1 and end_x == x) or (
                abs(end_x - x) <= 1 and end_y == y
        )

    def is_blocked(self, y, x, direction: str) -> bool:
        """Check if movement in the current direction is blocked."""
        dy, dx = self.directions[direction]
        next_y, next_x = y + dy, x + dx
        if not self.is_in_bounds(next_y, next_x):
            return True
        return self.grid[next_y][next_x] == 1

    def is_in_bounds(self, y, x):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def is_at_end(self):
        y, x = self.position
        return self.is_end_nearby(y, x)

    def free_directions(self) -> str:
        free_dirs = []
        y, x = self.position

        for direction, (dy, dx) in self.directions.items():
            new_y, new_x = y + dy, x + dx
            if self.is_in_bounds(new_y, new_x) and not self.is_blocked(y, x, direction):
                free_dirs.append(direction)

        return ":".join(sorted(free_dirs))

    def all_direction_combinations(self) -> list[tuple[str]]:
        free_dirs = sorted(self.directions.keys())
        all_combinations = []

        for r in range(1, len(free_dirs) + 1):
            for combo in combinations(free_dirs, r):
                all_combinations.append(combo)

        return all_combinations


def display_maze(maze, player):
    start_y, start_x = maze.start
    end_y, end_x = maze.end
    player_y, player_x = player.position

    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            if (y, x) == (player_y, player_x):
                print("X", end="")
            elif (y, x) == (start_y, start_x):
                print("S", end="")
            elif (y, x) == (end_y, end_x):
                print("E", end="")
            else:
                print("#" if cell == 1 else " ", end="")
        print()  # New line after each row


def find_start_position_near_s(maze):
    """Find the start position near 'S' in the maze."""
    s_y, s_x = maze.start
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Left, Right, Up, Down

    for dy, dx in directions:
        new_y, new_x = s_y + dy, s_x + dx
        if 0 <= new_y < len(maze.grid) and 0 <= new_x < len(maze.grid[0]):
            if maze.grid[new_y][new_x] == 0:
                return new_y, new_x

    return None  # No adjacent empty space found


def create_tables(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Mazes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grid TEXT,
            end_position TEXT
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS GameState (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maze_id INTEGER,
            player_position TEXT,
            FOREIGN KEY(maze_id) REFERENCES Mazes(id)
        );
    ''')



def serialize_game_state(player: MazePlayer, db_file: str):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    try:
        # Ensure tables exist
        create_tables(cur)

        # Clear existing data in tables
        cur.execute("DELETE FROM GameState")
        cur.execute("DELETE FROM Mazes")

        # Serialize and store the maze and player position
        # Serialize and store the maze
        grid_str = ','.join([''.join(map(str, row)) for row in player.grid])
        end_str = ','.join(map(str, player.end_position))
        cur.execute("INSERT INTO Mazes (grid, end_position) VALUES (?, ?)", (grid_str, end_str))
        maze_id = cur.lastrowid

        # Store the player position
        player_pos_str = ','.join(map(str, player.position))
        cur.execute("INSERT INTO GameState (maze_id, player_position) VALUES (?, ?)", (maze_id, player_pos_str))

    finally:
        conn.commit()
        conn.close()


def deserialize_game_state(db_file: str) -> MazePlayer:
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Fetch the latest game state
    cur.execute(
        "SELECT m.grid, m.end_position, g.player_position FROM GameState g JOIN Mazes m ON g.maze_id = m.id ORDER BY g.id DESC LIMIT 1")
    grid_str, end_str, player_pos_str = cur.fetchone()

    # Deserialize the maze and player position
    grid = [list(map(int, row)) for row in grid_str.split(',')]
    end_position = tuple(map(int, end_str.split(',')))
    player_position = tuple(map(int, player_pos_str.split(',')))

    conn.close()

    return MazePlayer(grid, player_position, end_position)


@action
def init_game() -> str:
    """
    Initializes the game with a randomly generated maze and places the player to start position.

    The function returns a string describing the initial state of the game, including the maze size,
    the player's starting position, and the directions the player can initially move in.

    Returns:
        str: A descriptive string about the initial state of the game, including the player's position
        and possible initial moves.
    """
    seed = random.randint(0, 100000)
    maze = Maze(seed=seed)
    maze_height = 5
    maze_width = 5
    maze.generator = Prims(maze_height, maze_width)
    maze.generate()
    maze.generate_entrances()
    player = MazePlayer(maze.grid, find_start_position_near_s(maze), maze.end)
    serialize_game_state(player, "game.db")
    return (f"You are a player in a 2 dimensional {maze_height * 2}x{maze_width * 2} maze. "
            "Find your way through the maze. "
            f"You have just entered the maze. Your position is {player.position}. "
            f"You can move from here: {player.free_directions().replace(':', ', ')}.")


@action
def game_action(move: str) -> str:
    """
    Executes a game action based on the player's move.

    This function takes the player's intended move direction (UP, DOWN, LEFT, RIGHT) as input,
    updates the player's position in the maze accordingly, and returns a string describing
    the result of the move. This includes the steps taken, any obstacles encountered,
    and the player's new position. If the player reaches the end of the maze, this is also indicated.

    Args:
        move (str): The direction in which the player wants to move one of (UP, DOWN, LEFT, RIGHT).

    Returns:
        str: A descriptive string of the outcome of the move, including the player's new position
        and any relevant game state changes.
    """
    player = deserialize_game_state("game.db")
    steps = player.move(move)
    serialize_game_state(player, "game.db")
    if player.is_at_end():
        return "\n".join(steps) + "\nFound through the maze! AMAZING! END OF GAME!"
    return "\n".join(steps) + f"\nYour position is {player.position}"
