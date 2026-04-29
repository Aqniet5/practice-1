import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "Muqan_2008",
    "port": 5432
}


class DBHandler:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.conn.autocommit = True#PostgreSQL automatically saves every successful query.
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
            """)

    def get_player_id(self, username):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO players(username)
                VALUES (%s)
                ON CONFLICT(username)
                DO UPDATE SET username = EXCLUDED.username
                RETURNING id;
            """, (username,))

            return cur.fetchone()[0]#returning first row as tuple,then accessing first element

    def save_session(self, username, score, level):
        player_id = self.get_player_id(username)

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES (%s, %s, %s);
            """, (player_id, score, level))

    def get_best_score(self, username):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s;
            """, (username,))#COALESCE: use 0 instead of NULL., to protect from SQL injection

            return cur.fetchone()[0]

    def get_top_scores(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    p.username,
                    gs.score,
                    gs.level_reached,
                    TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI')
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10;
            """)#gs.played_at is the timestamp

            return cur.fetchall()