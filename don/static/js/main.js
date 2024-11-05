// main.js
let countdownInterval;
let updateInterval = parseInt(document.getElementById('update-frequency').value) || 10;

// Set initial browser update time
function setBrowserUpdateTime() {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString("en-US", { hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true });
    document.getElementById("browser-update-time").textContent = formattedTime;
}

// Update countdown and fetch data on interval
function updateCountdown() {
    let nextUpdateIn = updateInterval;
    clearInterval(countdownInterval);

    countdownInterval = setInterval(() => {
        document.getElementById("next-update").textContent = nextUpdateIn;
        nextUpdateIn--;

        if (nextUpdateIn < 0) {
            clearInterval(countdownInterval);
            fetchUpdate(); // Fetch data and update
        }
    }, 1000);
}

// Fetch new data and refresh page content
async function fetchUpdate() {
    try {
        const response = await fetch(window.location.href);
        const html = await response.text();
        document.documentElement.innerHTML = html;

        // Reapply JS logic after update
        setBrowserUpdateTime();
        updateCountdown();
    } catch (error) {
        console.error("Failed to fetch update:", error);
    }
}

// Event listener to adjust interval based on dropdown selection
document.getElementById('update-frequency').addEventListener('change', (event) => {
    updateInterval = parseInt(event.target.value);
    updateCountdown();
});

document.addEventListener("DOMContentLoaded", () => {
    setBrowserUpdateTime();
    updateCountdown();
});