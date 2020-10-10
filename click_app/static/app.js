function showClicks() {

    /* data route */
    const url = "/api/clickdata";
    d3.json(url).then(function(response) {

        console.log(response);

        // Select the click displays
        d3.select(".user_click_num").text(response[0]['user_clicks']);
        d3.select(".total_click_num").text(response[0]['total_clicks']);

    });
}

// Add event listener for submit button
// d3.select("#clickButton").on("click", showClicks);

showClicks();















// let clickButton = d3.select('#clickButton');


// Event handler function
// function showClicks() {
//     /* data route */
//     const url = 'https://api.stoplight.io/v1/versions/9WaNJfGpnnQ76opqe/export/oas.json';
//     d3.json(url).then(function(response) {
//         console.log(url);
//         // Prevent the page from refreshing
//         d3.event.preventDefault();
//         console.log(response['info']);
//         d3.select("#user_click_num").text(response['info']);
//         d3.select("#total_click_num").text(response['info']);
//     });
// };

// function showClicks() {
//     let response = {"cars":50000,"houses":9000}

//     // Prevent the page from refreshing
//     // d3.event.preventDefault();
//     console.log(response['cars']);
//     d3.select("#user_click_num").text(response['cars']);
//     d3.select("#total_click_num").text(response['houses']);
// };

// async function showClicks() {  
//     let url = 'https://api.stoplight.io/v1/versions/9WaNJfGpnnQ76opqe/export/oas.json';

//     console.log(url);

//     let response = await d3.json(url);

//     console.log(url);


//     d3.select("#user_click_num").text(response['info']);
//     d3.select("#total_click_num").text(response['info']);

// };

// // Create event handler
// clickButton.on('click',showClicks);

// showClicks();