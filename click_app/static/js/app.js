// Function to get api and display data on load
function showClicks() {
    const url = '/api/clickdata';
    d3.json(url).then(function(response) {
        // Select the click displays
        d3.select('#user_click_num').text(response[0]['user_clicks']);
        d3.select('#total_click_num').text(response[0]['total_clicks']);
    });
}

d3.select(window).on('load', showClicks());

// Function to get updated api and display data on click
function handleSubmit(event) {
    event.preventDefault();
    const url = '/api/clickdata';
    d3.json(url, {method:"POST"}).then(function(response) {
        // Select the click displays
        d3.select('#user_click_num').text(response[0]['user_clicks']);
        d3.select('#total_click_num').text(response[0]['total_clicks']);
    });
}