from typing import List
from entity import event
from entity import people
import json
import os


class Initializer:
    def __init__(self) -> None:
        pass

    def get_investments(self) -> List[event.Investment]:
        f = open('./data/investments.json', encoding="utf8")
        data = json.load(f)
        investments = []
        for investment in data["investments"]:
            investments.append(event.Investment(
                investment["name"], investment["description"], investment["base_price"], investment["type_investment"]))

        f.close()
        return investments

    def get_items(self) -> List[event.Item]:
        f = open('./data/items.json', encoding="utf8")
        data = json.load(f)

        items = []
        for item in data["items"]:
            items.append(event.Item(
                item["name"], item["description"], item["image"], item["happiness"], item["money"]))

        f.close()

        return items

    def get_misfortunes(self) -> List[event.Misfortune]:
        f = open('./data/misfortunes.json', encoding="utf8")
        data = json.load(f)

        misfortunes = []
        for misfortune in data["misfortunes"]:
            misfortunes.append(event.Misfortune(
                misfortune["name"], misfortune["description"], misfortune["happiness"], misfortune["money"], misfortune["side_effects"]))

        f.close()
        return misfortunes

    def get_special_events(self) -> List[event.Special_Event]:
        f = open('./data/special_events.json', encoding="utf8")
        data = json.load(f)

        special_events = []
        for special_event in data["special_events"]:
            special_events.append(event.Special_Event(
                special_event["name"], special_event["description"], special_event["happiness"], special_event["money"], special_event["requirements"]))

        f.close()
        return special_events

    def get_jobs(self) -> List[event.Job]:
        f = open('./data/jobs.json', encoding="utf8")
        data = json.load(f)

        jobs = []
        for job in data["jobs"]:
            jobs.append(
                event.Job(job["name"], job["base_salary"], job["required_qualification"]))

        f.close()
        return jobs

    def get_people(self) -> List[people.PotentialPartner]:
        f = open('./data/love_interests.json', encoding="utf8")
        data = json.load(f)

        partners = []
        for partner in data["love_interests"]:
            partners.append(people.PotentialPartner(
                partner["name"], partner["gender"], partner["description"]))

        f.close()
        return partners
