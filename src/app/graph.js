document.addEventListener('DOMContentLoaded', function () {
    var myChart = Highcharts.chart('container', {
        title: {
            text: 'test'
        },

        xAxis: {
            type: 'datetime',
            title: 'Time'
        },
    
        plotOptions: {
            series: {
                pointStart: Date.UTC(2020, 7, 20),
                pointInterval: 24 * 3600 * 1000 // one day
            }
        },
    
        series: [{
            name: 'Sensor A',
            data: [70, 71, 73]
        }, {
            name: 'Sensor B',
            data: [71, 74, 80]
        }]
    });
});
