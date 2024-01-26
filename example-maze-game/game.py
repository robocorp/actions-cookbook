from itertools import combinations


class MazePlayer:
    def __init__(self, grid, position, end_position, game_id):
        """Initialize the maze player with the given maze and start position."""
        self.grid = grid
        self.position = position
        self.end_position = end_position
        self.game_id = game_id
        self.directions = {
            "NORTH": (-1, 0),
            "SOUTH": (1, 0),
            "WEST": (0, -1),
            "EAST": (0, 1),
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
        if direction in ["NORTH", "SOUTH"]:
            # Check WEST and EAST for perpendicular openings
            if x > 0 and self.grid[y][x - 1] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction WEST at ({y}, {x - 1})")
            if x < len(self.grid[0]) - 1 and self.grid[y][x + 1] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction EAST at ({y}, {x + 1})")
        elif direction in ["WEST", "EAST"]:
            # Check NORTH and DOWN for perpendicular openings
            if y > 0 and self.grid[y - 1][x] == 0:
                perp_openings = True
                print(f"Open path in perpendicular direction NORTH at ({y - 1}, {x})")
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
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # WEST, EAST, NORTH, SOUTH

    for dy, dx in directions:
        new_y, new_x = s_y + dy, s_x + dx
        if 0 <= new_y < len(maze.grid) and 0 <= new_x < len(maze.grid[0]):
            if maze.grid[new_y][new_x] == 0:
                return new_y, new_x

    return None  # No adjacent empty space found
