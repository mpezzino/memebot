/**
 * Created by jonathan on 1/2/15.
 */

$(document).ready(function() {
    $("#b").click( function() {

        $.getJSON("http://reddit_oracle_api.breauxgramm.in:8080/?callback=?",
            {
                t: $("#t_input").val()
            },
            function (data) {
                    $("#result-container").prepend($("<div><table><tr><td>Comment:</td><td>" + $("#t_input").val()
                    + "</td></tr><tr><td>Predicted Karma:</td><td>" + data +"</td></tr></table></div>"));
                }

        );
    })
})