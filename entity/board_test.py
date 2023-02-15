import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity import board
from entity import initializer
from entity import event
from entity import people

import unittest

initializer_var = initializer.Initializer()
test_board = board.Board(initializer_var)
test_player = people.Player("Name", "w", people.Preference.BOTH)

test_board.jobs = [event.Job("fake-job-1", 100, event.Education.NONE),
                   event.Job("fake-job-2", 300, event.Education.COURSES),
                   event.Job("fake-job-3", 100, event.Education.UNIVERSITY)]
test_board.investments = [event.Investment("fake-investmenr-1", "fake-descr-1", 100, event.Type_Investment.LAND),
                          event.Investment("fake-investmenr-2", "fake-descr-2", 100, event.Type_Investment.REAL_ESTATE), 
                          event.Investment("fake-investmenr-3", "fake-descr-3", 100, event.Type_Investment.STOCK)]
test_board.items = [event.Item("fake-item-1", "fake-descr-1", "fake-img-1", 100, -100),
                    event.Item("fake-item-2", "fake-descr-2", "fake-img-2", 100, -100),
                    event.Item("fake-item-3", "fake-descr-3", "fake-img-3", 100, -100)]
test_board.special_events = [event.Special_Event("fake-se-1", "fake-descr-1", 100, -100, {"relationship_status": [2, 3]}),
                             event.Special_Event("fake-se-2", "fake-descr-2", 100, -100, {}),
                             event.Special_Event("fake-se-3", "fake-descr-3", 100, -100, {})]
test_board.misfortunes = [event.Misfortune("fake-m-1", "fake-descr-1", 100, -100, event.Side_Effect.NONE),
                          event.Misfortune("fake-m-2", "fake-descr-2", 100, -100, event.Side_Effect.NONE),
                          event.Misfortune("fake-m-3", "fake-descr-3", 100, -100, event.Side_Effect.NONE)]
test_board.love_interests = [people.PotentialPartner("fake-name-1", people.Gender.FEMALE, "fake-descr-1"),
                             people.PotentialPartner("fake-name-2", people.Gender.FEMALE, "fake-descr-2"),
                             people.PotentialPartner("fake-name-3", people.Gender.MALE, "fake-descr-3")]


class TestBoard(unittest.TestCase):
    def test_match_jobs(self):
        # Act
        matched_jobs = test_board.match_jobs(event.Education.COURSES)
        
        # Assert
        self.assertEqual(matched_jobs, [test_board.jobs[0], test_board.jobs[1]])
    
    def test_match_people(self):
        # Act
        matched_male = test_board.match_people(people.Preference.MALE)
        matched_female = test_board.match_people(people.Preference.FEMALE)
        matched_both = test_board.match_people(people.Preference.BOTH)
        
        # Assert
        self.assertEqual(matched_male, [test_board.love_interests[2]])
        self.assertEqual(matched_female, [test_board.love_interests[0],test_board.love_interests[1] ])
        self.assertEqual(matched_both, [test_board.love_interests[0],test_board.love_interests[1], test_board.love_interests[2]])
        
    def test_match_special_event(self):
        # Arrange
        test_player.relationship = people.Relationship.SINGLE
        
        # Act
        matched_event = test_board.match_special_events(test_player)
        
        # Assert
        self.assertNotIn(matched_event, [test_board.special_events[1], test_board.special_events[2]])
        self.assertNotEqual(matched_event, test_board.special_events[0])
        
    def test_get_choices_education(self):
        # Arrange
        test_player.position = 1
        
        # Act 
        result = test_board.get_choices(test_player, 1)
        
        # Assert
        self.assertEqual(result["type_choice"], "education")
    
    def test_get_choices_job(self):
        # Arrange
        test_player.education = event.Education.UNIVERSITY
        test_player.position = 7
        
        # Act 
        result = test_board.get_choices(test_player, 1)
        
        # Assert
        self.assertEqual(result["type_choice"], "jobs")
        
    def test_get_choices_event(self):
        # Arrange
        test_player.position = 13
        
        # Act 
        result = test_board.get_choices(test_player, 1)
        
        # Assert
        self.assertIn(result["type_choice"], ["investments", "items", "misfortune"])
        
    def test_get_choices_person(self):
        # Arrange
        test_player.position = 19
        
        # Act 
        result = test_board.get_choices(test_player, 1)
        
        # Assert
        self.assertEqual(result["type_choice"], "people")
        
    def test_get_choices_special_event(self):
        # Arrange
        test_player.position = 25
        
        # Act 
        result = test_board.get_choices(test_player, 1)
        
        # Assert
        self.assertEqual(result["type_choice"], "special_event")
        
    def test_get_choices_events_later(self):
        # Arrange
        test_player.position = 31
        
        # Act 
        result = test_board.get_choices(test_player, 1)
        
        # Assert
        self.assertIn(result["type_choice"], ["investments", "items", "misfortune", "special_event"])
        
    def test_get_choices_finished(self):
        # Arrange
        test_player.position = 47
        
        # Act 
        result = test_board.get_choices(test_player, 5)
        
        # Assert
        self.assertEqual(result["type_choice"], "finished")
        
        
if __name__ == '__main__':
    unittest.main()