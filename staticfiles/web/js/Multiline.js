var dom = document.getElementById('container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var app = {};

var option;

// Function to fetch data from the API endpoint
function fetchDataAndUpdateChart() {
    fetch(apiBaseUrl)
        .then(response => response.json())
        .then(data => {
            var variables = data.variable_set;

            // Filter out "Jumlah" variable
            var filteredVariables = variables.filter(variable => variable.variable !== "Jumlah");

            // Extracting data for each variable
            var seriesData = filteredVariables.map(variable => ({
                name: variable.variable,
                type: 'line',
                stack: 'Total',
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: variable.valuedata_set.map(entry => entry.value)
            }));

            // Update the option object with the fetched data and legend
            option.series = seriesData;
            option.xAxis[0].data = filteredVariables[0].valuedata_set.map(entry => entry.formatted_date);
            option.legend.data = filteredVariables.map(variable => variable.variable);

            // Add a data filter inside the chart
            option.dataZoom = [
                {
                    type: 'slider',
                    start: 0,
                    end: 100
                }
            ];

            // Add source with link from url
            option.graphic = [{
                type: 'text',
                left: 90,
                top: 15,
                z: 100,
                style: {
                    text: 'Source: ' + data.source,
                    fontSize: 12,
                    fill: '#666',

                }
            }];

            // Add Satuan from satuan_value with 30px font size on top left corner
            option.graphic.push({
                type: 'text',
                left: 90,
                top: 0,
                z: 100,
                style: {
                    text: 'Satuan: ' + data.satuan_value,
                    fontSize: 12,
                    fill: '#666',

                }
            });

            // Update chart with the modified option
            myChart.setOption(option);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
    },
    legend: {
        left: 'center',
        bottom: 60,
        data: []
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            boundaryGap: false,
            data: []
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: []
};

// Call the function to fetch data and update the chart
fetchDataAndUpdateChart();

// Resize chart on window resize
window.addEventListener('resize', myChart.resize);
