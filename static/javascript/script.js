// Theme Toggle
document.getElementById("toggleDarkModeBtn").addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  const mode = document.body.classList.contains("light-mode") ? "light" : "dark";
  localStorage.setItem("theme", mode);
});

// Apply saved theme
if (localStorage.getItem("theme") === "light") {
  document.body.classList.add("light-mode");
}

// Map Initialization
const map = L.map("map").setView([0.0236, 37.9062], 6);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Chart Setup
let binChart = null;
function initializeChart() {
  const ctx = document.getElementById("binChart").getContext("2d");
  if (binChart) binChart.destroy();

  binChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Bin 1", "Bin 2", "Bin 3", "Bin 4"],
      datasets: [{
        label: "Bin Fill Level (%)",
        data: [20, 50, 80, 100],
        backgroundColor: ["green", "yellow", "orange", "red"]
      }]
    },
    options: {
      responsive: true
    }
  });
}

// Chart View Toggle
document.getElementById("toggleChartsBtn").addEventListener("click", () => {
  const section = document.getElementById("chartSection");
  const isVisible = section.style.display === "block";
  section.style.display = isVisible ? "none" : "block";
  this.textContent = isVisible ? "📊 View Charts" : "❌ Hide Charts";
  if (!isVisible) initializeChart();
});

// Fetch History
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

// Refresh Data Simulation
document.getElementById("refreshDataBtn").addEventListener("click", () => {
  alert("✅ Data refreshed (simulation)");
});

// Register Collector Form (FIXED JSON)
document.getElementById("collectorForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const name = document.querySelector("#collectorForm input[name='name']").value;
  const whatsapp = document.querySelector("#collectorForm input[name='whatsapp']").value;

  const res = await fetch("/api/register-collector", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, whatsapp })
  });
  e.target.reset();
  document.getElementById('collectorForm').style.display = 'none';
  

  const result = await res.json();
  if (res.ok) {
    alert("✅ Collector registered successfully!");
    window.location.reload(); // Optionally, dynamically update the list
  } else {
    alert(`❌ Error registering collector: ${result.error}`);
  }
});

// Edit/Delete Collector
function editCollector(id) {
  window.location.href = `/edit-collector/${id}`;
}

async function notifyCollectors() {
  const res = await fetch('/send-whatsapp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      to: 'whatsapp:+254758293126',
      message: '🚨 Manual alert: Please check bin XYZ!'
    })
  });

  const data = await res.json();
  alert(data.message || data.status || 'Sent');
}

function deleteCollector(id) {
  if (confirm("Delete this collector?")) {
    fetch(`/delete-collector/${id}`, { method: "DELETE" })
      .then(res => res.ok ? res.json() : Promise.reject("Failed to delete"))
      .then(() => {
        alert("✅ Collector deleted.");
        window.location.reload();
      })
      .catch(err => alert("❌ " + err));
  }
}
document.getElementById("collectorSearch").addEventListener("input", function () {
  const query = this.value.toLowerCase();
  const collectors = document.querySelectorAll("#registeredCollectors ul li");

  collectors.forEach((li) => {
    const text = li.textContent.toLowerCase();
    li.style.display = text.includes(query) ? "list-item" : "none";
  });
});
// Notify All Collectors Button Logic
async function notifyAllCollectors() {
  const msg = prompt("Enter a message to notify all collectors:");
  if (!msg) return;

  const res = await fetch("/notify-all", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  });

  const result = await res.json();
  alert(result.message || result.error);
  loadNotificationLogs(); // Refresh log
}

// Load Notification Logs
async function loadNotificationLogs() {
  const res = await fetch("/logs");
  const data = await res.json();
  const list = document.getElementById("logList");
  list.innerHTML = "";

  data.logs.forEach(log => {
    const li = document.createElement("li");
    li.textContent = `${log.timestamp} → ${log.collector}: ${log.message}`;
    list.appendChild(li);
  });
}

// Load logs when page loads
document.addEventListener("DOMContentLoaded", loadNotificationLogs);
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function () {
    // Toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // Toggle the eye icon
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});
