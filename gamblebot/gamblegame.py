import random
import time
from threading import Timer
from gambleplayer import Player
from gamblestate import GameState

class GambleGame:

    def __init__(self):
        self.running = False
        self.winning_player_name = None
        # current highest roll
        self.winning_score = 0
        # current players in live game with their bet amount
        self.current_players = {}
        # player name to player object mapping
        self.players = {}
        # game state used during betting/rolling phases
        self.state = GameState.IDLE
        # bet amount for current game
        self.bet_amount = None
        self.number_of_rolls = 0

    def start(self, amount, username):
        if self.running:
            return "game is already running"
        self.running = True
        self.bet_amount = amount
        self.state = GameState.BETTING
        self.place_bet(username)

        return ""

    def place_bet(self, username):
        if self.current_players.get(username) != None:
            return username + " already placed a bet"
        if self.players.get(username) == None:
            self.add_player(username)
        bet = self.players[username].bet(self.bet_amount)
        if type(bet) is str:
            self.remove_player(username)
            return username + " you do not have enough money to place that bet"
        else:
            self.current_players[username] = bet
            return username + " placed a bet of $" + str(self.bet_amount)

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

    def list_winning(self, username):
        if self.players.get(username) != None:
            return str(self.players[username].amount)
        else:
            return "You are not a registered player"

    def update_winner(self, name, score):
        if score > self.winning_score:
            self.winning_score = score
            self.winning_player_name = name

    def roll(self, name):
        if self.current_players.get(name) == None:
            return name + " is not in the current game"
        elif self.current_players.get(name) != 0:
            random_roll = self.players[name].roll()
            self.update_winner(name, random_roll)
            self.number_of_rolls += 1
            return random_roll

    def help(self):
        return  "start - start game\n" \
               "list - list current players\n" \
               "score - list all stored players and their score\n" \
               "winnings - list personal score\n" \
                "gift <n> <username> - gift $n to user"

    def reset(self):
        for player_name, bet_amount in self.current_players.items():
            self.players[player_name].amount += bet_amount

    def end(self):
        if self.winning_player_name != None:
            pot = sum(bet for bet in self.current_players.values())
            response = self.winning_player_name + " won $" + str(pot) + " with highest roll of " + str(self.winning_score)
            self.players[self.winning_player_name].amount += pot
        else:
            response = "Not enough players, game reset"
            self.reset()
        self.winning_score = 0
        self.winning_player_name = None
        self.current_players = {}
        self.running = False
        self.number_of_rolls = 0
        return response


