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
from datetime import datetime, timezone

alerts = Blueprint("alerts", __name__)


@alerts.route("/alerts", methods=["GET"])
def list_alerts():
    active_param = request.args.get("active")
    if active_param is None:
        alerts_list = db_get_all_alerts(active_only=None)  # return all
    elif active_param.lower() == "true":
        alerts_list = db_get_all_alerts(active_only=True)
    elif active_param.lower() == "false":
        alerts_list = db_get_all_alerts(active_only=False)
    else:
        return jsend_fail(
            data_key="active", data_value="active must be 'true' or 'false'"
        )

    # Serialize output
    result = []
    for alert in alerts_list:
        result.append(
            {
                "id": alert.id,
                "email": alert.email,
                "threshold": alert.threshold,
                "active": alert.active,
                "triggered_at": (
                    alert.triggered_at.isoformat() if alert.triggered_at else None
                ),
                "created_at": (
                    alert.created_at.isoformat() if alert.created_at else None
                ),
            }
        )

    return jsend_success(data_key="alerts", data_value=result)


@alerts.route("/alerts", methods=["POST"])
def create_alert():
    data = request.get_json()

    # Check if data is None
    if data is None:
        return jsend_fail(
            data_key="json",
            data_value="Malformed or missing JSON payload",
        )

    result = validate_alert(data=data, partial=False)
    if not isinstance(result, dict):
        return result
    alert = db_create_alert(email=result["email"], threshold=result["threshold"])
    # Return created resource
    alert_data = {
        "id": alert.id,
        "email": alert.email,
        "threshold": alert.threshold,
        "active": alert.active,
        "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    }
    return jsend_success(data_key="alert", data_value=alert_data, status_code=201)


@alerts.route("/alerts/<int:alert_id>", methods=["GET"])
def get_alert(alert_id: int):
    alert = db_get_alert_by_id(alert_id=alert_id)
    if alert is None:
        return jsend_fail(
            data_key="alert", data_value="Alert does not exist", status_code=404
        )

    alert_data = {
        "id": alert.id,
        "email": alert.email,
        "threshold": alert.threshold,
        "active": alert.active,
        "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    }
    return jsend_success(data_key="alert", data_value=alert_data)


@alerts.route("/alerts/<int:alert_id>", methods=["PUT", "PATCH"])
def update_alert(alert_id: int):
    alert = db_get_alert_by_id(alert_id)
    if alert is None:
        return jsend_fail(
            data_key="alert", data_value="Alert does not exist", status_code=404
        )
    data = request.get_json()

    # Use the same validation helper as create; in update we allow partial
    # validation so callers can PATCH/PUT with a subset of fields.
    if request.method == "PUT":
        # PUT means “replace the entire object”.
        if data is None:
            return jsend_fail("json", "Missing JSON payload")
        result = validate_alert(data, partial=False)
    else:
        # PATCH means “update only what you send”.
        if data is None:
            data = {}
        result = validate_alert(data, partial=True)

    if not isinstance(result, dict):
        return result

    email = result.get("email") if "email" in result else None
    threshold = result.get("threshold") if "threshold" in result else None
    active = data.get("active")

    # Another logic with triggered_at
    old_active = alert.active
    new_active = data.get("active")
    triggered_at = None
    # Only set triggered_at when transitioning from active → inactive
    if old_active is True and new_active is False:
        triggered_at = datetime.now(timezone.utc)

    updated = db_update_alert(
        alert=alert,
        email=email,
        threshold=threshold,
        active=active,
        triggered_at=triggered_at,
    )

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
    return jsend_success(data_key="alert", data_value=alert_data)


@alerts.route("/alerts/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id: int):
    alert = db_get_alert_by_id(alert_id=alert_id)
    if alert is None:
        return jsend_fail("alert", "Alert does not exist", status_code=404)

    db_delete_alert(alert=alert)
    return jsend_success()
