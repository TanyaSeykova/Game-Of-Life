$(document).ready(function () {
  $("#play_button").on("click", function () {
    $.ajax({
      type: "POST",
      url: "/process_data",
      contentType: "application/json",
      data: JSON.stringify({
        players: [
          {
            player_name: document.getElementById("player_1_name").value,
            player_symbol: document.getElementById("player_1_symbol").options[document.getElementById("player_1_symbol").selectedIndex].text,
            player_preference: document.getElementById("player_1_preference").options[document.getElementById("player_1_preference").selectedIndex].text
          },
          {
            player_name: document.getElementById("player_2_name").value,
            player_symbol: document.getElementById("player_2_symbol").options[document.getElementById("player_2_symbol").selectedIndex].text,
            player_preference: document.getElementById("player_2_preference").options[document.getElementById("player_2_preference").selectedIndex].text
          }
        ]
      }),
      success: function (response) {
        console.log(response)
        if (response["error"]) {
          alert(response["error"])
          console.log(window.location.href)
        } else {
          window.location.href = "game_board"
        }
      }
    });
  });
});

function open_game_board() {
  $.ajax({
    type: "GET",
    url: "/redirect_game_board",
    success: function (response) {
      console.log(response);
    }
  });
}