import json


def test_update_alert_correct_attributes(client, init_database):
    updated = {"threshold": 99999}
    response = client.patch(
        "/api/alerts/1", data=json.dumps(updated), content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["data"]["alert"]["threshold"] == 99999


def test_update_nonexistent_alert(client):
    updated = {"threshold": 50000}
    response = client.patch(
        "/api/alerts/999", data=json.dumps(updated), content_type="application/json"
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["status"] == "fail"


def test_update_alert_invalid_threshold(client, init_database):
    updated = {"threshold": "nope"}
    response = client.patch(
        "/api/alerts/1", data=json.dumps(updated), content_type="application/json"
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["status"] == "fail"
