htmx.on("htmx:afterSwap", (evt) => {
  const div = document.getElementById("data-container");
  const data = JSON.parse(div.dataset.values);
  const values = metrics.map(m => clamp(data[m.key]));
  const score = data.score
  createBreakdown(values,score);
  createChart(values,score);
});
