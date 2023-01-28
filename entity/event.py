from enum import Enum
import random

class Education(Enum):
    UNIVERSITY = 1
    COURSES = 2
    NONE = 3

class Job:
    def __init__(self, name, base_salary, required_qualification):
        self.name = name
        self.base_salary = base_salary
        self.growth_index = round(random.uniform(1.01, 1.5), 2)
        self.required_qualification = required_qualification

    def is_qualified(self, qualification) -> bool:
        if qualification <= self.required_qualification:
            return True
        return False
    
    def get_current_salary(self, years_worked):
        return self.base_salary * pow(self.growth_index, years_worked)

class Event:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Type_Investment(Enum):
    STOCK = 1
    REAL_ESTATE = 2
    LAND = 3

class Investment(Event):
    def __init__(self, name, description, base_price, type_investment):
        super().__init__(name, description)
        self.base_price = base_price
        self.growth_index = round(random.uniform(0.5, 2), 2)
        self.type_investment = type_investment
    
    def get_current_value(self, years_owned):
        return self.base_price * pow(self.growth_index, years_owned)

class Item(Event):
    def __init__(self, name, description, image, happiness, money):
        super().__init__(name, description)
        self.image = image
        self.happiness = happiness
        self.money = money

class Side_Effect(Enum):
    LOSE_STOCK = 1
    LOSE_REAL_ESTATE = 2
    LOSE_LAND = 3

class Misfortunes(Event):
    def __init__(self, name, description, happiness, money, side_effects):
        super().__init__(name, description)
        self.happiness = happiness
        self.money = money
        self.side_effects = side_effects

class Special_Event(Event):
    def __init__(self, name, description, happiness, money, requirements):
        super().__init__(name, description)
        self.happiness = happiness
        self.money = money
        self.requirements = requirements

