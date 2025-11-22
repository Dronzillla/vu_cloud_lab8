from blueprintapp.app import db
from blueprintapp.blueprints.api.models import Alert


def db_get_all_alerts(active_only=None) -> list[Alert]:
    """Read all 'Alert' records in database.

    Args:
        active_only (bool | None, optional): Filter to return only active/not active/all alerts. Defaults to None.
    Returns:
        list[Alert]: list of 'Alert' objects, that were uploaded in database.
    """
    query = Alert.query
    if active_only is True:
        query = query.filter_by(active=True)
    elif active_only is False:
        query = query.filter_by(active=False)
    return query.all()


def db_create_alert(email: str, threshold: float) -> Alert:
    """Create new 'Alert' record in database.

    Args:
        email (str): Email address for alert notifications.
        threshold (float): Threshold value that triggers the alert.

    Returns:
        Alert: 'Alert' object
    """
    alert = Alert(email=email, threshold=threshold)
    db.session.add(alert)
    db.session.commit()
    return alert


def db_get_alert_by_id(alert_id: int) -> Alert | None:
    """Search for 'Alert' record by provided id.

    Args:
        alert_id (int): Alert.id

    Returns:
        Alert | None: 'Alert' object if record was found, 'None' if no 'Alert' object matching the filters was found.
    """
    return Alert.query.filter_by(id=alert_id).one_or_none()


def db_delete_alert(alert: Alert) -> None:
    """Deletes 'Alert' object from database.

    Args:
        alert (Alert): 'Alert' object to delete.

    Returns:
        None
    """
    db.session.delete(alert)
    db.session.commit()


def db_update_alert(
    alert: Alert,
    *,
    email: str | None = None,
    threshold: float | None = None,
    active: bool | None = None,
    triggered_at=None
) -> Alert:
    """Update 'Alert' object with provided values.

    Args:
        alert (Alert): Alert object
        email (str | None, optional): new email address
        threshold (float | None, optional): new threshold value
        active (bool | None, optional): new active status
        triggered_at (optional): new triggered timestamp

    Returns:
        Alert: updated 'Alert' object
    """
    if email is not None:
        alert.email = email
    if threshold is not None:
        alert.threshold = float(threshold)
    if active is not None:
        alert.active = bool(active)
    if triggered_at is not None:
        alert.triggered_at = triggered_at

    db.session.commit()
    return alert
