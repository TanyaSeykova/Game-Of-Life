from enum import IntEnum
from entity import event
import json

import random

class Gender(IntEnum):
    MALE = 1
    FEMALE = 2

class Relationship(IntEnum):
    SINGLE = 1
    DATING = 2
    MARRIED = 3

class Preference(IntEnum):
    MALE = 1
    FEMALE = 2
    BOTH = 3

MAX_STAR_MONEY = 10000
MAX_START_HAPPINESS = 500

MAX_HAPPINESS_RELATIONSHIP = 1000
MIN_HAPPINESS_RELATIONSHIP = -200

class PotentialPartner:
    def __init__(self, name: str, gender: Gender, description: str):
        self.name = name
        self.gender = gender
        self.description = description
        self.happiness = random.randint(MIN_HAPPINESS_RELATIONSHIP, MAX_HAPPINESS_RELATIONSHIP)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def match_preference(self, preference: Preference):
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
        self.money = random.randint(0, MAX_STAR_MONEY)
        self.happiness = random.randint(0, MAX_START_HAPPINESS)
        self.is_finished = False
        self.position = 0
        self.education = event.Education(3) # None
        self.job = (None, 0) # job and years on position
        self.investments = []
        self.relationship = Relationship(1) # Single
        self.preference = preference
        self.children = 0
    
    def toJSON(self):
        return json.dumps({
            "name": self.name,
            "symbol": self.symbol,
            "money": self.money,
            "happiness": self.happiness,
            "is_finished": self.is_finished,
            "position": self.position,
            "job": {
                "job_name": self.job[0],
                "years_on_pos": self.job[1]
            },
            "investments": self.investments,
            "relationship": self.relationship,
            "preference": self.preference,
            "children": self.children,
            "position": self.position,
        })
        
    def to_dict(self):
        return {
            'name': self.name,
            'symbol': self.symbol,
            'money': self.money,
            'happiness': self.happiness,
            'is_finished': self.is_finished,
            'position': self.position,
            'education': self.education.value,
            'job': self.job[0],
            'job_years': self.job[1],
            'investments': self.investments,
            'relationship': self.relationship.value,
            'preference': self.preference.value,
            'children': self.children
        }
    def to_json(self):
        return json.dumps(self.to_dict())
        
        