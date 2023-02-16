from mapper import common


def validate_players(raw_data):
    player1, player2 = common.raw_data_to_players(raw_data)
    if player1.name == player2.name:
        return None, "Имената на играчите трябва да са различни"
    if player1.symbol == player2.symbol:
        return None, "Символите на играчите трябва да са различни"
    if player1.name == "" or player2.name == "":
        return None, "Имената на играчите трябва да са поне един символ"

    return (player1, player2), ""
