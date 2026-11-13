from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid
import os

from ai.triage import classify_sos
from services.incidents import create_or_attach_incident


app = Flask(__name__)


# ============================================================
# IN-MEMORY DATA
# ============================================================

sos_reports = []
incidents = []


# ============================================================
# HOME PAGES
# ============================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/citizen")
def citizen():
    return render_template("citizen.html")


@app.route("/tracking")
def tracking():
    return render_template("tracking.html")


# ============================================================
# CREATE SOS
# ============================================================

@app.route("/api/sos", methods=["POST"])
def create_sos():

    data = request.get_json(silent=True) or request.form.to_dict()

    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    category = str(data.get("category", "Other")).strip()
    description = str(data.get("description", "")).strip()

    try:
        latitude = float(data.get("latitude"))
        longitude = float(data.get("longitude"))
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error": "Valid latitude and longitude are required."
        }), 400

    if not description:
        return jsonify({
            "success": False,
            "error": "Please enter an emergency description."
        }), 400

    # --------------------------------------------------------
    # AI TRIAGE
    # --------------------------------------------------------

    ai_result = classify_sos(description)

    severity = ai_result["severity"]

    # --------------------------------------------------------
    # CREATE SOS REPORT
    # --------------------------------------------------------

    tracking_id = "SOS-" + uuid.uuid4().hex[:8].upper()

    timestamp = datetime.now().isoformat(timespec="seconds")

    report = {
        "sos_id": tracking_id,
        "tracking_id": tracking_id,
        "name": name,
        "phone": phone,
        "category": category,
        "description": description,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp,
        "severity": severity,
        "score": ai_result["score"],
        "explanation": ai_result["explanation"],
        "status": "RECEIVED",
        "incident_id": None
    }

    sos_reports.append(report)

    # --------------------------------------------------------
    # INCIDENT FUSION
    # --------------------------------------------------------

    fusion_report = {
        "sos_id": tracking_id,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    }

    incident = create_or_attach_incident(
        fusion_report,
        incidents
    )

    report["incident_id"] = incident["incident_id"]

    return jsonify({
        "success": True,
        "tracking_id": tracking_id,
        "sos_id": tracking_id,
        "severity": severity,
        "score": ai_result["score"],
        "explanation": ai_result["explanation"],
        "incident_id": incident["incident_id"],
        "status": "RECEIVED"
    })


# ============================================================
# GET ALL SOS REPORTS
# ============================================================

@app.route("/api/sos", methods=["GET"])
def get_sos_reports():

    return jsonify(sos_reports)


# ============================================================
# GET ONE SOS BY TRACKING ID
# ============================================================

@app.route("/api/sos/<tracking_id>", methods=["GET"])
def get_sos(tracking_id):

    for report in sos_reports:

        if report["tracking_id"] == tracking_id:

            return jsonify(report)

    return jsonify({
        "success": False,
        "error": "SOS report not found."
    }), 404


# ============================================================
# GET INCIDENTS
# ============================================================

@app.route("/api/incidents", methods=["GET"])
def get_incidents():

    result = []

    for incident in incidents:

        reports = incident["reports"]

        if not reports:
            continue

        # Use the first report as the main map location
        first_report = reports[0]

        severities = []

        for report in sos_reports:

            if report["incident_id"] == incident["incident_id"]:
                severities.append(report["severity"])

        severity_order = {
            "LOW": 1,
            "MEDIUM": 2,
            "URGENT": 3,
            "HIGH": 4,
            "CRITICAL": 5
        }

        highest_severity = "LOW"

        for severity in severities:

            if severity_order.get(
                severity, 1
            ) > severity_order.get(
                highest_severity, 1
            ):
                highest_severity = severity

        result.append({
            "incident_id": incident["incident_id"],
            "report_count": incident["report_count"],
            "latitude": first_report["latitude"],
            "longitude": first_report["longitude"],
            "severity": highest_severity,
            "description": (
                f"{incident['report_count']} SOS report(s) "
                "fused into this incident."
            )
        })

    return jsonify(result)


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard_summary():

    active_reports = [
        report for report in sos_reports
        if report["status"] not in ["RESOLVED", "COMPLETED"]
    ]

    critical_reports = [
        report for report in active_reports
        if report["severity"] == "CRITICAL"
    ]

    return jsonify({
        "active_sos": len(active_reports),
        "critical_cases": len(critical_reports),
        "fused_incidents": len(incidents),
        "available_teams": 0
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "ONLINE",
        "service": "AlertNet",
        "ai": "ACTIVE",
        "incident_fusion": "ACTIVE"
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import webbrowser
    import threading

    print()
    print("========================================")
    print("       ALERTNET FLOOD RESPONSE")
    print("========================================")
    print("AI Triage       : ACTIVE")
    print("Incident Fusion : ACTIVE")
    print("Dashboard       : ACTIVE")
    print("========================================")
    print()

    def open_pages():
        webbrowser.open("http://127.0.0.1:5000/")
        webbrowser.open("http://127.0.0.1:5000/citizen")

    threading.Timer(2, open_pages).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )