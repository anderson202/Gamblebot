import sys
import time
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

    def post(self, response, channel):
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    def get_user_input(self, player):
        timeout = time.time() + 30 
        while(True):
            if time.time() > timeout:
                return -1
            
            username, msg, channel = self.parse_slack_output(self.slack_client.rtm_read())
            if(msg and channel):
                if username != None and username == player and msg.split()[1] == "roll":
                    return self.game.players[player].roll()

    def handle_command(self, username, msg, channel):
        print(msg)
        response = ""
        if len(msg.split()) > 1:
            gamble_command = msg.split()[1]
            if gamble_command == "start":
                if len(msg.split()) != 3:
                    response = "Please specify bet amount"
                else:
                    bet_amount = int(msg.split()[2])
                    response = self.game.start(bet_amount)
                    if response == "":
                        self.post(username + " has started a game. Amount to join is $" + str(bet_amount) +
                                  ".\n 30 seconds to bet, type 'bet' to place bet", channel)
                        t = Timer(30, self.game.start_rolling())
                        t.start()

            elif gamble_command == "bet" and self.game.state == GameState.BETTING:
                try:
                    self.game.add_player(username)
                    bet = self.game.players[username].bet(self.game.bet_amount)
                    if type(bet) is str:
                        response = username + " you do not have enough money to place that bet"
                        self.game.remove_player(username)
                    else:
                        self.game.current_players[username] = bet
                        response = username + " placed a bet of " + str(self.game.bet_amount)
                except:
                    response = "bet amount is not correct"

            elif gamble_command == "roll" and self.game.state == GameState.ROLLING:
                response = self.game.roll(username)

            elif gamble_command == "list":
                response = self.game.list_players()

            elif gamble_command == "score":
                response = self.game.list_score()

            elif gamble_command == "help":
                response = self.game.help()

            elif gamble_command == "winnings":
                response = self.game.list_winning(username)
        else:
            response="Use 'start <bet value>' to start the game"

        self.post(response, channel)


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


