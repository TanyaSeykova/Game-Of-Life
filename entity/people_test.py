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


class TestPotentialPartner(unittest.TestCase):
    def test_match_preference_true_both(self):
        # Assert
        pref = people.Preference.BOTH
        test_partner = people.PotentialPartner("fake-name-1", people.Gender.FEMALE, "fake-descr-1")
        
        # Act
        result = test_partner.match_preference(pref)
        
        # Assert
        self.assertTrue(result)
        
    def test_match_preference_true_exact(self):
        # Assert
        pref = people.Preference.FEMALE
        test_partner = people.PotentialPartner("fake-name-1", people.Gender.FEMALE, "fake-descr-1")
        
        # Act
        result = test_partner.match_preference(pref)
        
        # Assert
        self.assertTrue(result)
        
    def test_match_preference_false(self):
        # Assert
        pref = people.Preference.MALE
        test_partner = people.PotentialPartner("fake-name-1", people.Gender.FEMALE, "fake-descr-1")
        
        # Act
        result = test_partner.match_preference(pref)
        
        # Assert
        self.assertFalse(result)


class TestPlayer(unittest.TestCase):
    def test_process_education_none(self):
        # Arrange
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        # Act
        
        test_player.process_education(0)
        
        # Assert
        self.assertEqual(test_player.money, 3000)
        self.assertEqual(test_player.education, event.Education.NONE)
        
    def test_process_education_courses(self):
        # Arrange
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        # Act
        
        test_player.process_education(1)
        
        # Assert
        self.assertEqual(test_player.money, -1000)
        self.assertEqual(test_player.education, event.Education.COURSES)
    
    def test_process_education_university(self):
        # Arrange
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        # Act
        
        test_player.process_education(2)
        
        # Assert
        self.assertEqual(test_player.money, -3500)
        self.assertEqual(test_player.education, event.Education.UNIVERSITY)
        
    def test_process_job(self):
        # Arrange 
        jobs = [event.Job("fake-job-1", 100, event.Education.NONE),
                   event.Job("fake-job-2", 300, event.Education.COURSES),
                   event.Job("fake-job-3", 100, event.Education.UNIVERSITY)]
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        
        # Act 
        test_player.process_job(1, jobs)
        
        # Assert
        self.assertEqual(test_player.job, (jobs[1], 0))
        
    def test_process_investments(self):
        # Arrange 
        i1 = event.Investment("fake-investmenr-1", "fake-descr-1", -100, event.Type_Investment.LAND)
        i2 = event.Investment("fake-investmenr-2", "fake-descr-2", -200, event.Type_Investment.REAL_ESTATE)
        i3 = event.Investment("fake-investmenr-3", "fake-descr-3", -300, event.Type_Investment.STOCK)
        i0 = event.Investment("fake-investmenr-0", "fake-descr-0", 0, event.Type_Investment.LAND)
        investments = [i1, i2, i3]
        
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.investments = [i0]
        
        # Act 
        test_player.process_investment(1, investments)
        
        # Assert
        self.assertEqual(test_player.investments, [i0, i2])
        self.assertEqual(test_player.money, -200)
        
    def test_process_item(self):
        # Arrange 
        i1 = event.Item("fake-item-1", "fake-descr-1", "fake-img-1", 100, -100)
        i2 = event.Item("fake-item-2", "fake-descr-2", "fake-img-2", 200, -200)
        i3 = event.Item("fake-item-3", "fake-descr-3", "fake-img-3", 300, -300)
        items = [i1, i2, i3]
        
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        
        # Act 
        test_player.process_item(1, items)
        
        # Assert
        self.assertEqual(test_player.happiness, 200)
        self.assertEqual(test_player.money, -200)
    
    def test_process_people(self):
        # Arrange 
        
        p1 = people.PotentialPartner("fake-name-1", people.Gender.FEMALE, "fake-descr-1")
        p2 = people.PotentialPartner("fake-name-2", people.Gender.FEMALE, "fake-descr-2")
        p3 = people.PotentialPartner("fake-name-3", people.Gender.MALE, "fake-descr-3")
        people_ = [p1, p2, p3]
        
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.happiness = 0
        p2.happiness = 100
        
        # Act 
        test_player.process_people(1, people_)
        
        # Assert
        self.assertEqual(test_player.happiness, 100)
        self.assertEqual(test_player.relationship, people.Relationship.DATING)
        
    def test_misfortune_none(self):
        # Arrange
        m = event.Misfortune("fake-m-3", "fake-descr-3", -100, -100, event.Side_Effect.NONE)
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        
        # Act 
        test_player.process_misfortune([m])
        
        # Assert
        self.assertEqual(test_player.happiness, -100)
        self.assertEqual(test_player.money, -100)
        
    def test_misfortune_lose_stock(self):
        # Arrange
        m = event.Misfortune("fake-m-3", "fake-descr-3", -100, -100, event.Side_Effect.LOSE_STOCK)
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        i1 = event.Investment("fake-investmenr-1", "fake-descr-1", -100, event.Type_Investment.LAND)
        i2 = event.Investment("fake-investmenr-2", "fake-descr-2", -200, event.Type_Investment.REAL_ESTATE)
        i3 = event.Investment("fake-investmenr-3", "fake-descr-3", -300, event.Type_Investment.STOCK)
        test_player.investments = [i1, i2, i3]
        
        # Act 
        test_player.process_misfortune([m])
        
        # Assert
        self.assertEqual(test_player.happiness, -100)
        self.assertEqual(test_player.money, -100)
        self.assertEqual(test_player.investments, [i1, i2])
        
    def test_misfortune_lose_land(self):
        # Arrange
        m = event.Misfortune("fake-m-3", "fake-descr-3", -100, -100, event.Side_Effect.LOSE_LAND)
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        i1 = event.Investment("fake-investmenr-1", "fake-descr-1", -100, event.Type_Investment.LAND)
        i2 = event.Investment("fake-investmenr-2", "fake-descr-2", -200, event.Type_Investment.REAL_ESTATE)
        i3 = event.Investment("fake-investmenr-3", "fake-descr-3", -300, event.Type_Investment.STOCK)
        test_player.investments = [i1, i2, i3]
        
        # Act 
        test_player.process_misfortune([m])
        
        # Assert
        self.assertEqual(test_player.happiness, -100)
        self.assertEqual(test_player.money, -100)
        self.assertEqual(test_player.investments, [i2, i3])
        
    def test_misfortune_lose_real_estate(self):
        # Arrange
        m = event.Misfortune("fake-m-3", "fake-descr-3", -100, -100, event.Side_Effect.LOSE_REAL_ESTATE)
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        i1 = event.Investment("fake-investmenr-1", "fake-descr-1", -100, event.Type_Investment.LAND)
        i2 = event.Investment("fake-investmenr-2", "fake-descr-2", -200, event.Type_Investment.REAL_ESTATE)
        i3 = event.Investment("fake-investmenr-3", "fake-descr-3", -300, event.Type_Investment.STOCK)
        test_player.investments = [i1, i2, i3]
        
        # Act 
        test_player.process_misfortune([m])
        
        # Assert
        self.assertEqual(test_player.happiness, -100)
        self.assertEqual(test_player.money, -100)
        self.assertEqual(test_player.investments, [i1, i3])
    
    def test_special_event_basic(self):
        # Arrange
        se = event.Special_Event("fake-se-2", "fake-descr-2", 100, -100, {})
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        
        # Act 
        test_player.process_special_event([se])
        
        # Assert
        self.assertEqual(test_player.happiness, 100)
        self.assertEqual(test_player.money, -100)
        
    def test_special_event_wedding(self):
        # Arrange
        se = event.Special_Event("Сватба", "fake-descr-2", 100, -100, {})
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        test_player.relationship = people.Relationship.DATING
        
        # Act 
        test_player.process_special_event([se])
        
        # Assert
        self.assertEqual(test_player.happiness, 100)
        self.assertEqual(test_player.money, -100)
        self.assertEqual(test_player.relationship, people.Relationship.MARRIED)
    
    def test_special_event_baby(self):
        # Arrange
        se = event.Special_Event("Бебе", "fake-descr-2", 100, -100, {})
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        test_player.happiness = 0
        test_player.children = 1
        
        # Act 
        test_player.process_special_event([se])
        
        # Assert
        self.assertEqual(test_player.happiness, 100)
        self.assertEqual(test_player.money, -100)
        self.assertEqual(test_player.children, 2)
        
    def test_process_turn_pass(self):
        # Arrange
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 0
        job = event.Job("fake-job-1", 100, event.Education.NONE)
        job.growth_index = 2
        
        test_player.job = (job, 2)
        
        # Act
        test_player.process_turn_pass()
        
        # Assert
        self.assertEqual(test_player.job, (job, 3))
        self.assertEqual(test_player.money, 800)
        
    def test_evaluate_player(self):
        # Arrange
        test_player = people.Player("Name", "w", people.Preference.BOTH)
        test_player.money = 30
        test_player.happiness = 5
        test_player.children = 1
        
        i0 = event.Investment("fake-investmenr-0", "fake-descr-0", -100, event.Type_Investment.LAND)
        i0.growth_index = 2
        test_player.investments = [i0]

        
        # Act
        result = test_player.evaluate_player()
        
        # Assert
        self.assertEqual(result, 580)
        
        
if __name__ == '__main__':
    unittest.main()