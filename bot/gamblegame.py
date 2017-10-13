from .gambleplayer import Player
from .gamblestate import GameState
from .playerdao import PlayerDao

class GambleGame:

    def __init__(self):
        self.player_dao = PlayerDao()
        self.running = False
        self.winning_player_name = None
        # current highest roll
        self.winning_score = 0
        # current players in live game with their bet amount
        self.current_players = {}
        # player name to player object mapping
        self.players = self.player_dao.fetch_players()
        # game state used during betting/rolling phases
        self.state = GameState.IDLE
        # bet amount for current game
        self.bet_amount = None
        self.pot = 0


    def start(self, amount, username):
        try:
            amount = round(float(amount), 2)
        except:
            return "Incorrect bet value (must be a positive real number)"

        if self.running:
            return "game is already running"
        if amount <= 0:
            return "bet amount must be greater than 0"
        if amount > self.players[username].amount:
            return "Cannot start game with more than what you have"
        self.running = True
        self.bet_amount = amount
        self.state = GameState.BETTING
        self.place_bet(username)

        return

    def gift(self, send_player, receive_player, amount):
        try:
            if float(amount) <= 0:
                return "Please enter a positive real value"
            if (self.players.get(send_player) == None) or (self.players.get(receive_player) == None):
                return "Cannot gift as one or more username is not registered"
            if self.players[send_player].gift(float(amount), self.players[receive_player]):
                self.player_dao.update_players(self.players)
                return send_player + " gifted $" + "%.2f" % (float(amount)) + " to " + receive_player
            else:
                return send_player + " do not have enough money to gift"

        except:
            return amount + " is not a proper real value"

    # add extra money to user (CHEAT)
    def add(self, username, amount):
        if self.players.get(username) != None:
            self.players[username].amount += amount

    # places a bet and adds user to list of users in live game
    def place_bet(self, username):
        if self.current_players.get(username) != None:
            return username + " already placed a bet"
        bet = self.players[username].bet(self.bet_amount)
        if not bet:
            return username + " you only have $" + str(self.players[username].amount)
        else:
            self.current_players[username] = bet
            return username + " placed a bet of $" + "%.2f" % (self.bet_amount)

    # add user to game player record
    def add_player(self, name):
        new_player = Player(name)
        self.players[name] = new_player
        return name + " has joined the game"

    # remove player from current game
    def remove_player(self, name):
        self.current_players.pop(name, None)

    # list currently in game players
    def list_players(self):
        return list(self.current_players.keys())

    # list score for all existing players
    def list_score(self):
        response = ""
        for player in self.players.values():
            response += player.name + ": $" + "%.2f" % player.amount+ "\n"
        return response

    # list winning for specified user
    def list_winning(self, username):
        if self.players.get(username) != None:
            return "$%.2f" % self.players[username].amount
        else:
            return "You are not a registered player"

    # update winner variable to highest score
    def update_winner(self, name, score):
        if score > self.winning_score:
            self.winning_score = score
            self.winning_player_name = name

    # roll a random number in rolling phase if player has never rolled
    def roll(self, name):
        if self.state != GameState.ROLLING:
            return "Not in rolling state"
        if self.current_players.get(name) == None:
            return name + " has already rolled"
        else:
            random_roll = self.players[name].roll()
            self.update_winner(name, random_roll)
            self.remove_player(name)
            return name + " rolled " + str(random_roll)


    def help(self):
        return  "start - start game\n" \
               "list - list current players\n" \
               "score - list all stored players and their score\n" \
               "winnings - list personal score\n" \
                "gift <n> <username> - gift $n to user"

    # return pot value to all players
    def reset(self):
        for player_name, bet_amount in self.current_players.items():
            self.players[player_name].amount += bet_amount

    # ending game by resetting pot or rewarding winner
    def end(self):
        if self.winning_player_name != None:
            response = self.winning_player_name + " won $" + "%.2f" % (self.pot) + " with highest roll of " + str(self.winning_score)
            self.players[self.winning_player_name].amount += self.pot
        else:
            if self.state == GameState.IDLE:
                response = "Nobody rolled, game resetting..."
            else:
                response = "Not enough players, game resetting..."
            self.reset()
        self.player_dao.update_players(self.players)
        self.winning_score = 0
        self.winning_player_name = None
        self.current_players = {}
        self.running = False
        return response


