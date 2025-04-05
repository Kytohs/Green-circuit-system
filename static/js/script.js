async function fetchHistory(period) {
    const response = await fetch(`/get_bin_history?period=${period}`);
    const data = await response.json();

    const labels = data.map(entry => entry.timestamp);
    const weights = data.map(entry => entry.weight);

    binChart.data.labels = labels;
    binChart.data.datasets[0].data = weights;
    binChart.update();
}

document.getElementById("daily").addEventListener("click", () => fetchHistory("daily"));
document.getElementById("weekly").addEventListener("click", () => fetchHistory("weekly"));
document.getElementById("monthly").addEventListener("click", () => fetchHistory("monthly"));
