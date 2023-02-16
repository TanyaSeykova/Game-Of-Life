# pylint: disable=missing-module-docstring
from enum import IntEnum
from typing import List
from entity import event
import json

import random


class Gender(IntEnum):
    MALE = 1
    FEMALE = 2

    def to_json(self):
        return self.value


class Relationship(IntEnum):
    SINGLE = 1
    DATING = 2
    MARRIED = 3

    def to_json(self):
        return self.value


class Preference(IntEnum):
    MALE = 1
    FEMALE = 2
    BOTH = 3

    def to_json(self):
        return self.value


MAX_START_MONEY = 10000
MAX_START_HAPPINESS = 500

MAX_HAPPINESS_RELATIONSHIP = 2000
MIN_HAPPINESS_RELATIONSHIP = -200


class PotentialPartner:
    def __init__(self, name: str, gender: Gender, description: str):
        self.name = name
        self.gender = gender
        self.description = description
        self.happiness = random.randint(
            MIN_HAPPINESS_RELATIONSHIP,
            MAX_HAPPINESS_RELATIONSHIP)


    def match_preference(self, preference: Preference):
        if preference == Preference.BOTH:
            return True
        return self.gender == preference

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "description": self.description,
            "happiness": self.happiness,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Player:
    def __init__(self, name: str, symbol: str, preference: Preference):
        self.name = name
        self.symbol = symbol
        self.money = random.randint(0, MAX_START_MONEY)
        self.happiness = random.randint(0, MAX_START_HAPPINESS)
        self.is_finished = False
        self.position = 0
        self.education = event.Education.NOT_SELECTED
        self.job = (None, 0)  # job and years on position
        self.investments = []
        self.relationship = Relationship.SINGLE  # Single
        self.preference = preference
        self.children = 0

    def get_job(self):
        if self.job[0] is None:
            return None
        return self.job[0].to_json()

    def get_investments(self):
        return [i.to_json() for i in self.investments]

    def to_dict(self):
        return {
            'name': self.name,
            'symbol': self.symbol,
            'money': self.money,
            'happiness': self.happiness,
            'is_finished': self.is_finished,
            'position': self.position,
            'education': self.education,
            'job': self.get_job(),
            'job_years': self.job[1],
            'investments': self.get_investments(),
            'relationship': self.relationship,
            'preference': self.preference,
            'children': self.children
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def process_education(self, index_choice: int):
        if index_choice == 0:  # None
            self.money += 3000
            self.education = event.Education.NONE
        if index_choice == 1:  # Courses
            self.money -= 1000
            self.education = event.Education.COURSES
        if index_choice == 2:  # University
            self.money -= 3500
            self.education = event.Education.UNIVERSITY

    def process_job(self, index_choice: int, choices: List[event.Job]):
        self.job = (choices[index_choice], 0)

    def process_investment(self, index_choice: int,
                           choices: List[event.Investment]):
        self.investments.append(choices[index_choice])
        self.money += choices[index_choice].base_price

    def process_item(self, index_choice: int, choices: List[event.Item]):
        self.money += choices[index_choice].money
        self.happiness += choices[index_choice].happiness

    def process_people(
            self,
            index_choice: int,
            choices: List[PotentialPartner]):
        self.happiness += choices[index_choice].happiness
        self.relationship = Relationship.DATING

    def process_misfortune(self, choices: List[event.Misfortune]):
        choice = choices[0]
        self.money += choice.money
        self.happiness += choice.happiness

        if choice.side_effects == event.Side_Effect.NONE:
            pass
        elif choice.side_effects == event.Side_Effect.LOSE_STOCK:
            objects_to_remove = [
                obj for obj in self.investments if obj.type_investment == event.Type_Investment.STOCK]
            if len(objects_to_remove):
                if objects_to_remove:
                    self.investments.remove(random.choice(objects_to_remove))
        elif choice.side_effects == event.Side_Effect.LOSE_LAND:
            objects_to_remove = [
                obj for obj in self.investments if obj.type_investment == event.Type_Investment.LAND]
            if len(objects_to_remove):
                if objects_to_remove:
                    self.investments.remove(random.choice(objects_to_remove))
        elif choice.side_effects == event.Side_Effect.LOSE_REAL_ESTATE:
            objects_to_remove = [
                obj for obj in self.investments if obj.type_investment == event.Type_Investment.REAL_ESTATE]
            if len(objects_to_remove):
                if objects_to_remove:
                    self.investments.remove(random.choice(objects_to_remove))

    def process_special_event(self, choices: List[event.Special_Event]):
        choice = choices[0]
        self.money += choice.money
        self.happiness += choice.happiness

        if choice.name == "Сватба":
            self.relationship = Relationship.MARRIED
        if choice.name == "Бебе":
            self.children += 1

    def process_turn_pass(self):
        if self.job != (None, 0):
            self.job = (self.job[0], self.job[1] + 1)
            turn_wage = self.job[0].base_salary * \
                (self.job[0].growth_index**self.job[1])

            self.money += turn_wage

    def process_choice(self, current_choices: dict, index_choice: int):
        self.process_turn_pass()
        type_choice = current_choices["type_choice"]
        choices = current_choices["choices"]

        if type_choice == "education":
            self.process_education(index_choice)
        elif type_choice == "jobs":
            self.process_job(index_choice, json_array_to_job_list(choices))
        elif type_choice == "investments":
            self.process_investment(
                index_choice, json_array_to_investment_list(choices))
        elif type_choice == "items":
            self.process_item(index_choice, json_array_to_item_list(choices))
        elif type_choice == "misfortune":
            self.process_misfortune(json_array_to_misfortune_list(choices))
        elif type_choice == "people":
            self.process_people(
                index_choice,
                json_array_to_people_list(choices))
        elif type_choice == "special_event":
            self.process_special_event(
                json_array_to_special_event_list(choices))

    def evaluate_player(self):
        sum_ = 0
        sum_ += self.money
        sum_ += self.happiness * 10
        sum_ += self.children * 300
        for investment in self.investments:
            sum_ += investment.get_current_value()
        return sum_


# mappers
def json_array_to_item_list(json_array: List[dict]) -> List[event.Item]:
    item_list = []
    for item in json_array:
        item_list.append(
            event.Item(
                item['name'],
                item['description'],
                item['image'],
                item['happiness'],
                item['money']))
    return item_list


def json_array_to_investment_list(
        json_array: List[dict]) -> List[event.Investment]:
    investment_list = []
    for item in json_array:
        investment_list.append(
            event.Investment(
                item['name'],
                item['description'],
                item['base_price'],
                item['type_investment']))
    return investment_list


def json_array_to_misfortune_list(
        json_array: List[dict]) -> List[event.Misfortune]:
    misfortune_list = []
    for item in json_array:
        misfortune_list.append(
            event.Misfortune(
                item['name'],
                item['description'],
                item['happiness'],
                item['money'],
                item['side_effects']))
    return misfortune_list


def json_array_to_special_event_list(
        json_array: List[dict]) -> List[event.Special_Event]:
    special_event_list = []
    for item in json_array:
        special_event_list.append(
            event.Special_Event(
                item['name'],
                item['description'],
                item['happiness'],
                item['money'],
                item['requirements']))
    return special_event_list


def json_array_to_job_list(json_array: List[dict]) -> List[event.Job]:
    job_list = []
    for item in json_array:
        job_list.append(
            event.Job(
                item['name'],
                item['base_salary'],
                item['required_qualification']))
    return job_list


def json_array_to_people_list(
        json_array: List[dict]) -> List[PotentialPartner]:
    people_list = []
    for item in json_array:
        people_list.append(
            PotentialPartner(
                item['name'],
                item['gender'],
                item['description']))
    return people_list
