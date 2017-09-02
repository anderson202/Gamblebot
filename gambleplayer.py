import random

class Player:

    def __init__(self, name):
        self.name = name
        self.amount = 100

    def roll(self):
        return random.randint(1, 100)

    def bet(self, bet_amount):
        if bet_amount > self.amount:
            return "Not enough money"
        else:
            self.amount -= bet_amount
            return bet_amount

    def __str__(self):
        return self.name
