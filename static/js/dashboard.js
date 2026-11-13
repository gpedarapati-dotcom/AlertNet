// ============================================
// ALERTNET — COMMAND DASHBOARD
// ============================================

let allIncidents = [];

// --------------------------------------------
// START DASHBOARD
// --------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
    console.log("AlertNet Dashboard started");

    if (typeof initializeMap === "function") {
        initializeMap();
    }

    loadDashboardData();

    // Refresh every 5 seconds
    setInterval(loadDashboardData, 5000);
});


// --------------------------------------------
// LOAD DATA FROM BACKEND
// --------------------------------------------

async function loadDashboardData() {
    try {
        const response = await fetch("/api/sos");

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        const data = await response.json();

        // Support different backend response formats
        if (Array.isArray(data)) {
            allIncidents = data;
        } else if (Array.isArray(data.incidents)) {
            allIncidents = data.incidents;
        } else if (Array.isArray(data.sos)) {
            allIncidents = data.sos;
        } else if (Array.isArray(data.data)) {
            allIncidents = data.data;
        } else {
            allIncidents = [];
        }

        updateDashboard(allIncidents);

    } catch (error) {
        console.log("Waiting for backend:", error.message);
        showBackendWaiting();
    }
}


// --------------------------------------------
// UPDATE ENTIRE DASHBOARD
// --------------------------------------------

function updateDashboard(incidents) {

    updateMetrics(incidents);

    updateIncidentList(incidents);

    updateMap(incidents);

    updateFusion(incidents);

    updatePriority(incidents);

    updateTimeline(incidents);
}


// --------------------------------------------
// METRIC CARDS
// --------------------------------------------

function updateMetrics(incidents) {

    const active = incidents.filter(function (incident) {
        const status = String(
            incident.status || "ACTIVE"
        ).toUpperCase();

        return status !== "RESOLVED" &&
               status !== "COMPLETED";
    });

    const critical = incidents.filter(function (incident) {
        return getSeverity(incident) === "CRITICAL";
    });

    const fused = new Set();

    incidents.forEach(function (incident) {
        if (incident.incident_id) {
            fused.add(incident.incident_id);
        }
    });

    setText("activeSos", active.length);
    setText("criticalCases", critical.length);

    setText(
        "fusedIncidents",
        fused.size || incidents.length
    );

    // Rescue teams will be connected when backend provides them
    const teamElement = document.getElementById("availableTeams");

    if (teamElement && teamElement.textContent.trim() === "") {
        teamElement.textContent = "—";
    }
}


// --------------------------------------------
// SEVERITY
// --------------------------------------------

function getSeverity(incident) {

    const value =
        incident.severity ||
        incident.priority ||
        incident.level ||
        "LOW";

    return String(value).toUpperCase();
}


// --------------------------------------------
// INCIDENT LIST
// --------------------------------------------

