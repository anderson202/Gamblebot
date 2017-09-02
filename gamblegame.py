import random
import time
from threading import Timer
from gambleplayer import Player
from gamblestate import GameState

class GambleGame:

    def __init__(self):
        self.running = False
        self.winning_player_name = None
        self.winning_score = 0
        # current players in live game with their bet amount
        self.current_players = {}
        self.players = {}
        self.state = GameState.IDLE
        self.bet_amount = None

    def start(self, amount):
        if self.running:
            return "game is already running"
        self.running = True
        self.bet_amount = amount
        self.state = GameState.BETTING
        return ""

    def add_player(self, name):
        if name in self.current_players.keys():
            return name + " is already in the game"
        # add to list of existing players to have played
        if name not in self.players.keys():
            new_player = Player(name)
            self.players[name] = new_player
        self.current_players[name] = 0
        return name + " has joined the game"
    
    def remove_player(self, name):
        self.current_players.pop(name, None)
    
    def list_players(self):
        return list(self.current_players.keys())

    def list_score(self):
        response = ""
        for player in self.players.values():
            response += player.name + ": " + str(player.amount) + ","
        return response.strip(",")

    def list_winning(self, player):
        return str(player.amount)

    def start_rolling(self):
        self.total_bets = sum(bet for bet in self.current_players.values())
        self.state = GameState.ROLLING
        t = Timer(30, self.end())
        t.start()

    def update_winner(self, name, score):
        if score > self.winning_score:
            self.winning_score = score
            self.winning_player_name = name

    def roll(self, name):
        if self.current_players.get(name) == None:
            return name + " is not in the current game"
        elif self.current_players.get(name) != 0:
            return name + " has already rolled"
        self.current_players[name] = self.players[name].roll()
        self.update_winner(name, self.current_players[name])

    def help(self):
        return  "start - start game\n" \
               "list - list current players\n" \
               "score - list all stored players and their score\n"

    def end(self):
        '''self.players[self.winning_player_name].amount += self.total_bets
        self.winning_score = 0
        self.winning_player_name = None
        self.current_players = {}
        self.running = False'''
        print("END")


