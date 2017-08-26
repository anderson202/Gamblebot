import random
from gambleplayer import Player

class GambleGame:

    def __init__(self):
        self.running = False
        self.winning_player = None
        self.winning_score = 0
        # current players in live game with their bet amount
        self.current_players = {}
        self.players = {}

    def start(self):
        if self.running:
            return "Game is already running"
        elif len(self.current_players) < 1:
            return "Need more players"
        self.running = True
        return ""

    def add_player(self, player):
        if player.name in self.current_players.keys():
            return player.name + " is already in the game"
        self.players[player.name] = player
        self.current_players[player.name] = 0
        return player.name + " has joined the game"

    def list_players(self):
        return self.current_players.keys()

    def list_score(self):
        response = ""
        for player, score in self.players.items():
            response += player + ": " + str(score) + ","
        return response.strip(",")

    def list_winning(self, player):
        return str(player.amount)

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
        self.current_players = {}
        self.running = False


