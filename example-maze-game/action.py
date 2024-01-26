import random
from mazelib import Maze
from mazelib.generate.Prims import Prims
from robocorp.actions import action

from database import serialize_game_state, deserialize_game_state
from game import MazePlayer, find_start_position_near_s


@action(is_consequential=False)
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


@action(is_consequential=False)
def game_action(move: str) -> str:
    """
    Executes a game action based on the player's move.
    updates the player's position in the maze accordingly, and returns a string describing
    the result of the move.

    Args:
        move (str): The direction in which the player wants to move one of (NORTH, SOUTH, WEST, EAST).

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
