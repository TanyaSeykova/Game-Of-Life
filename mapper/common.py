import json
from entity import people

def rawDataToPlayers(raw_data):
    player_array = raw_data["players"]
    player1 = people.Player(player_array[0]["player_name"], player_array[0]["player_symbol"], player_array[0]["player_preference"])
    player2 = people.Player(player_array[1]["player_name"], player_array[1]["player_symbol"], player_array[1]["player_preference"])
    
    return player1, player2

def requestToPlayerTurn(data):
    return data["player_turn"]