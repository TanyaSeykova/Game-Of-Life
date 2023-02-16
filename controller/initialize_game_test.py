import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

import unittest
from controller import initialize_game
from entity import people

class TestValidatePlayers(unittest.TestCase):
    def test_empty_name(self):
        # Arrange
        test_data = {'players': [{'player_name': '',
                                  'player_symbol': '😍',
                                  'player_preference': 'Мъже'},
                                 {'player_name': 'j',
                                  'player_symbol': '😃',
                                  'player_preference': 'И двете'}]}

        # Act
        players, err = initialize_game.validate_players(test_data)

        # Assert
        self.assertIsNone(players)
        self.assertEqual(
            err, "Имената на играчите трябва да са поне един символ")

    def test_same_names(self):
        # Arrange
        test_data = {'players': [{'player_name': 'same',
                                  'player_symbol': '😍',
                                  'player_preference': 'Мъже'},
                                 {'player_name': 'same',
                                  'player_symbol': '😃',
                                  'player_preference': 'И двете'}]}

        # Act
        players, err = initialize_game.validate_players(test_data)

        # Assert
        self.assertIsNone(players)
        self.assertEqual(err, "Имената на играчите трябва да са различни")

    def test_same_symbols(self):
        # Arrange
        test_data = {'players': [{'player_name': 'name 1',
                                  'player_symbol': '😍',
                                  'player_preference': 'Мъже'},
                                 {'player_name': 'name 2',
                                  'player_symbol': '😍',
                                  'player_preference': 'И двете'}]}

        # Act
        players, err = initialize_game.validate_players(test_data)

        # Assert
        self.assertIsNone(players)
        self.assertEqual(err, "Символите на играчите трябва да са различни")

    def test_success(self):
        # Arrange

        test_data = {'players': [{'player_name': 'Book',
                                  'player_symbol': '😍',
                                  'player_preference': 'Мъже'},
                                 {'player_name': 'Pen',
                                  'player_symbol': '😃',
                                  'player_preference': 'И двете'}]}
        player1 = people.Player("Book", "😍", people.Preference.MALE)
        player2 = people.Player("Pen", "😃", people.Preference.BOTH)
        # Act
        players, err = initialize_game.validate_players(test_data)

        # Assert
        self.assertEqual(player1.name, players[0].name)
        self.assertEqual(player1.symbol, players[0].symbol)
        self.assertEqual(player1.preference, players[0].preference)
        self.assertEqual(player2.name, players[1].name)
        self.assertEqual(player2.symbol, players[1].symbol)
        self.assertEqual(player2.preference, players[1].preference)
        self.assertEqual(err, "")


if __name__ == '__main__':
    unittest.main()
