import sqlite3

from game import MazePlayer

DB_FILE = "game.db"

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
            game_id TEXT UNIQUE,
            FOREIGN KEY(maze_id) REFERENCES Mazes(id)
        );
    ''')



def serialize_game_state(player: MazePlayer):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        # Ensure tables exist
        create_tables(cur)

        # Serialize the maze
        grid_str = ','.join([''.join(map(str, row)) for row in player.grid])
        end_str = ','.join(map(str, player.end_position))

        # Check if the game already exists
        cur.execute("SELECT id FROM GameState WHERE game_id = ?", (player.game_id,))
        game_state = cur.fetchone()

        if game_state is None:
            # If game does not exist, insert new maze and game state
            cur.execute("INSERT INTO Mazes (grid, end_position) VALUES (?, ?)", (grid_str, end_str))
            maze_id = cur.lastrowid
            player_pos_str = ','.join(map(str, player.position))
            cur.execute("INSERT INTO GameState (maze_id, player_position, game_id) VALUES (?, ?, ?)",
                        (maze_id, player_pos_str, player.game_id))
        else:
            # If game exists, update the existing game state
            player_pos_str = ','.join(map(str, player.position))
            cur.execute("UPDATE GameState SET player_position = ? WHERE game_id = ?",
                        (player_pos_str, player.game_id))

    finally:
        conn.commit()
        conn.close()


def deserialize_game_state(game_id: str) -> MazePlayer:
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        # Fetch the game state based on UUID
        cur.execute(
            "SELECT m.grid, m.end_position, g.player_position FROM GameState g JOIN Mazes m ON g.maze_id = m.id WHERE g.game_id = ?",
            (game_id,))
        row = cur.fetchone()

        if row is None:
            raise ValueError("No game found with the specified UUID")

        grid_str, end_str, player_pos_str = row

        # Deserialize the maze and player position
        grid = [list(map(int, row)) for row in grid_str.split(',')]
        end_position = tuple(map(int, end_str.split(',')))
        player_position = tuple(map(int, player_pos_str.split(',')))

        return MazePlayer(grid, player_position, end_position, game_id)

    finally:
        conn.close()
