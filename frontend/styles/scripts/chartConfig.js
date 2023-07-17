function addData(chart, label, data) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
  });
  chart.update();
}

function removeFirstData(chart) {
  chart.data.labels.splice(0, 1);
  chart.data.datasets.forEach((dataset) => {
    dataset.data.shift();
  });
}

var chartTemperature;
  var chartUmidade;

  $(document).ready(function() {
    const ctx1 = document.getElementById('chart1');
    const ctx2 = document.getElementById('chart2');

    chartTemperature = new Chart(ctx1, {
      type: "line",
     
      data: {
       
        datasets: [{
          label: "Temperatura",
          backgroundColor: ["rgba(85, 34, 0, 1)",],
          borderColor: ["rgba(85, 34, 0, 1)",],       
          borderWidth: 1,    
        }],
      },
      options: {      
        
        scales: {
          x: {
            display: false,
            ticks: {
              color: ["rgba(85, 34, 0, 1)",],  
            }
          },
          y: {
            ticks: {                  
              color: ["rgba(85, 34, 0, 1)",],  
            }
          }
        },       

        plugins: {

          title: {
            display: true,
            text: "Temperatura (°C)",
            color: "#552200",
            font: {
              size: "17px",
              weight: ["700"],
            },           
          },

          legend: {display: false},         
        },
      },      
    });

    chartUmidade = new Chart(ctx2, {
      type: "line",     
      data: {       
        datasets: [{
          label: "Umidade",
          backgroundColor: ["rgba(85, 34, 0, 1)",],
          borderColor: ["rgba(85, 34, 0, 1)",],       
          borderWidth: 1,    
        }],
      },
      options: {           
        scales: {
          x: {
            display: false,
            ticks: {
              color: ["rgba(85, 34, 0, 1)",],  
            }
          },
          y: {
            ticks: {             
              color: ["rgba(85, 34, 0, 1)",],  
            }
          }
        },       

        plugins: {
         
          title: {
            display: true,
            text: "Umidade (%)",
            color: "#552200",
            font: {
              size: "17px",
              weight: ["700"],
            },           
          },

          legend: {display: false},       
        },
      },      
    })
  });
 