import sqlite3

from game import MazePlayer


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
