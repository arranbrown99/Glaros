/* GLOBALS */
const ctx = document.getElementById("stockPricesChart").getContext('2d');
var stock_prices_chart = null;
var data_points = '10';
var time_interval = '1d';
var chart;

/* When the Document is ready (finished rendering) do the following */
$(document).ready(function () {

    /* Update the Stock Prices Chart for the first time */
    update_stock_prices(data_points, time_interval);

    /* Update the Migration Timeline chart (happens only once) */
    google.charts.load('current', {'packages': ['timeline']});
    google.charts.setOnLoadCallback(drawChart);

    /* Some code to ensure that the height of the stock prices chart
       matches the card on the left ("general information")*/
    setHeight($('#right-card'), $('#left-card'));

    // When the window is resized the height might
    // change depending on content. So to be safe
    // we rerun the function
    $(window).on('resize', function () {
        // set the height of the right container (Stock Prices)
        // equal to left container (General Information).
        setHeight($('#right-card'), $('#left-card'));
    });

    create_migrations_table();

});

/**
 * Takes a (date) object in the format: {"d": day, "m": month, "y": year}
 * and returns a Javascript Date object.
 * @param date
 * @returns {Date}
 */
function json_to_date(date) {
    return new Date(Date.UTC(date.y, date.m - 1, date.d, date.h, date.min, date.s))
}

function generate_timeline_tooltip(csp, from, until, duration) {
    let html = "<div class=\"card\" style=\"height: 150px;width: 300px;\">\n" +
        "  <div class=\"card-body\">\n" +
        "    <h5 class=\"card-title\" style=\"color: darkslategray;\">" + csp + "</h5>\n" +
        "    <hr>\n" +
        "    <p class=\"card-text\">" + from + " - " + until + "</p>\n" +
        "    <p class=\"card-text\" style=\"\"><strong>Duration:</strong> " + duration + "</p>\n" +
        "  </div>\n" +
        "</div>";
    return html
}

/**
 * Function that presents the migrations timeline chart
 */
function drawChart() {
    var container = document.getElementById('timeline');
    chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    // AJAX request for timeline data
    $.ajax({
        url: $("#timeline").attr("data-update-url"), // the url is provided by the button's attributes
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            dataTable.addColumn({type: 'string', id: 'csp_name'});
            dataTable.addColumn({type: 'string', id: 'dummy bar label'});
            dataTable.addColumn({type: 'string', role: 'tooltip', p: {html: true}});
            dataTable.addColumn({type: 'date', id: 'Start'});
            dataTable.addColumn({type: 'date', id: 'End'});

            var data_options = {weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric'};

            data.migrations.forEach(entry => dataTable.addRows([
                [
                    entry[0],
                    "",
                    generate_timeline_tooltip(
                        csp = entry[0],
                        from = json_to_date(entry[1]).toLocaleDateString('en-GB', data_options),
                        until = json_to_date(entry[2]).toLocaleDateString('en-GB', data_options),
                        duration = entry[3]),
                    json_to_date(entry[1]),
                    json_to_date(entry[2]),
                ]]
            ));

            var chart_options = {
                hAxis: {
                    format: 'dd-MMM',
                    // gridlines: {count: 15}
                },
                tooltip: {isHtml: true},
                colors: data.colors_list,
                timeline: {
                    colorByRowLabel: true,
                }
            };
            chart.draw(dataTable, chart_options);
            $(window).on('resize', function () {
                chart.draw(dataTable, chart_options);
            });
        }
    });
}

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
    $.ajax({
        url: $("#update-stock-prices").attr("data-ajaxurl"), // the url is provided by the button's attributes
        method: 'GET',
        dataType: 'json',
        data: {
            'points': points,
            'interval': interval
        },
        success: function (data) {

            // clear the canvas
            if (stock_prices_chart) {
                stock_prices_chart.destroy(); // destroy rather than clear so the hovers don't stay alive
            }

            stock_prices_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    // dates come as json objects. javascript months are zero-indexed
                    labels: data.labels.map(x => json_to_date(x)),
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
                                    week: 'MMM DD',
                                    month: 'MMM DD',
                                    quarter: 'MMM DD',
                                    year: 'MMM DD',
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

// sets height of element 1 to equal the height of element 2
function setHeight(elem1, elem2) {
    var height = elem2.height();
    elem1.css('height', height);
}

function create_migrations_table() {

    //create Tabulator on DOM element with id "migrations-table"
    var table = new Tabulator("#migrations-table", {
        ajaxURL: document.getElementById("migrations-table").getAttribute("data-ajaxurl"), //ajax URL
        ajaxProgressiveLoad: "scroll", //enable progressive loading
        ajaxProgressiveLoadScrollMargin: 100, // triger next ajax load when scroll bar is 300px or less from the bottom of the table.
        paginationSize: 10, // how many records per page
        height: 500, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
        layout: "fitColumns", //fit columns to width of table (optional)
        columns: [ //Define Table Columns
            {title: "ID", field: "id", align: "center", width: 100},
            {title: "Date of Migration", field: "date", align: "center", width: 260},
            {title: "From Where", field: "from", align: "center", width: 200},
            {title: "To Where", field: "to", align: "center", width: 200},
        ],
    });
}
