const type_choice_education = "education"
const type_choice_investments = "investments"
const type_choice_items = "items"
const type_choice_jobs = "jobs"
const type_choice_people = "people"
const type_choice_misfortune = "misfortune"
const type_choice_special_event = "special_event"
const type_choice_finished = "finished"

const width_table = 7

const mapEducation = {
    1: "Университет",
    2: "Курсове",
    3: "Без"
}

const mapRelationShip = {
    1: "Сам / Сама",
    2: "Във връзка",
    3: "Женен / Омъжена",
}

const mapInvestment = {
    1: "Акции",
    2: "Недвижима собственост",
    3: "Земя",
}

const mapSideEffect = {
    1: "Загуба на акции",
    2: "Загуба на недвижими имоти",
    3: "Загуба на земя",
    4: "Няма",
}

var playerOnTurn = 1
var currentChoices = null

function jobToString(job) {
    if (job == null) {
        return "Без"
    }
    job = JSON.parse(job)
    return String.fromCharCode(job["name"])
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
    document.getElementById("name_span_1").textContent = player1["name"]
    document.getElementById("symbol_span_1").textContent = player1["symbol"]
    document.getElementById("money_span_1").textContent = player1["money"]
    document.getElementById("happiness_span_1").textContent = player1["happiness"]
    console.log("EDUCATION: ", player1["education"])
    document.getElementById("education_span_1").textContent = mapEducation[player1["education"]]
    document.getElementById("children_span_1").textContent = player1["children"]
    document.getElementById("relationship_span_1").textContent = mapRelationShip[player1["relationship"]]
    document.getElementById("investments_span_1").textContent = player1["investments"].join(', ')
    document.getElementById("job_span_1").textContent = jobToString(player1["job"])
    document.getElementById("job_years_span_1").textContent =player1["job_years"]

    document.getElementById("name_span_2").textContent = player2["name"]
    document.getElementById("symbol_span_2").textContent = player2["symbol"]
    document.getElementById("money_span_2").textContent = player2["money"]
    document.getElementById("happiness_span_2").textContent = player2["happiness"]
    document.getElementById("education_span_2").textContent = mapEducation[player2["education"]]
    document.getElementById("children_span_2").textContent = player2["children"]
    document.getElementById("relationship_span_2").textContent = mapRelationShip[player2["relationship"]]
    document.getElementById("investments_span_2").textContent = player2["investments"].join(', ')
    document.getElementById("job_span_2").textContent = jobToString(player2["job"])
    document.getElementById("job_years_span_2").textContent = player2["job_years"]

    putSymbolOnPosition(player1, player2)
}

// add event listeners
window.addEventListener("load", (event) => {
    document.getElementById("button_1_roll").addEventListener("click", rollAndGetChoices)
    document.getElementById("button_2_roll").addEventListener("click", rollAndGetChoices)

    document.getElementById("button_choices_education_none").addEventListener("click", () => {sendChoice(0)})
    document.getElementById("button_choices_education_courses").addEventListener("click", () => {sendChoice(1)})
    document.getElementById("button_choices_education_university").addEventListener("click", () => {sendChoice(2)})
    document.getElementById("button_choices_investment_1").addEventListener("click", () => {sendChoice(0)})
    document.getElementById("button_choices_investment_2").addEventListener("click", () => {sendChoice(1)})
    document.getElementById("button_choices_investment_3").addEventListener("click", () => {sendChoice(2)})
    document.getElementById("button_choices_item_1").addEventListener("click", () => {sendChoice(0)})
    document.getElementById("button_choices_item_2").addEventListener("click", () => {sendChoice(1)})
    document.getElementById("button_choices_item_3").addEventListener("click", () => {sendChoice(2)})
    document.getElementById("button_choices_job_1").addEventListener("click", () => {sendChoice(0)})
    document.getElementById("button_choices_job_2").addEventListener("click", () => {sendChoice(1)})
    document.getElementById("button_choices_job_3").addEventListener("click", () => {sendChoice(2)})
    document.getElementById("button_choices_people_1").addEventListener("click", () => {sendChoice(0)})
    document.getElementById("button_choices_people_2").addEventListener("click", () => {sendChoice(1)})
    document.getElementById("button_choices_people_3").addEventListener("click", () => {sendChoice(2)})

    document.getElementById("button_misfortune").addEventListener("click", () => {sendChoice(0)})
    document.getElementById("button_special_event").addEventListener("click", () => {sendChoice(0)})

});

// roll and give choices

