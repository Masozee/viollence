var dom = document.getElementById('container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});

fetch(apiBaseUrl)
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        var years = [];
        var seriesOptions = [];
        var timelineData = [];

        // Handle scenarios where valuedata_set might be empty
        data.variable_set.forEach(variable => {
            variable.valuedata_set.forEach(function (item) {
                if (!years.includes(item.formatted_date)) {
                    years.push(item.formatted_date);
                }
            });
        });

        years.sort();

        years.forEach(function (year) {
            var yearData = data.variable_set.map(function (variable) {
                var totalValue = 0;
                variable.valuedata_set.forEach(function (valuedata) {
                    if (valuedata.formatted_date === year) {
                        totalValue += valuedata.value;
                    }
                });
                return {
                    name: variable.variable,
                    value: totalValue
                };
            });

            seriesOptions.push({
                title: {
                    text: data.title + ' - ' + year,
                    left: 'center',
                    top: 'top'
                },
                series: [{ type: 'treemap', data: yearData }]
            });

            timelineData.push({ value: year, tooltip: { formatter: '{b}' } });
        });

        myChart.setOption({
            baseOption: {
                timeline: {
                    axisType: 'category',
                    autoPlay: true,
                    playInterval: 1500,
                    bottom: 20,
                    data: timelineData
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function (params) {
                        return params.name + ': ' + params.value + ' ' + data.satuan_value;
                    }
                },
                series: [
                    {
                        name: data.title,
                        type: 'treemap',
                        visibleMin: 300,
                        roam: false,
                        breadcrumb: {
                            show: false
                        },
                        levels: [
                            {
                                itemStyle: {
                                    borderColor: '#555',
                                    borderWidth: 4,
                                    gapWidth: 4
                                }
                            },
                            {
                                colorSaturation: [0.3, 0.6],
                                itemStyle: {
                                    borderColorSaturation: 0.7,
                                    gapWidth: 2,
                                    borderWidth: 2
                                }
                            }
                        ]
                    }
                ]
            },
            options: seriesOptions
        });
    })
    .catch(function (error) {
        console.error('Error:', error);
        alert('Failed to load data. Check console for details.');
    });

window.addEventListener('resize', function () {
    myChart.resize();
});
