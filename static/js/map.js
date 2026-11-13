// ============================================
// ALERTNET — LIVE INCIDENT MAP
// ============================================

let alertMap = null;
let incidentMarkers = [];


// ============================================
// INITIALIZE MAP
// ============================================

function initializeMap() {

    const mapElement = document.getElementById("map");

    // Stop if this page doesn't contain a map
    if (!mapElement) {
        return;
    }

    // Prevent duplicate initialization
    if (alertMap) {
        return;
    }

    // Hyderabad default location
    alertMap = L.map("map").setView(
        [17.3850, 78.4867],
        11
    );


    // OpenStreetMap tiles
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution:
                '&copy; OpenStreetMap contributors'
        }
    ).addTo(alertMap);


    // Initial marker
    addIncidentMarker(
        17.3850,
        78.4867,
        "AlertNet Command Center",
        "System monitoring area",
        "LOW"
    );

}



// ============================================
// ADD INCIDENT MARKER
// ============================================

function addIncidentMarker(
    latitude,
    longitude,
    title,
    description,
    severity
) {

    if (!alertMap) {
        return;
    }


    if (
        latitude === undefined ||
        longitude === undefined ||
        latitude === null ||
        longitude === null
    ) {
        return;
    }


    const lat =
        parseFloat(latitude);

    const lng =
        parseFloat(longitude);


    if (
        Number.isNaN(lat) ||
        Number.isNaN(lng)
    ) {
        return;
    }


    // ========================================
    // MARKER COLOR
    // ========================================

    let color = "#25d366";

    const level =
        String(
            severity || "LOW"
        ).toUpperCase();


    if (level === "CRITICAL") {

        color = "#ff4757";

    }

    else if (level === "HIGH") {

        color = "#ff8c42";

    }

    else if (level === "MEDIUM") {

        color = "#ffc107";

    }


    // ========================================
    // CUSTOM CIRCLE MARKER
    // ========================================

    const markerIcon =
        L.divIcon({

            className: "",

            html: `
                <div style="
                    width:20px;
                    height:20px;
                    border-radius:50%;
                    background:${color};
                    border:3px solid white;
                    box-shadow:
                        0 0 0 5px ${color}33,
                        0 0 18px ${color};
                "></div>
            `,

            iconSize: [20, 20],

            iconAnchor: [10, 10]

        });


    const marker =
        L.marker(
            [lat, lng],
            {
                icon: markerIcon
            }
        ).addTo(alertMap);


    // ========================================
    // POPUP
    // ========================================

    marker.bindPopup(`

        <div style="
            min-width:220px;
            font-family:Arial,sans-serif;
        ">

            <strong style="
                font-size:16px;
            ">
                ${escapeMapText(title || "Emergency Incident")}
            </strong>

            <br><br>

            <span style="
                color:#666;
                font-size:13px;
            ">
                ${escapeMapText(description || "No description")}
            </span>

            <br><br>

            <strong>
                Severity:
            </strong>

            <span style="
                color:${color};
                font-weight:bold;
            ">
                ${escapeMapText(level)}
            </span>

            <br><br>

            <span style="
                color:#666;
                font-size:11px;
            ">
                ${lat.toFixed(5)},
                ${lng.toFixed(5)}
            </span>

        </div>

    `);


    incidentMarkers.push(marker);

}



// ============================================
// CLEAR ALL INCIDENT MARKERS
// ============================================

function clearIncidentMarkers() {

    incidentMarkers.forEach(
        function(marker) {

            if (alertMap) {
                alertMap.removeLayer(marker);
            }

        }
    );


    incidentMarkers = [];

}



// ============================================
// DISPLAY INCIDENTS ON MAP
// ============================================

function displayIncidentsOnMap(incidents) {

    if (!alertMap) {
        return;
    }


    clearIncidentMarkers();


    if (
        !Array.isArray(incidents) ||
        incidents.length === 0
    ) {

        return;

    }


    let bounds = [];


    incidents.forEach(
        function(incident) {

            const latitude =
                incident.latitude ??
                incident.lat;


            const longitude =
                incident.longitude ??
                incident.lng ??
                incident.lon;


            if (
                latitude === undefined ||
                longitude === undefined
            ) {
                return;
            }


            addIncidentMarker(

                latitude,

                longitude,

                incident.incident_id ||
                incident.tracking_id ||
                "Emergency Incident",

                incident.description ||
                incident.message ||
                "Emergency report",

                incident.severity ||
                incident.priority ||
                "LOW"

            );


            bounds.push(
                [
                    parseFloat(latitude),
                    parseFloat(longitude)
                ]
            );

        }
    );


    // ========================================
    // FIT MAP TO INCIDENTS
    // ========================================

    if (bounds.length > 0) {

        alertMap.fitBounds(
            bounds,
            {
                padding: [40, 40],
                maxZoom: 14
            }
        );

    }

}



// ============================================
// ESCAPE TEXT FOR MAP POPUPS
// ============================================

function escapeMapText(value) {

    const text =
        String(value ?? "");


    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}



// ============================================
// START MAP
// ============================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        initializeMap();

    }
);