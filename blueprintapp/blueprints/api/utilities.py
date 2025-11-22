from flask import jsonify, Response
from typing import Union


def jsend_success(
    data_key: str = None,
    data_value: Union[dict, list[dict]] = None,
    status_code: int = 200,
) -> Response:
    """
    Returns a JSend-compliant success response.

    This function formats a successful JSON response following the JSend specification.
    It includes a 'status' of 'success' and wraps the data inside a 'data' key.

    Args:
        data_key (str, optional): The key to use for the data payload. Defaults to None.
        data_value (Union[dict, list[dict]], optional): The value associated with the data_key.
            Can be a dictionary or a list of dictionaries. Defaults to None.
        status_code (int, optional): HTTP status code for the response. Defaults to 200.

    Returns:
        Response: Flask JSON response object with 'success' status and provided data.
    """
    if data_key == None and data_value == None:
        return jsonify({"status": "success", "data": None}), status_code

    return jsonify({"status": "success", "data": {data_key: data_value}}), status_code


def jsend_fail(data_key: str, data_value: str, status_code: int = 400) -> Response:
    """
    Returns a JSend-compliant failure response.

    This function formats a failure JSON response following the JSend specification.
    It includes a 'status' of 'fail' and wraps the data inside a 'data' key.

    Args:
        data_key (str): The key representing the specific failure data.
        data_value (str): A message or value explaining the failure.
        status_code (int, optional): HTTP status code for the response. Defaults to 400.

    Returns:
        Response: Flask JSON response object with 'fail' status and provided failure data.
    """
    return jsonify({"status": "fail", "data": {data_key: data_value}}), status_code


# def jsend_error() -> Response:
#     # TODO integrate errors?
#     pass


def validate_alert(data, partial: bool = False) -> Union[dict, Response]:
    """
    Validate alert payload.

    If `partial` is False (used for create/PUT semantics) both `email` and
    `threshold` are required. If `partial` is True (PATCH-like semantics) the
    function will validate only the fields that are present and return a dict
    with the normalized values.

    Returns either a dict with validated fields or a JSend `fail` Response.
    """
    email = data.get("email") if data is not None else None
    threshold = data.get("threshold") if data is not None else None

    validated: dict = {}

    # For full validation (create / non-partial), require presence
    if not partial:
        if not email:
            return jsend_fail(data_key="email", data_value="email is required")
        if threshold is None:
            return jsend_fail(data_key="threshold", data_value="threshold is required")

    # If email is provided, validate it's a non-empty string
    if email is not None:
        if not str(email).strip():
            return jsend_fail(
                data_key="email", data_value="email must be a non-empty string"
            )
        validated["email"] = str(email).strip()

    # If threshold is provided, validate numeric
    if threshold is not None:
        try:
            validated["threshold"] = float(threshold)
        except (ValueError, TypeError):
            return jsend_fail(
                data_key="threshold", data_value="threshold must be a number"
            )

    return validated
