let chart = null

function createChart(values,score) {
  if (chart) {
    chart.data.datasets[0].data = values;
    chart.data.datasets[0].borderColor = colorForScore(score)
    chart.data.datasets[0].pointBackgroundColor = colorForScore(score)
    chart.update();
    return;
  }
  
  let ctx = document.getElementById('riskChart').getContext('2d');
  let g = ctx.createLinearGradient(0,0,0,420);
  g.addColorStop(0, 'rgba(34,197,94,0.18)');
  g.addColorStop(1, 'rgba(34,197,94,0.06)');
  
  chart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: metrics.map(m=>m.label),
      datasets: [{
        label: 'Safety Health Score',
        data: values,
        fill: true,
        backgroundColor: g,
        borderColor: colorForScore(score),
        borderWidth: 2,
        pointBackgroundColor: colorForScore(score),
        pointBorderColor: '#0b1220',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      elements: { line: { tension: 0.35 } },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(6,10,23,0.95)',
          titleFont: { size: 13, weight: '600' },
          bodyFont: { size: 13 },
          padding: 10,
          cornerRadius: 6,
          callbacks: {
            label: (ctx)=> `${ctx.label}: ${ctx.parsed.r}/100`
          }
        }
      },
      scales: {
        r: {
          min: 0,
          max: 100,
          beginAtZero: true,
          ticks: { 
            stepSize: 20, 
            color: 'rgba(203,213,225,0.92)', 
            font: { size: 11 }, 
            backdropColor: 'transparent',
            callback: function(value, _, _) {
              return value + "%";
            },
          },
          grid: { color: 'rgba(255,255,255,0.12)' },
          angleLines: { color: 'rgba(255,255,255,0.3)' },
          pointLabels: { color: 'rgba(226,232,240,0.95)', font: { size: 12 } }
        }
      }
    }
  });
}

