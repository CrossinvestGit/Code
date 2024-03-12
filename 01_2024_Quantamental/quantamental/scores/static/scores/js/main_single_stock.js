// Handles all the events and interactions for the visualization
let barChart
let lineChart
let horTable
let sankeyChart

// Sankey Chart
d3.json(sankeyData).then(data => { // Fetches data from the specified JSON file
    console.log(data)

    sankeyChart = new SankeyChart(_parentElement = "#sankey-chart-area", _data = data, _dimension = { width: 928, height: 450 });

})



const updateSingleStockView = () => {

    // Description
    axios.get(output1, {
        params: {
            ticker: $('.form-select').val() // Additional data like ticker
        }
    }).then(response => {
        const data = response.data;
        horTable = new HorizontalTable(_tableid = "miau1", _data = data);
    }).catch(error => {
        console.error('Error fetching data:', error);
    });



    // Qualitative Table
    axios.get(output2, {
        params: {
            ticker: $('.form-select').val() // Additional data like ticker
        }
    }).then(response => {
        const data = response.data;
        horTable = new HorizontalTable(_tableid = "miau2", _data = data);
    }).catch(error => {
        console.error('Error fetching data:', error);
    });





    d3.json(sankeyTest).then(data => { // Fetches data from the specified JSON file
        console.log(data)

        sankeyChart.manageData(data)

    })



}

// Event listeners
$('.form-select').on("change", updateSingleStockView)


// const selectedStock = $('.form-select').val();








// d3.csv(csvUrl).then(data => {

//     cleanData = data
//     for (const d of cleanData) {
//         d.revenue = Number(d.revenue)
//         d.profit = Number(d.profit)
//     }

//     filteredDataB = cleanData
//     barChart = new BarChart("#barchart-area");
// })