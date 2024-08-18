# app/utils/error_handlers.py
from flask import jsonify, Response
from pydantic import ValidationError
from typing import Tuple


def handle_validation_error(e: ValidationError) -> Tuple[Response, int]:
    """
    Handles validation errors thrown by Pydantic models.

    Args:
        e (ValidationError): The exception raised by Pydantic validation.

    Returns:
        Tuple[Response, int]: A Flask response object with error details and
        the HTTP status code.
    """
    return jsonify({"error": "Validation error", "details": e.errors()}), 400


def handle_value_error(e: ValueError) -> Tuple[Response, int]:
    """
    Handles generic value errors typically related to data processing.

    Args:
        e (ValueError): The exception raised.

    Returns:
        Tuple[Response, int]: A Flask response object with error details and
        the HTTP status code.
    """
    return jsonify({"error": str(e)}), 400
