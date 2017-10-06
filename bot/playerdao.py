import sqlite3
from gambleplayer import Player

class PlayerDao:

    def connect_to_db(self):
        return sqlite3.connect('game.db')

    def update_players(self, players):
        conn = self.connect_to_db()
        statement = "REPLACE into users values (?, ?)"
        for player in players.values():
            values = [player.name, player.amount]
            conn.execute(statement, values)
        conn.commit()
        conn.close()

    def fetch_players(self):
        conn = self.connect_to_db()
        players = {}
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            name = row['username']
            players[name] = Player(name, row['winnings'])
        cursor.close()
        conn.commit()
        conn.close()
        return players