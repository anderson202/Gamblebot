import sys
import time
import multiprocessing
import threading
from threading import Timer
from os import environ
from slackclient import SlackClient
from gamblegame import GambleGame
from gamblestate import GameState

class GambleBot:

    def __init__(self, api_token=environ.get('api_key'), bot_id=environ.get('bot_id')):
        self.AT_BOT = "<@" + bot_id + ">"
        self.game = GambleGame()
        self.slack_client = SlackClient(api_token)
        self.timeout = 30
        self.handler_process = []
        self.current_thread = None

    # counts down a specified duration and then changes state of the game
    def count_down(self, duration, next_state, handler, channel):
        # flag to post at 5 seconds
        posted_warning = False
        start_time = time.time()
        while(True):
            if self.game.state == GameState.ROLLING and len(self.game.current_players) == 0:
                break
            current_count = time.time() - start_time
            if duration < current_count:
                self.game.state = next_state
                break
            if current_count > 25 and not posted_warning:
                self.post("5 seconds remaining!", channel)
                posted_warning = True
        time.sleep(1.5)
        if handler != None:
            handler(channel)

    # handle betting phase while allowing users to continue to call commands
    def handle_betting(self, username, bet_amount, channel):
        self.post(username + " has started a game. Amount to join is $" + "%.2f" % (bet_amount) +
                                  ".\n 30 seconds to bet, type 'bet' to place bet", channel)
        self.current_thread = threading.Thread(target=self.count_down, args=(self.timeout, GameState.ROLLING, self.handle_rolling, channel))
        self.current_thread.start()

    # handle rolling phase
    def handle_rolling(self, channel):
        self.game.pot = sum(bet for bet in self.game.current_players.values())
        if len(self.game.current_players) < 2:
            self.handle_end(channel)
        else:
            self.post("30 seconds to roll!", channel)
            self.current_thread = threading.Thread(target=self.count_down, args=(self.timeout, GameState.IDLE, self.handle_end, channel))
            self.current_thread.start()

    # end the game and post response
    def handle_end(self, channel):
        response = self.game.end()
        self.post(response, channel)

    def handle_command(self, username, msg, channel):
        # add user to list of users if they use any command
        if self.game.players.get(username) == None:
            self.game.add_player(username)
        response = ""
        if len(msg.split()) > 1:
            gamble_command = msg.split()[1]
            if gamble_command == "start":
                if len(msg.split()) != 3:
                    response = "Please specify bet amount"
                else:
                    try:
                        bet_amount = round(float(msg.split()[2]), 2)
                        response = self.game.start(bet_amount, username)
                        if response == "":
                            self.handle_betting(username, bet_amount, channel)
                    except:
                        response = "Incorrect bet value (must be a positive real number)"

            elif gamble_command == "bet" and self.game.state == GameState.BETTING:
                try:
                    response = self.game.place_bet(username)
                except:
                    response = "bet amount is not correct"

            elif gamble_command == "roll":
                response = self.game.roll(username)

            elif gamble_command == "list":
                response = self.game.list_players()

            elif gamble_command == "score":
                response = self.game.list_score()

            elif gamble_command == "help":
                response = self.game.help()

            elif gamble_command == "winnings":
                response = self.game.list_winning(username)

            elif gamble_command == "gift":
                if len(msg.split()) > 3:
                    gift_amount = msg.split()[2]
                    player_to_gift = msg.split()[3]
                    response = self.game.gift(username, player_to_gift, gift_amount)
        else:
            response="Use 'start <bet value>' to start the game"

        if response != "":
            self.post(response, channel)


    def post(self, response, channel):
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    # get output from real time message stream
    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.AT_BOT in output['text']:
                    username = self.slack_client.api_call("users.info", user=output['user'])['user']['name']
                    return username, output['text'].strip().lower(), output['channel']
        return None, None, None

    def listen(self):
        if self.slack_client.rtm_connect():
            print("Bot connected and running!")
            while True:
                username, msg, channel = self.parse_slack_output(self.slack_client.rtm_read())
                if msg and channel:
                    self.handle_command(username, msg, channel)
        else:
            print("Connection failed.")

if __name__ == "__main__":
    bot = GambleBot()
    bot.listen()


