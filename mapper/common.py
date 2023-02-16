from entity import people
from typing import List


def raw_data_to_players(raw_data):
    player_array = raw_data["players"]
    player1 = people.Player(
        player_array[0]["player_name"],
        player_array[0]["player_symbol"],
        preference_str_to_preference_enum(
            player_array[0]["player_preference"]))
    player2 = people.Player(
        player_array[1]["player_name"],
        player_array[1]["player_symbol"],
        preference_str_to_preference_enum(
            player_array[1]["player_preference"]))

    return player1, player2


def request_to_player_turn(data):
    return data["player_turn"]


def preference_str_to_preference_enum(pref: str) -> people.Preference:
    if pref == "Мъже":
        return people.Preference.MALE
    if pref == "Жени":
        return people.Preference.FEMALE
    return people.Preference.BOTH
