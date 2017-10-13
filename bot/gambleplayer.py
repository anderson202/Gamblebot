import random

class Player:

    def __init__(self, name, amount=100):
        self.name = name
        self.amount = amount

    def roll(self):
        return random.randint(1, 100)

    def bet(self, bet_amount):
        if bet_amount > self.amount or bet_amount < 0:
            return 0
        else:
            self.amount -= bet_amount
            return bet_amount

    def gift(self, amount, player):
        if self.amount >= amount and amount > 0:
            player.amount += amount
            self.amount -= amount
            return amount
        else:
            return 0

    def __str__(self):
        return self.name