function rollAndGetChoices() {
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
    let typeChoice = choices["type_choice"]
    let choicesOfType = choices["choices"]
    if (typeChoice == type_choice_education) {
        document.getElementById("choices_education").style.display = "flex"
    }
    else if (typeChoice == type_choice_investments) {
        document.getElementById("choices_investment").style.display = "flex"
        populateInvestments(choicesOfType)
    }
    else if (typeChoice == type_choice_items) {
        document.getElementById("choices_item").style.display = "flex"
        populateItems(choicesOfType)
    }
    else if (typeChoice == type_choice_jobs) {
        document.getElementById("choices_job").style.display = "flex"
        populateJobs(choicesOfType)
    }
    else if (typeChoice == type_choice_people) {
        document.getElementById("choices_people").style.display = "flex"
        populatePeople(choicesOfType)
    }
    else if (typeChoice == type_choice_misfortune) {
        document.getElementById("choices_misfortune").style.display = "flex"
        populateMisfortune(choicesOfType)
    }
    else if (typeChoice == type_choice_special_event) {
        document.getElementById("choices_special_event").style.display = "flex"
        populateSpecialEvents(choicesOfType)
    } else if (typeChoice == type_choice_finished) {
        if (playerOnTurn == 1) {
            document.getElementById("button_1_roll").disabled = true
        } else {
            document.getElementById("button_2_roll").disabled = false
        }
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

function populateJobs(choices) {
    let choice1 = choices[0]
    let choice2 = choices[1]
    let choice3 = choices[2]

    document.getElementById("job_name_1").innerHTML = choice1["name"]
    document.getElementById("job_money_1").innerHTML = choice1["base_salary"]

    document.getElementById("job_name_2").innerHTML = choice2["name"]
    document.getElementById("job_money_2").innerHTML = choice2["base_salary"]

    document.getElementById("job_name_3").innerHTML = choice3["name"]
    document.getElementById("job_money_3").innerHTML = choice3["base_salary"]
}

function populateInvestments(choices) {
    let choice1 = choices[0]
    let choice2 = choices[1]
    let choice3 = choices[2]

    document.getElementById("investment_name_1").innerHTML = choice1["name"]
    document.getElementById("investment_description_1").innerHTML = choice1["description"]
    document.getElementById("investment_price_1").innerHTML = choice1["base_price"]
    document.getElementById("investment_type_1").innerHTML = mapInvestment[choice1["type_investment"]]

    document.getElementById("investment_name_2").innerHTML = choice2["name"]
    document.getElementById("investment_description_2").innerHTML = choice2["description"]
    document.getElementById("investment_price_2").innerHTML = choice2["base_price"]
    document.getElementById("investment_type_2").innerHTML = mapInvestment[choice2["type_investment"]]

    document.getElementById("investment_name_3").innerHTML = choice3["name"]
    document.getElementById("investment_description_3").innerHTML = choice3["description"]
    document.getElementById("investment_price_3").innerHTML = choice3["base_price"]
    document.getElementById("investment_type_3").innerHTML = mapInvestment[choice3["type_investment"]]
}

function populateItems(choices) {
    let choice1 = choices[0]
    let choice2 = choices[1]
    let choice3 = choices[2]

    document.getElementById("item_name_1").innerHTML = choice1["name"]
    document.getElementById("item_description_1").innerHTML = choice1["description"]
    document.getElementById("item_happiness_1").innerHTML = "+" + choice1["happiness"]
    document.getElementById("item_price_1").innerHTML = "-" + choice1["money"]
    document.getElementById("item_image_1").src = choice1["image"]

    document.getElementById("item_name_2").innerHTML = choice2["name"]
    document.getElementById("item_description_2").innerHTML = choice2["description"]
    document.getElementById("item_happiness_2").innerHTML = "+" + choice2["happiness"]
    document.getElementById("item_price_2").innerHTML = "-" + choice2["money"]
    document.getElementById("item_image_2").src = choice2["image"]

    document.getElementById("item_name_3").innerHTML = choice3["name"]
    document.getElementById("item_description_3").innerHTML = choice3["description"]
    document.getElementById("item_happiness_3").innerHTML = "+" + choice3["happiness"]
    document.getElementById("item_price_3").innerHTML = "-" + choice3["money"]
    document.getElementById("item_image_3").src = choice3["image"]
}

function populatePeople(choices) {
    let choice1 = choices[0]
    let choice2 = choices[1]
    let choice3 = choices[2]

    document.getElementById("people_name_1").innerHTML = choice1["name"]
    document.getElementById("people_description_1").innerHTML = choice1["description"]

    document.getElementById("people_name_2").innerHTML = choice2["name"]
    document.getElementById("people_description_2").innerHTML = choice2["description"]

    document.getElementById("people_name_3").innerHTML = choice3["name"]
    document.getElementById("people_description_3").innerHTML = choice3["description"]
}

function populateMisfortune(choices) {
    let choice = choices[0]

    document.getElementById("misfortune_name").innerHTML = choice["name"]
    document.getElementById("misfortune_description").innerHTML = choice["description"]
    document.getElementById("misfortune_happiness").innerHTML = choice["happiness"]
    document.getElementById("misfortune_money").innerHTML = choice["money"]
    document.getElementById("misfortune_side_effect").innerHTML = mapSideEffect[choice["side_effects"]]
}

function populateSpecialEvents(choices) {
    let choice = choices[0]

    document.getElementById("special_event_name").innerHTML = choice["name"]
    document.getElementById("special_event_description").innerHTML = choice["description"]
    document.getElementById("special_event_happiness").innerHTML = "+" + choice["happiness"]
    document.getElementById("special_event_money").innerHTML = "-" + choice["money"]
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
        let row1 = Math.floor((pos1 - 1) / width_table)
        let col1 = -1
        if (row1 % 2 == 0) {
            col1 = pos1 - row1 * width_table - 1
        } else {
            col1 = width_table - (pos1 - row1 * width_table)
        }
        console.log("Row, col: ", row1, col1)
        table.rows[row1].cells[col1].innerHTML = ""
        table.rows[row1].cells[col1].innerHTML = table.rows[row1].cells[col1].innerHTML + player1["symbol"]
    }
    if (player2["position"] != "0") {
        let pos2 = parseInt(player2["position"])
        let row2 = Math.floor((pos2 - 1) / width_table)
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
    for (let row = 0; row < width_table; row++) {
        for (let col = 0; col < width_table; col++) {
            if (row % 2) {
                table.rows[row].cells[col].innerHTML = String(row * width_table + width_table - col)
            } else {
                table.rows[row].cells[col].innerHTML = String(row * width_table + col + 1)
            }
        }
    }
}

function sendChoice(indexChoice) {
    $.ajax({
        type: "POST",
        url: "/process_choice",
        contentType: "application/json",
        data: JSON.stringify({
            player_turn: playerOnTurn,
            index_choice: indexChoice
        }),
        success: function (response) {
            console.log(response)
            getPlayers()
            hideChoices()
        }
    });
}