var dom = document.getElementById('container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});

fetch(apiBaseUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        return response.json();
    })
    .then(data => {
        var timelineData = [];
        var options = [];

        // Assume data is structured for multiple years
        var years = [...new Set(data.variable_set.flatMap(variable => variable.valuedata_set.map(item => item.formatted_date)))];
        years.sort();

        years.forEach(year => {
            var pieData = data.variable_set.map(variable => {
                var sum = variable.valuedata_set
                    .filter(item => item.formatted_date === year)
                    .reduce((acc, item) => acc + item.value, 0);
                return { name: variable.variable, value: sum };
            });

            timelineData.push(year.toString());
            options.push({
                title: {
                    text: 'Data for ' + year,
                    subtext: data.title,
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} (' + data.satuan_value + ') ({d}%)'
                },
                series: [{
                    name: 'Sales',
                    type: 'pie',
                    radius: '55%',
                    data: pieData,
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }]
            });
        });

        myChart.setOption({
            baseOption: {
                timeline: {
                    axisType: 'category',
                    autoPlay: true,
                    data: timelineData,
                    label: {
                        formatter: function (s) {
                            return (new Date(s)).getFullYear();
                        }
                    }
                },
                legend: {
                    left: 'right',
                    data: data.variable_set.map(variable => variable.variable)
                },
            },
            options: options
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to load data. Check console for details.');
    });

window.addEventListener('resize', () => myChart.resize());