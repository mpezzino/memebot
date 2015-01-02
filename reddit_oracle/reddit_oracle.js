/**
 * Created by jonathan on 1/2/15.
 */

$(document).ready(function() {
    $("#b").click( function() {

        $.getJSON("http://localhost:8080/?callback=?",
            {
                t: $("#t_input").val()
            },
            function (data) {
                    $("#result").text(data);
                }

        );
    })
})