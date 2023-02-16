import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

import unittest
from mapper import common as cmnmapper
from entity import people
from entity import event

class TestRawDataToPlayers(unittest.TestCase):
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
        player1_res, player2_res = cmnmapper.raw_data_to_players(test_data)

        # Assert
        self.assertEqual(player1.name, player1_res.name)
        self.assertEqual(player1.symbol, player1_res.symbol)
        self.assertEqual(player1.preference, player1_res.preference)
        self.assertEqual(player2.name, player2_res.name)
        self.assertEqual(player2.symbol, player2_res.symbol)
        self.assertEqual(player2.preference, player2_res.preference)

class TestRequestToPlayerTurn(unittest.TestCase):
    def test_success(self):
        # Arrange
        request = {'player_turn': 1}
        
        # Act 
        response = cmnmapper.request_to_player_turn(request)
        
        # Assert 
        self.assertEqual(response, 1)
       
class TestPreferenceStrToPreferenceEnum(unittest.TestCase):
    def test_male(self):
        # Arrange
        pref = "Мъже"
         
        # Act 
        result = cmnmapper.preference_str_to_preference_enum(pref)
         
        # Assert
        self.assertEqual(result, people.Preference.MALE)
        
    def test_female(self):
        # Arrange
        pref = "Жени"
         
        # Act 
        result = cmnmapper.preference_str_to_preference_enum(pref)
         
        # Assert
        self.assertEqual(result, people.Preference.FEMALE)
    
    def test_both(self):
        # Arrange
        pref = "И двете"
         
        # Act 
        result = cmnmapper.preference_str_to_preference_enum(pref)
         
        # Assert
        self.assertEqual(result, people.Preference.BOTH)
         
        
if __name__ == '__main__':
    unittest.main()
