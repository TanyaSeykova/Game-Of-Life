const type_choice_education = "education"
const type_choice_investments = "investments"
const type_choice_items = "items"
const type_choice_jobs = "jobs"
const type_choice_people = "people"
const type_choice_misfortune = "misfortune"
const type_choice_special_event = "special_event"

const width_table = 7

let mapEducation = {
    1: "Университет",
    2: "Курсове",
    3: "Без"
}

let mapRelationShip = {
    1: "Сам / Сама",
    2: "Във връзка",
    3: "Женен / Омъжена",
}

var playerOnTurn = 1
function jobToString(jobName) {
    if (jobName == null) {
        return "Без"
    }
    return jobName
}

$.ajax({
    type: "GET",
    url: "/load_game_board",
    success: function (response) {
        populatePlayers(response)
    }
});

function populatePlayers(players) {
    let player1 = JSON.parse(players["player1"])
    let player2 = JSON.parse(players["player2"])

    console.log(player1)
    console.log(player1["job"]["job_name"] == null)
    document.getElementById("name_span_1").textContent = player1["name"]
    document.getElementById("symbol_span_1").textContent = player1["symbol"]
    document.getElementById("money_span_1").textContent = player1["money"]
    document.getElementById("happiness_span_1").textContent = player1["happiness"]
    document.getElementById("education_span_1").textContent = mapEducation[player1["education"]]
    document.getElementById("children_span_1").textContent = player1["children"]
    document.getElementById("relationship_span_1").textContent = mapRelationShip[player1["relationship"]]
    document.getElementById("investments_span_1").textContent = player1["investments"].join(', ')
    document.getElementById("job_span_1").textContent = jobToString(player1["job"]["job_name"])
    document.getElementById("job_years_span_1").textContent = player1["job"]["years_on_pos"]

    document.getElementById("name_span_2").textContent = player2["name"]
    document.getElementById("symbol_span_2").textContent = player2["symbol"]
    document.getElementById("money_span_2").textContent = player2["money"]
    document.getElementById("happiness_span_2").textContent = player2["happiness"]
    document.getElementById("education_span_2").textContent = mapEducation[player2["education"]]
    document.getElementById("children_span_2").textContent = player2["children"]
    document.getElementById("relationship_span_2").textContent = mapRelationShip[player2["relationship"]]
    document.getElementById("investments_span_2").textContent = player2["investments"].join(', ')
    document.getElementById("job_span_2").textContent = jobToString(player2["job"]["job_name"])
    document.getElementById("job_years_span_2").textContent = player2["job"]["years_on_pos"]

    putSymbolOnPosition(player1, player2)
}

// add event listeners
window.addEventListener("load", (event) => {
    document.getElementById("button_1_roll").addEventListener("click", rollAndGetChoices)
    document.getElementById("button_2_roll").addEventListener("click", rollAndGetChoices)
});

// roll and give choices

function rollAndGetChoices() {
    console.log("HERE")
    $.ajax({
        type: "POST",
        url: "/roll_and_give_choices",
        contentType: "application/json",
        data: JSON.stringify({
            player_turn: playerOnTurn
        }),
        success: function (response) {
            showChoices(response["generated_choices"])
            showRolled(response["rolled"])
            getPlayers()
        }
    });
}

function showChoices(choices) {
    hideChoices()
    console.log(choices["type_choice"])
    if (choices["type_choice"] == type_choice_education) {
        document.getElementById("choices_education").style.display = "flex"
    }
    else if (choices["type_choice"] == type_choice_investments) {
        document.getElementById("choices_investment").style.display = "flex"
    }
    else if (choices["type_choice"] == type_choice_items) {
        document.getElementById("choices_item").style.display = "flex"
    }
    else if (choices["type_choice"] == type_choice_jobs) {
        document.getElementById("choices_job").style.display = "flex"
    }
    else if (choices["type_choice"] == type_choice_people) {
        document.getElementById("choices_people").style.display = "flex"
    }
    else if (choices["type_choice"] == type_choice_misfortune) {
        document.getElementById("choices_misfortune").style.display = "flex"
    }
    else if (choices["type_choice"] == type_choice_special_event) {
        document.getElementById("choices_special_event").style.display = "flex"
    }
}

function hideChoices() {
    document.getElementById("choices_education").style.display = "none"
    document.getElementById("choices_investment").style.display = "none"
    document.getElementById("choices_item").style.display = "none"
    document.getElementById("choices_job").style.display = "none"
    document.getElementById("choices_people").style.display = "none"
    document.getElementById("choices_misfortune").style.display = "none"
    document.getElementById("choices_special_event").style.display = "none"
}
function showRolled(roll) {
    if (playerOnTurn == 1) {
        document.getElementById("result_roll_1").value = roll
    } else {
        document.getElementById("result_roll_2").value = roll
    }
}


function getPlayers() {
    $.ajax({
        type: "GET",
        url: "/get_players",
        success: function (response) {
            populatePlayers(response)
        }
    });
}

function putSymbolOnPosition(player1, player2) {
    console.log(player1["position"])
    if (player1["position"] == "0" && player2["position"] == "0") {
        return
    }

    cleanTable()
    let table = document.getElementById("board_table")

    if (player1["position"] != "0") {
        let pos1 = parseInt(player1["position"])
        let row1 =  Math.floor(pos1 / width_table)
        let col1 = -1
        if (row1 % 2 == 0) {
            col1 = pos1 - row1 * width_table - 1
        } else {
            col1 = width_table - (pos1 - row1 * width_table)
        } 
        console.log(row1)
        table.rows[row1].cells[col1].innerHTML = ""
        table.rows[row1].cells[col1].innerHTML = table.rows[row1].cells[col1].innerHTML + player1["symbol"]
    }
    if (player2["position"] != "0") {
        let pos2 = parseInt(player2["position"])
        let row2 =  Math.floor(pos2 / width_table)
        let col2 = -1
        if (row2 % 2 == 0) {
            col2 = pos2 - row2 * width_table - 1
        } else {
            col2 = width_table - (pos2 - row2 * width_table)
        }
        table.rows[row2].cells[col2].innerHTML = ""
        table.rows[row2].cells[col2].innerHTML = table.rows[row2].cells[col2].innerHTML + player2["symbol"]
    }

}

function cleanTable() {
    let table = document.getElementById("board_table")
    let rows = table.children
    for (let index = 0; index < rows.length; index++) {
        let row = rows[index];
        if (index % 2) {
            for (let j = 0; j < row.length; j++) {
                console.log(index * width_table + j + 1)
                let cell = row[j];
                cell.innerHTML = String(index * width_table + j + 1)
            }
        }
        else {
            for (let j = row.length - 1; j >= 0; j--) {
                let cell = row[j];
                cell.innerHTML = String(index * width_table + width_table - j)
            }
        }

    }
}