function updateIncidentList(incidents) {

    const container = document.getElementById("incidentList");

    if (!container) return;

    if (!incidents || incidents.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <div style="font-size:32px;">✓</div>
                <strong>No active incidents</strong>
                <p>Waiting for incoming SOS reports...</p>
            </div>
        `;

        return;
    }

    container.innerHTML = "";

    incidents.slice(0, 10).forEach(function (incident) {

        const severity = getSeverity(incident);

        const id =
            incident.incident_id ||
            incident.tracking_id ||
            "SOS";

        const description =
            incident.description ||
            incident.message ||
            "Emergency report";

        const status =
            incident.status ||
            "ACTIVE";

        const card = document.createElement("div");

        card.className = "incident-card";

        card.innerHTML = `
            <div class="incident-header">
                <strong>${escapeHTML(id)}</strong>

                <span class="severity ${severity.toLowerCase()}">
                    ${escapeHTML(severity)}
                </span>
            </div>

            <div class="incident-description">
                ${escapeHTML(description)}
            </div>

            <div class="incident-meta">
                <span>Status: ${escapeHTML(String(status))}</span>
            </div>
        `;

        container.appendChild(card);
    });
}


// --------------------------------------------
// MAP
// --------------------------------------------

function updateMap(incidents) {

    if (
        typeof displayIncidentsOnMap === "function"
    ) {
        displayIncidentsOnMap(incidents);
    }
}


// --------------------------------------------
// INCIDENT FUSION
// --------------------------------------------

function updateFusion(incidents) {

    const sosCount = incidents.length;

    const incidentIds = new Set();

    incidents.forEach(function (incident) {

        if (incident.incident_id) {
            incidentIds.add(incident.incident_id);
        }
    });

    const fusionCount =
        incidentIds.size || sosCount;

    setText("sosFusionCount", sosCount);
    setText("incidentFusionCount", fusionCount);
}


// --------------------------------------------
// AI PRIORITY PANEL
// --------------------------------------------

function updatePriority(incidents) {

    const priorityElement =
        document.getElementById("priorityLevel");

    const messageElement =
        document.getElementById("priorityMessage");

    if (!priorityElement) return;

    if (!incidents || incidents.length === 0) {

        priorityElement.textContent = "STANDBY";

        if (messageElement) {
            messageElement.textContent =
                "Waiting for emergency reports.";
        }

        return;
    }

    // Find highest-priority active incident
    const priorityOrder = {
        CRITICAL: 4,
        HIGH: 3,
        MEDIUM: 2,
        LOW: 1
    };

    let highest = incidents[0];

    incidents.forEach(function (incident) {

        if (
            priorityOrder[getSeverity(incident)] >
            priorityOrder[getSeverity(highest)]
        ) {
            highest = incident;
        }
    });

    const severity = getSeverity(highest);

    priorityElement.textContent = severity;

    if (messageElement) {

        if (severity === "CRITICAL") {
            messageElement.textContent =
                "Immediate rescue response required.";
        }

        else if (severity === "HIGH") {
            messageElement.textContent =
                "High-priority incident detected.";
        }

        else if (severity === "MEDIUM") {
            messageElement.textContent =
                "Incident requires monitoring and response.";
        }

        else {
            messageElement.textContent =
                "Low-priority incident under monitoring.";
        }
    }

    setText(
        "rescueStatus",
        severity === "CRITICAL"
            ? "URGENT"
            : "PENDING"
    );
}


// --------------------------------------------
// ACTIVITY TIMELINE
// --------------------------------------------

function updateTimeline(incidents) {

    const timeline =
        document.getElementById("activityTimeline");

    if (!timeline) return;

    if (incidents.length === 0) {

        timeline.innerHTML = `
            <div class="timeline-item">
                <strong>System ready</strong>
                <span>Waiting for SOS reports</span>
            </div>
        `;

        return;
    }

    timeline.innerHTML = "";

    incidents.slice(0, 5).forEach(function (incident) {

        const id =
            incident.tracking_id ||
            incident.incident_id ||
            "SOS";

        const severity = getSeverity(incident);

        const item =
            document.createElement("div");

        item.className = "timeline-item";

        item.innerHTML = `
            <strong>New emergency: ${escapeHTML(id)}</strong>
            <span>AI priority: ${escapeHTML(severity)}</span>
        `;

        timeline.appendChild(item);
    });
}


// --------------------------------------------
// BROADCAST
// --------------------------------------------

async function sendBroadcast() {

    const status =
        document.getElementById("broadcastStatus");

    if (!status) return;

    status.textContent =
        "Broadcast simulation ready.";

    status.classList.add("success");

    // Actual broadcast endpoint will be connected
    // when the backend rescue/broadcast module is added.
}


// --------------------------------------------
// BACKEND WAITING MESSAGE
// --------------------------------------------

function showBackendWaiting() {

    const active =
        document.getElementById("activeSos");

    if (active && active.textContent.trim() === "") {
        active.textContent = "—";
    }

    const critical =
        document.getElementById("criticalCases");

    if (critical && critical.textContent.trim() === "") {
        critical.textContent = "—";
    }

    const fused =
        document.getElementById("fusedIncidents");

    if (fused && fused.textContent.trim() === "") {
        fused.textContent = "—";
    }

    const teams =
        document.getElementById("availableTeams");

    if (teams && teams.textContent.trim() === "") {
        teams.textContent = "—";
    }
}


// --------------------------------------------
// HELPER
// --------------------------------------------

function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function escapeHTML(value) {

    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}