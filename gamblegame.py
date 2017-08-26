import random

class GambleGame:

    def __init__(self):
        self.players = {}
        self.running = False
        self.winning_player = None
        self.winning_score = 0
        self.current_players = []

    def start(self):
        if self.running:
            return "Game is already running"
        elif len(self.current_players) < 1:
            return "Need more players"
        self.running = True
        return ""

    def add_player(self, username):
        if username in self.current_players:
            return username + " is already in the game"
        self.players[username] = 0
        self.current_players.append(username)
        return username + " has joined the game"

    def list_players(self):
        return self.current_players

    def list_score(self):
        response = ""
        for player, score in self.players.items():
            response += player + ": " + str(score) + ","
        return response.strip(",")

    def roll(self):
        return random.randint(1, 100)

    def update_winner(self, player, score):
        if score > self.winning_score:
            self.winning_score = score
            self.winning_player = player

    def end(self):
        self.players[self.winning_player] += 1
        self.winning_score = 0
        self.winning_player = None
        self.current_players = []
        self.running = False


