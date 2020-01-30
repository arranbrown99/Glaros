/* Timeline code */
google.charts.load('current', {'packages': ['timeline']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var container = document.getElementById('timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({type: 'string', id: 'President'});
    dataTable.addColumn({type: 'date', id: 'Start'});
    dataTable.addColumn({type: 'date', id: 'End'});
    dataTable.addRows([
        ['AWS', new Date(2015, 10, 1), new Date(2015, 10, 3)],
        ['Azure', new Date(2015, 10, 3), new Date(2015, 10, 5)],
        ['GCP', new Date(2015, 10, 5), new Date(2015, 10, 7)],
        ['AWS', new Date(2015, 10, 7), new Date(2015, 10, 14)],
        ['GCP', new Date(2015, 10, 14), new Date(2015, 10, 16)],
        ['Azure', new Date(2015, 10, 16), new Date(2015, 10, 20)],
        ['AWS', new Date(2015, 10, 20), new Date(2015, 10, 25)],
        ['GCP', new Date(2015, 10, 25), new Date(2015, 10, 29)],
        ['Azure', new Date(2015, 10, 29), new Date(2015, 10, 30)],
        ['AWS', new Date(2015, 10, 30), new Date(2015, 11, 6)],
    ]);

    var options = {
        colors: ['#FF6384', '#36A2EB', '#FFCD56'],
    };
    chart.draw(dataTable, options);
}

/* Stock Prices (Line Plot) code */
const ctx = document.getElementById("stockPricesChart").getContext('2d');
;
console.log(ctx);
var stock_prices_chart = null;
var data_points = '10';
var time_interval = '1d';

function update_chart() {
    let button = event.srcElement;
    let name = button.getAttribute("name");

    switch (name) {
        case 'datapoints':
            data_points = button.getAttribute("data-points");
            break;
        case 'intervals':
            time_interval = button.getAttribute("data-interval");
            break;
    }

    update_stock_prices(data_points, time_interval);
}

function update_stock_prices(points, interval) {
    console.log(points, interval);
    $.ajax({
        url: $("#update-stock-prices").attr("data-ajaxurl"), // the url is provided by the button's attributes
        method: 'GET',
        dataType: 'json',
        data: {
            'points': points,
            'interval': interval
        },
        success: function (data) {
            console.log(data.labels);
            console.log(data.labels.map(x => new Date(Date.UTC(x.y, x.m - 1, x.d))));

            // clear the canvas
            if (stock_prices_chart) {
                stock_prices_chart.destroy(); // destroy rather than clear so the hovers don't stay alive
            }

            stock_prices_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    // dates come as json objects. javascript months are zero-indexed
                    labels: data.labels.map(x => new Date(Date.UTC(x.y, x.m - 1, x.d))),
                    datasets: data.datasets,
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {
                                displayFormats: {
                                    millisecond: 'MMM DD',
                                    second: 'MMM DD',
                                    minute: 'MMM DD',
                                    hour: 'MMM DD',
                                    day: 'MMM DD',
                                    week: 'MMM YYYY',
                                    month: 'MMM YYYY',
                                    quarter: 'MMM YYYY',
                                    year: 'MMM YYYY',
                                }
                            },
                            ticks: {
                                source: 'labels',
                            },
                        }],
                    },
                }
            });
        }
    });
}

// let stock_prices_chart = new Chart(ctx, {
//     type: 'line',
//     data: {
//         labels: [new Date().toLocaleDateString(), 'February', 'March', 'April', 'May', 'June', 'July'],
//         datasets:
//             [{
//                 label: 'AWS',
//                 backgroundColor: 'rgb(255, 99, 132)',
//                 borderColor: 'rgb(255, 99, 132)',
//                 data: [73, -6, -99, 79, 93, -32, -99],
//                 fill: false,
//             }, {
//                 label: 'AZURE',
//                 fill: false,
//                 backgroundColor: 'rgb(54, 162, 235)',
//                 borderColor: 'rgb(54, 162, 235)',
//                 data: [-98, -26, 23, -95, 1, -72, -14],
//             }]
//     },
//     // options: options
// });


$(document).ready(function () {
    console.log("ready");
    /*
    Update the Stock Prices Chart for the first time
     */
    update_stock_prices(data_points, time_interval);

    /* Some code to ensure that the height of the stock prices chart
       matches the card on the left ("general information")*/
    setHeight($('#right-card'), $('#left-card'));

    // When the window is resized the height might
    // change depending on content. So to be safe
    // we rerun the function
    $(window).on('resize', function () {
        setHeight($('#right-card'), $('#left-card'));
    });

});

// sets height of element 1 to equal the height of element 2
function setHeight(elem1, elem2) {
    var height = elem2.height();
    elem1.css('height', height);
}