import random
from entity import event
from entity import initializer
from entity import people
from typing import List

# read from file to load all data


class Board():
    def __init__(self, initializer_: initializer.Initializer) -> None:
        self.jobs = initializer_.get_jobs()
        self.investments = initializer_.get_investments()
        self.items = initializer_.get_items()
        self.special_events = initializer_.get_special_events()
        self.misfortunes = initializer_.get_misfortunes()
        self.love_interests = initializer_.get_people()

    def match_jobs(self, education: event.Education) -> List[event.Job]:
        matched_jobs = []
        for job in self.jobs:
            if job.is_qualified(education):
                matched_jobs.append(job)

        return matched_jobs

    def match_people(self, preference: people.Preference) -> List[people.PotentialPartner]:
        if preference == people.Preference.BOTH:
            return self.love_interests

        matched_people = []
        for person in self.love_interests:
            if person.match_preference(preference):
                matched_people.append(person)

        return matched_people

    def match_special_events(self, player: people.Player) -> List[event.Special_Event]:

        matched_events = []
        for special_event in self.special_events:
            if special_event.can_have_event(player):
                matched_events.append(special_event)

        return matched_events

    def get_random_jobs(self, player: people.Player):
        matched_jobs = self.match_jobs(player.education)
        choices = random.sample(matched_jobs, k=3)
        choices = [j.to_dict() for j in choices]
        return {
            "type_choice": "jobs",
            "choices": choices
        }

    def get_random_investments(self):
        
        choices = random.sample(self.investments, k=3)
        choices = [i.to_dict() for i in choices]
        return {
            "type_choice": "investments",
            "choices": choices
        }

    def get_random_items(self):
        
        choices = random.sample(self.items, k=3)
        
        choices = [i.to_dict() for i in choices]
        return {
            "type_choice": "items",
            "choices": choices
        }

    def get_random_misfortune(self):
        choice = random.choices(self.misfortunes)
        
        choice = [m.to_dict() for m in choice]
        
        return {
            "type_choice": "misfortune",
            "choices": choice
        }

    def get_random_love_interests(self, player: people.Player):
        matched_people = self.match_people(player.preference)
        choices = random.sample(matched_people, k=3)
        choices = [p.to_dict() for p in choices]
        return {
            "type_choice": "people",
            "choices": choices
        }

    def get_random_special_events(self, player: people.Player):
        matched_events = self.match_special_events(player)
        choice = random.choices(matched_events)
        choice = [se.to_dict() for se in choice]
        return {
            "type_choice": "special_event",
            "choices": choice
        }

    def get_random_event(self, include_special: bool, player: people.Player):
        possibilities = ["items", "misfortunes", "investments"]
        if include_special:
            possibilities.append("special")

        choice = random.choice(possibilities)
        print("CHOICE: ", choice)
        if choice == "items":
            return self.get_random_items()
        if choice == "misfortunes":
            return self.get_random_misfortune()
        if choice == "investments":
            return self.get_random_investments()
        if choice == "special":
            return self.get_random_special_events(player)

    def get_choices(self, player: people.Player, roll: int):
        current_pos = player.position + roll
        if current_pos >= 49:
            current_pos = 49
            return {
                "type_choice": "finished",
                "choices": []
            }

        if 1 <= current_pos <= 6:
            if player.education == event.Education.NOT_SELECTED:
                return {
                    "type_choice": "education",
                    "choices": []
                }
            else:
                return self.get_random_event(False, player)
        if 7 <= current_pos <= 12:
            if player.job == (None, 0):
                return self.get_random_jobs(player)
            else:
                return self.get_random_event(False, player)
        if 13 <= current_pos <= 18:
            return self.get_random_event(False, player)
        if 19 <= current_pos <= 24:
            if player.relationship == people.Relationship.SINGLE:
                return self.get_random_love_interests(player)
            else:
                return self.get_random_event(False, player)
        if 25 <= current_pos <= 30:
            return self.get_random_special_events(player)
        if 31 <= current_pos <= 48:
            return self.get_random_event(True, player)
