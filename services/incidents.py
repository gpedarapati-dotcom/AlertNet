from datetime import datetime
from math import radians, sin, cos, sqrt, atan2


# Incident fusion rules
MAX_DISTANCE_METERS = 200
MAX_TIME_MINUTES = 30


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in meters.
    """

    earth_radius = 6371000  # meters

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def time_difference_minutes(time1, time2):
    """
    Calculate difference between two timestamps in minutes.
    """

    if isinstance(time1, str):
        time1 = datetime.fromisoformat(time1)

    if isinstance(time2, str):
        time2 = datetime.fromisoformat(time2)

    difference = abs((time1 - time2).total_seconds())

    return difference / 60


def is_same_incident(report1, report2):
    """
    Check whether two SOS reports are candidates
    for the same incident.

    Conditions:
    - Distance <= 200 meters
    - Time difference <= 30 minutes
    """

    distance = haversine_distance(
        report1["latitude"],
        report1["longitude"],
        report2["latitude"],
        report2["longitude"]
    )

    time_difference = time_difference_minutes(
        report1["timestamp"],
        report2["timestamp"]
    )

    return (
        distance <= MAX_DISTANCE_METERS
        and time_difference <= MAX_TIME_MINUTES
    )


def find_matching_incident(report, incidents):
    """
    Find an existing incident that matches the new SOS report.
    """

    for incident in incidents:

        for existing_report in incident["reports"]:

            if is_same_incident(report, existing_report):
                return incident

    return None


def create_or_attach_incident(report, incidents):
    """
    Attach an SOS report to an existing incident
    or create a new incident.

    Original SOS reports are never deleted.
    """

    matching_incident = find_matching_incident(
        report,
        incidents
    )

    # Existing incident found
    if matching_incident:

        matching_incident["reports"].append(report)

        matching_incident["report_count"] = len(
            matching_incident["reports"]
        )

        return matching_incident

    # No matching incident → create new incident
    incident_id = f"INC{len(incidents) + 1:03d}"

    new_incident = {
        "incident_id": incident_id,
        "reports": [report],
        "report_count": 1
    }

    incidents.append(new_incident)

    return new_incident


# ------------------------------------------------
# DEMO / TEST
# ------------------------------------------------

if __name__ == "__main__":

    incidents = []

    base_time = "2026-11-13T10:00:00"

    reports = [

        {
            "sos_id": "SOS001",
            "latitude": 17.3850,
            "longitude": 78.4860,
            "timestamp": base_time
        },

        {
            "sos_id": "SOS002",
            "latitude": 17.3860,
            "longitude": 78.4865,
            "timestamp": "2026-11-13T10:10:00"
        },

        {
            "sos_id": "SOS003",
            "latitude": 17.3855,
            "longitude": 78.4862,
            "timestamp": "2026-11-13T20:00:00"
        }
    ]

    for report in reports:

        incident = create_or_attach_incident(
            report,
            incidents
        )

        print(
            f"{report['sos_id']} → "
            f"{incident['incident_id']}"
        )

    print("\nIncident Summary")
    print("================")

    for incident in incidents:

        print(
            incident["incident_id"],
            "→",
            incident["report_count"],
            "SOS reports"
        )