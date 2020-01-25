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
