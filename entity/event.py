from enum import IntEnum
import json
import random

class Education(IntEnum):
    UNIVERSITY = 1
    COURSES = 2
    NONE = 3
    NOT_SELECTED = 4
    
    def to_json(self):
        return self.value

class Job:
    def __init__(self, name: str, base_salary: int, required_qualification: Education):
        self.name = name
        self.base_salary = base_salary
        self.growth_index = round(random.uniform(1.05, 1.1), 2)
        self.required_qualification = required_qualification

    def is_qualified(self, qualification: Education) -> bool:
        if qualification <= self.required_qualification:
            return True
        return False
    
    def get_current_salary(self, years_worked):
        return self.base_salary * pow(self.growth_index, years_worked)
    
    def to_dict(self):
        return {
            "name": self.name,
            "base_salary": self.base_salary,
            "growth_index": self.growth_index,
            "required_qualification": self.required_qualification
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

class Event:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Type_Investment(IntEnum):
    STOCK = 1
    REAL_ESTATE = 2
    LAND = 3
    
    def to_json(self):
        return self.value

class Investment(Event):
    def __init__(self, name: str, description: str, base_price: int, type_investment: Type_Investment):
        super().__init__(name, description)
        self.base_price = base_price
        self.growth_index = round(random.uniform(0.5, 2), 2)
        self.type_investment = type_investment
    
    def get_current_value(self):
        return -self.base_price * self.growth_index
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "base_price": self.base_price,
            "growth_index": self.growth_index,
            "type_investment": self.type_investment
        }

    def to_json(self):
        return json.dumps(self.to_dict())

class Item(Event):
    def __init__(self, name: str, description: str, image: str, happiness: int, money: int):
        super().__init__(name, description)
        self.image = image
        self.happiness = happiness
        self.money = money
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "happiness": self.happiness,
            "money": self.money
        }

    def to_json(self):
        return json.dumps(self.to_dict())

class Side_Effect(IntEnum):
    LOSE_STOCK = 1
    LOSE_REAL_ESTATE = 2
    LOSE_LAND = 3
    NONE = 4
    
    def to_json(self):
        return self.value

class Misfortune(Event):
    def __init__(self, name: str, description: str, happiness: int, money: int, side_effects: Side_Effect):
        super().__init__(name, description)
        self.happiness = happiness
        self.money = money
        self.side_effects = side_effects
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "happiness": self.happiness,
            "money": self.money,
            "side_effects": self.side_effects
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Special_Event(Event):
    def __init__(self, name: str, description: str, happiness: int, money: int, requirements: dict):
        super().__init__(name, description)
        self.happiness = happiness
        self.money = money
        self.requirements = requirements
        
    def can_have_event(self, player):
        if self.requirements == {}:
            return True
        
        if "relationship_status" in self.requirements:
            if player.relationship not in self.requirements["relationship_status"]:
                return False
            
        if "min_num_children" in self.requirements:
            if player.children < self.requirements["min_num_children"]:
                return False
            
        return True

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "happiness": self.happiness,
            "money": self.money,
            "requirements": self.requirements
        }

    def to_json(self):
        return json.dumps(self.to_dict())
        