from flask import Flask, jsonify, request, render_template
import json
from entity import initializer
from controller import initialize_game
from controller import play_game
from entity import people
from entity import board
from mapper import common as cmnmapper


app = Flask(__name__)

# variables
player1: people.Player = None
player2: people.Player = None
game_board_var: board.Board = None
initializer_var = initializer.Initializer()
current_choices = None


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/process_data", methods=["POST"])
def process_data():
    data = request.get_json()
    players, err = initialize_game.validate_players(data)
    if err != "":
        return jsonify({"error": err})
    
    global player1, player2
    player1, player2 = players
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/game_board')
def redirect_game_board():
    return render_template("game_board.html")

@app.route('/load_game_board')
def game_board():
    global game_board_var
    game_board_var = board.Board(initializer_var)
    return jsonify({"player1": player1.to_json(), "player2": player2.to_json()})


@app.route('/roll_and_give_choices', methods=["POST"])
def roll_and_give_choices():
    data = request.get_json()
    roll = play_game.roll_dice()
    player_turn = cmnmapper.request_to_player_turn(data)
    global current_choices
    if player_turn == 1:
        current_choices = game_board_var.get_choices(player1, roll)
        result = jsonify({"generated_choices" : current_choices, "position_player": player1.position, "rolled" : roll})
        player1.position += roll
        if player1.position >= 49:
            player1.position = 49
            player1.is_finished = True
        return result
    else:
        current_choices = game_board_var.get_choices(player2, roll)
        result = jsonify({"generated_choices" : current_choices, "position_player": player2.position, "rolled" : roll})
        player2.position += roll
        if player2.position >= 49:
            player2.position = 49
            player2.is_finished = True
        return result
    
        
@app.route('/get_players')
def get_players():
    return jsonify({"player1": player1.to_json(), "player2": player2.to_json()})

@app.route("/process_choice", methods=["POST"])
def process_choice():
    data = request.get_json()
    player_turn = cmnmapper.request_to_player_turn(data)
    index_choice = data["index_choice"]
    if player_turn == 1:
        player1.process_choice(current_choices, index_choice)
    else:
        player2.process_choice(current_choices, index_choice)
    return jsonify({"status" : "success"})

@app.route("/skip_event", methods=["POST"])
def skip_event():
    data = request.get_json()
    player_turn = cmnmapper.request_to_player_turn(data)
    if player_turn == 1:
        player1.process_turn_pass()
    else:
        player2.process_turn_pass()
    return jsonify({"status" : "success"})

@app.route('/get_results')
def get_results():
    return jsonify({"player_1_score": player1.evaluate_player(), "player_2_score": player2.evaluate_player()})

if __name__ == '__main__':
    app.run(debug=True)