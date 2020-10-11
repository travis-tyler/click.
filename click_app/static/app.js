function showClicks() {
    /* data route */
    const url = "/api/clickdata";
    d3.json(url).then(function(response) {

        console.log(response[0]['user_clicks']);
        console.log(response[0]['total_clicks']);

        // Select the click displays
        d3.select("#user_click_num").text(response[0]['user_clicks']);
        d3.select("#total_click_num").text(response[0]['total_clicks']);

    });
}

// Add event listener for submit button
// d3.select("#clickButton").on("click", function(event) {
//     event.preventDefault();
//     showClicks();
// });

d3.select("#clickButton").on("click", showClicks());


showClicks();