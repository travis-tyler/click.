function showClicks() {

    /* data route */
    const url = "/api/clickdata";
    d3.json(url).then(function(response) {

        console.log(response);

        // Select the click displays
        d3.select(".user_click_num").data(response[0]);
        d3.select(".total_click_num").data(response[1]);

    });
}

showClicks();