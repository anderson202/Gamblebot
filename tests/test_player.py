import unittest
from bot.gambleplayer import Player

class Test(unittest.TestCase):

    def setUp(self):
        self.player = Player("John")
        self.other_player = Player("Appleseed", 200)

    def test_default_param(self):
        self.assertEqual(self.player.amount, 100)

    def test_optional_param(self):
        self.assertEqual(self.other_player.amount, 200)

    def test_roll(self):
        self.assertTrue(type(self.player.roll() == int))

    def test_bet_negative(self):
        self.assertEqual(self.player.bet(-1), 0)

    def test_bet_greater(self):
        self.assertEqual(self.player.bet(200), 0)

    def test_bet(self):
        self.assertEqual(self.player.bet(10), 10)

    def test_gift_negative(self):
        self.assertEqual((self.player.gift(-10, self.other_player)), 0)

    def test_gift_greater(self):
        self.assertEqual((self.player.gift(200, self.other_player)), 0)

    def test_gift(self):
        self.assertEqual((self.player.gift(10, self.other_player)), 10)
        self.assertEqual(self.other_player.amount, 210)



if __name__ == '__main__':
    unittest.main()

