// ✅ Ensure Chart.js is loaded
if (typeof Chart !== "undefined") {
    console.log("✅ Chart.js is loaded.");
} else {
    console.error("❌ Chart.js failed to load!");
}

// ✅ Declare global variables
var binChart = null;
var separateChart = null;
var map = null;
var socket = io.connect("http://127.0.0.1:5000"); // Single WebSocket Connection

// ✅ Function to Initialize Chart
function initializeChart() {
    var canvas = document.getElementById("binChart");

    if (!canvas) {
        console.error("❌ Error: Canvas for Chart.js not found!");
        return;
    }

    var ctx = canvas.getContext("2d");

    if (binChart) {
        binChart.destroy(); // ✅ Destroy existing chart if it exists
    }

    binChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Bin Fill Level (%)",
                data: [],
                backgroundColor: ["green", "yellow", "orange", "red"]
            }]
        },
        options: { responsive: true }
    });
}

// ✅ Function to Update Chart Data
function updateChart(bins) {
    if (!binChart) {
        console.error("❌ Error: Chart.js is not initialized!");
        return;
    }

    const binLabels = bins.map((bin) => bin.bin_id);
    const binWeights = bins.map((bin) => bin.weight);

    binChart.data.labels = binLabels;
    binChart.data.datasets[0].data = binWeights;
    binChart.update();
}

// ✅ Function to Initialize Map
function initializeMap() {
    var mapContainer = document.getElementById("map");
    if (!mapContainer) {
        console.error("❌ Error: Map container not found!");
        return;
    }

    if (map !== null) {
        map.remove(); // ✅ Destroy existing map before re-creating it
    }

    map = L.map("map").setView([51.505, -0.09], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([51.505, -0.09])
        .addTo(map)
        .bindPopup("A sample location.")
        .openPopup();
}

// ✅ Function to Fetch Initial Bin Data
function fetchInitialBinData() {
    console.log("Fetching bin data...");

    // Simulated API call
    setTimeout(() => {
        const bins = [
            { bin_id: "Bin 1", weight: 30 },
            { bin_id: "Bin 2", weight: 60 },
            { bin_id: "Bin 3", weight: 90 },
            { bin_id: "Bin 4", weight: 20 }
        ];

        if (!binChart) {
            initializeChart(); // ✅ Ensure chart is initialized before updating
        }

        updateChart(bins);
    }, 1000);
}

// ✅ Function to Initialize the Separate Chart
function initializeSeparateChart() {
    var canvas = document.getElementById("separateChart");

    if (!canvas) {
        console.error("❌ Error: Canvas for Separate Chart.js not found!");
        return;
    }

    var ctx = canvas.getContext("2d");

    if (separateChart) {
        separateChart.destroy(); // ✅ Destroy existing chart if it exists
    }

    separateChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Bin A", "Bin B", "Bin C", "Bin D"],
            datasets: [{
                label: "Bin Fill Level (%)",
                data: [10, 40, 70, 90], // Example data
                backgroundColor: ["blue", "purple", "cyan", "pink"]
            }]
        },
        options: { responsive: true }
    });
}

// ✅ Listen for real-time bin updates
socket.on("bin_update", function (bins) {
    console.log("Received bin update:", bins);
    updateChart(bins);
});

// ✅ Dark Mode Toggle with LocalStorage
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    // Save theme preference
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

// ✅ Initialize everything once when DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("binChart")) {
        initializeChart();
    } else {
        console.error("❌ Error: Chart canvas not found!");
    }

    initializeMap();
    fetchInitialBinData();

    // ✅ Dark Mode Persistence
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }

    // ✅ Ensure the button exists before adding event listener
    var toggleChartBtn = document.getElementById("toggleChartBtn");
    if (toggleChartBtn) {
        toggleChartBtn.addEventListener("click", function () {
            var chartContainer = document.getElementById("chartContainer");

            if (!chartContainer) {
                console.error("❌ Error: Chart container not found!");
                return;
            }

            if (chartContainer.style.display === "none") {
                chartContainer.style.display = "block";
                initializeSeparateChart();
                this.textContent = "Hide Charts";
            } else {
                chartContainer.style.display = "none";
                this.textContent = "Show Charts";
            }
        });
    } else {
        console.error("❌ Error: Toggle Chart Button not found!");
    }

    // ✅ Dark Mode Toggle Button
    var darkModeBtn = document.getElementById("toggleDarkMode");
    if (darkModeBtn) {
        darkModeBtn.addEventListener("click", toggleDarkMode);
    } else {
        console.error("❌ Error: Dark Mode Button not found!");
    }
});
