// Function to get api and display data on load
function showClicks() {
    const url = '/api/clickdata';
    d3.json(url).then(function(response) {
        // Select the click displays
        d3.select('#user_click_num').text(response[0]['user_clicks']);
        d3.select('#total_click_num').text(response[0]['total_clicks']);
        
        // Plotly code to generate chart from API
        // Trace for leaderboard data
        let trace = {
            x: response[0]['leaderboard']['users'],
            y: response[0]['leaderboard']['clicks'],
            type:"bar"
        };

        let data = [trace];

        let layout = {
            title: 'Top Clickers',
            height: 500,
            width: 800,
            xaxis: {
                title: 'Username'
            },
            yaxis: {
                title: 'Number of clicks'
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: 'white'
            }       
        };

        let config = {responsive: true}
    
        Plotly.newPlot("plot", data, layout, config);

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

        // Plotly code to generate chart from API
        // Trace for leaderboard data
        let trace = {
            x: response[0]['leaderboard']['users'],
            y: response[0]['leaderboard']['clicks'],
            type:"bar"
        };

        let data = [trace];

        let layout = {
            title: 'Top clickers',
            height: 500,
            width: 800,
            xaxis: {
                title: 'Username'
            },
            yaxis: {
                title: 'Number of clicks'
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: 'white'
            }       
        };

        let config = {responsive: true}
    
        Plotly.newPlot("plot", data, layout, config);

    });
}



