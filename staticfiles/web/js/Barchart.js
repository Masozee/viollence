var dom = document.getElementById('container');
var myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: false
});

// Fetch data from API endpoint
fetch(apiBaseUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    return response.json();
  })
  .then(data => {
    console.log('Data:', data); // Log fetched data for debugging

    var options = {
      tooltip: {
        trigger: 'axis',
        formatter: function(params) {
          var result = params[0].name;
          params.forEach(function (item) {
            result += '<br/>' + item.marker + item.seriesName + ': ' + item.value + ' ' + data.satuan_value;
          });
          return result;
        }
      },
      legend: {
        left: '65px',
        top: '70px',
        textStyle: {
          color: '#333' // Legend text color
        },
        data: data.variable_set.map(variable => ({ name: variable.variable }))
      },
      xAxis: {
        type: 'category',
        axisTick: { alignWithLabel: true },
        axisLine: { lineStyle: { color: '#5470C6' } }, // example color
        data: data.variable_set[0].valuedata_set.map(entry => entry.formatted_date)
      },
      yAxis: {
        type: 'value'
      },
      dataZoom: [
        { type: 'slider', start: 0, end: 100 },
        { type: 'inside', start: 0, end: 100 }
      ],
      series: data.variable_set.map(variable => ({
        name: variable.variable,
        type: 'bar',
        data: variable.valuedata_set.map(entry => entry.value),
        itemStyle: {
          color: variable.id === data.variable_set[0].id ? '#4d8787' : '#4d8787' // Adjust as needed
        }
      }))
    };

    // Add options to the chart
    myChart.setOption(options);

    // Add title with hyperlink to the source
    var title = data.source;
    var url = data.url;
    var sourceText = 'Source: ' + title;
    var sourceHTML = '<a href="' + url + '" target="_blank">' + sourceText + '</a>';
    var sourceDiv = document.createElement('div');
    sourceDiv.style.position = 'absolute';
    sourceDiv.style.left = '85px';
    sourceDiv.style.top = '90px';
    sourceDiv.style.color = '#333'; // Text color
    sourceDiv.innerHTML = sourceHTML;
    dom.parentNode.appendChild(sourceDiv); // Append to the parent node of the chart
  })
  .catch(error => {
    console.error('Error:', error); // Log any errors for debugging
  });

window.addEventListener('resize', myChart.resize);
