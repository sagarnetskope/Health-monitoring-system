$(function () {

    $('#container').highcharts({

        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false

        },

        exporting: { enabled: false },

        credits: {
        enabled: false
        },
        title: {
            text: 'Your BMI Level'
        },

        pane: {
            startAngle: -90,
            endAngle: 90,
            background: null
        },

        plotOptions: {
            gauge: {
                dataLabels: {
                    enabled: false
             },
                dial: {
                                        radius: '75%',
                    backgroundColor: 'black',
                    borderColor: 'black',
                    borderWidth: 1,
                    baseWidth: 7,
                    topWidth: 1,
                    baseLength: '70%', // of radius
                    rearLength: '10%'
                }
            }
        },

        // the value axis
        yAxis: {
            labels: {x:-12,y:10,

             style: {color:'white',fontSize: '15px'
                    , }



            },
            tickPositions: [18.5,25,30],
            minorTickLength: 2,
            min: 10,
            max: 50,
            plotBands: [{
                from: 0,
                to: 18.5,
                color: '#807dba', // red
                thickness: '50%'
            }, {
                from: 18.5,
                to: 24.9,
                color: '#41ab5d', // yellow
                thickness: '50%'
             }, {
                from: 24.9,
                to: 30,
                color: 'rgb(255,165,0)', // yellow
                thickness: '50%'
            }, {
                from: 30,
                to: 50,
                color: '#d04b4b', // green
                thickness: '50%'
            }]
        },

        series: [{
            name: 'Speed',
            data: [10]
        }]

    });
});