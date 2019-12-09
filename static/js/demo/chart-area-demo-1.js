// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var countyData = JSON.parse(JSON.parse(document.getElementById('county-data').textContent));
debugger;
// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: countyData.map((item, index) => index),
    datasets: [{
      label: "Sessions",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: countyData.map(item => item.fields.answer_percentage*100),
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        },
        scaleLabel: {
          display: true,
          labelString: 'شماره آزمون سوال',
        },
      }],
      yAxes: [{
        ticks: {
          min: 0,
          // max: countyData.reduce((max, item) => max < item.fields.answer_percentage ? item.fields.answer_percentage : max, 0),
          max: 100,
          maxTicksLimit: 5
        },
        scaleLabel: {
          display: true,
          labelString: 'درصد پاسخگویی',
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
