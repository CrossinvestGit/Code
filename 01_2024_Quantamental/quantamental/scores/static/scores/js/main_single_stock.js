// Handles all the events and interactions for the visualization
let barChart
let lineChart
let horTable

const updateSingleStockView = () => {
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