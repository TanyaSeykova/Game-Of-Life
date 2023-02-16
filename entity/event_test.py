import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

import unittest
from entity import event
from entity import people


test_job = event.Job("fake-job-1", 100, event.Education.COURSES)


class TestJob(unittest.TestCase):
    def test_is_qualified(self):
        # Act
        is_qualified_none = test_job.is_qualified(event.Education.NONE)
        is_qualified_courses = test_job.is_qualified(event.Education.COURSES)
        is_qualified_university = test_job.is_qualified(
            event.Education.UNIVERSITY)

        # Assert
        self.assertFalse(is_qualified_none)
        self.assertTrue(is_qualified_courses)
        self.assertTrue(is_qualified_university)

    def test_get_current_salary(self):
        # Arrange
        test_job.growth_index = 1.5

        # Act
        result = test_job.get_current_salary(2)

        # Assert
        self.assertEqual(result, 225)


test_investment = event.Investment(
    "fake-investmenr-1", "fake-descr-1", -100, event.Type_Investment.LAND)


class TestInvestment(unittest.TestCase):

    def test_get_current_value(self):
        # Arrange
        test_investment.growth_index = 1.5

        # Act
        result = test_investment.get_current_value()

        # Assert
        self.assertEqual(result, 150)


test_special_event = event.Special_Event(
    "fake-se-1", "fake-descr-1", 100, -100, {"relationship_status": [2, 3]})
test_player = people.Player("Name", "w", people.Preference.BOTH)


class TestSpecialEvent(unittest.TestCase):

    def test_get_current_value(self):
        # Arrange
        test_player.relationship = people.Relationship.MARRIED

        # Act
        result = test_special_event.can_have_event(test_player)

        # Assert
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
