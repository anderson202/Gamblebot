import sys
import time
import random
from slackclient import SlackClient
from gamblegame import GambleGame

class GambleBot:


    def __init__(self, token, id):
        API_TOKEN = token
        BOT_ID = id
        self.AT_BOT = "<@" + BOT_ID + ">"
        self.game = GambleGame()
        self.slack_client = SlackClient(API_TOKEN)

    def post(self, response, channel):
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    def get_user_input(self, player):
        while(True):
            username, command, channel = self.parse_slack_output(self.slack_client.rtm_read())
            if(command and channel):
                if username != None and username == player and command.split()[1] == "roll":
                    return

    def handle_command(self, username, command, channel):
        print(command)
        response = ""
        if len(command.split()) > 1:
            gamble_command = command.split()[1]
            if gamble_command == "join":
                response = self.game.add_player(username)

            elif gamble_command == "start":
                response = self.game.start()
                if response == "":
                    for player in self.game.players.keys():
                        response = player + "'s turn to roll"
                        self.post(response, channel)
                        self.get_user_input(player)

                        random_int = random.randint(1, 100)
                        self.game.update_winner(player, random_int)
                        response = "You rolled " + str(random_int)
                        self.post(response, channel)
                        time.sleep(1)
                    response = "Winner of this round is " + self.game.winning_player
                    self.game.end()

            elif gamble_command == "list":
                response = self.game.list_players()

            elif gamble_command == "score":
                response = self.game.list_score()

            elif gamble_command == "help":
                response = "join - join existing game\nstart - start game\nlist - list current players\nscore - list all stored players and their score"
        else:
            response="Use 'join' to join the game"


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
        READ_WEBSOCKET_DELAY = 1
        if self.slack_client.rtm_connect():
            print("Bot connected and running!")
            while True:
                username, command, channel = self.parse_slack_output(self.slack_client.rtm_read())
                if command and channel:
                    self.handle_command(username, command, channel)
        else:
            print("Connection failed.")



if __name__ == "__main__":
    token = sys.argv[1]
    id = sys.argv[2]
    bot = GambleBot(token, id)
    bot.listen()


