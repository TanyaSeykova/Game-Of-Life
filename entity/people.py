from enum import Enum
import event

import random

class Gender(Enum):
    MALE = 1
    FEMALE = 2

class Relationship(Enum):
    SINGLE = 1
    DATING = 2
    MARRIED = 3

class Preference(Enum):
    MALE = 1
    FEMALE = 2
    BOTH = 3

MAX_STAR_MONEY = 10000
MAX_START_HAPPINESS = 500

MAX_HAPPINESS_RELATIONSHIP = 1000
MIN_HAPPINESS_RELATIONSHIP = -200

class PotentialPartner:
    def __init__(self, name, gender, description):
        self.name = name
        self.gender = gender
        self.description = description
        self.happiness = random.randint(MIN_HAPPINESS_RELATIONSHIP, MAX_HAPPINESS_RELATIONSHIP)
    
class Player:
    def __init__(self, name, symbol, gender, preference):
        self.name = name
        self.symbol = symbol
        self.gender = gender
        self.money = random.randint(0, MAX_STAR_MONEY)
        self.happiness = random.randint(0, MAX_START_HAPPINESS)
        self.is_finished = False
        self.education = event.Education(3) # None
        self.job = (None, 0)
        self.investments = []
        self.relationship = Relationship(1) # Single
        self.preference = preference
        self.children = 0
        
        