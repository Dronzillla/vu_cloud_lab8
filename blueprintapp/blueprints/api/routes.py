from flask import Blueprint, request
from blueprintapp.blueprints.api.db_operations import (
    db_get_all_alerts,
    db_create_alert,
    db_get_alert_by_id,
    db_delete_alert,
    db_update_alert,
)
from blueprintapp.blueprints.api.utilities import validate_alert
from blueprintapp.blueprints.api.utilities import jsend_success, jsend_fail

alerts = Blueprint("alerts", __name__)


@alerts.route("/alerts", methods=["GET"])
def list_alerts():
    active = request.args.get("active", "false").lower() == "true"
    alerts_list = db_get_all_alerts(active_only=active)
    # Serialize output
    result = []
    for a in alerts_list:
        result.append(
            {
                "id": a.id,
                "email": a.email,
                "threshold": a.threshold,
                "active": a.active,
                "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
        )
    return jsend_success(data_key="alerts", data_value=result)


@alerts.route("/alerts", methods=["POST"])
def create_alert():
    data = request.get_json()
    result = validate_alert(data)
    if not isinstance(result, dict):
        return result
    alert = db_create_alert(result["email"], result["threshold"])
    # Return created resource
    alert_data = {
        "id": alert.id,
        "email": alert.email,
        "threshold": alert.threshold,
        "active": alert.active,
        "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    }
    return jsend_success("alert", alert_data, status_code=201)


@alerts.route("/alerts/<int:alert_id>", methods=["GET"])
def get_alert(alert_id: int):
    a = db_get_alert_by_id(alert_id)
    if a is None:
        return jsend_fail(
            data_key="alert", data_value="Alert does not exist", status_code=404
        )

    alert_data = {
        "id": a.id,
        "email": a.email,
        "threshold": a.threshold,
        "active": a.active,
        "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }
    return jsend_success(data_key="alert", data_value=alert_data)


@alerts.route("/alerts/<int:alert_id>", methods=["PUT", "PATCH"])
def update_alert(alert_id: int):
    a = db_get_alert_by_id(alert_id)
    if a is None:
        return jsend_fail("alert", "Alert does not exist", status_code=404)
    data = request.get_json() or {}

    # Use the same validation helper as create; in update we allow partial
    # validation so callers can PATCH/PUT with a subset of fields.
    result = validate_alert(data, partial=True)
    if not isinstance(result, dict):
        return result

    email = result.get("email") if "email" in result else None
    threshold = result.get("threshold") if "threshold" in result else None
    active = data.get("active")

    updated = db_update_alert(a, email=email, threshold=threshold, active=active)

    alert_data = {
        "id": updated.id,
        "email": updated.email,
        "threshold": updated.threshold,
        "active": updated.active,
        "triggered_at": (
            updated.triggered_at.isoformat() if updated.triggered_at else None
        ),
        "created_at": updated.created_at.isoformat() if updated.created_at else None,
    }
    return jsend_success("alert", alert_data)


@alerts.route("/alerts/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id: int):
    a = db_get_alert_by_id(alert_id)
    if a is None:
        return jsend_fail("alert", "Alert does not exist", status_code=404)

    db_delete_alert(a)
    return jsend_success()
