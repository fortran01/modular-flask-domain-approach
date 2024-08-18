# app/guards/auth_guard.py

from functools import wraps
from flask import request, jsonify, g, Response
from typing import Callable, Any


class AuthGuard:
    @staticmethod
    def can_activate(f: Callable) -> Callable:
        """
        Decorator to check if a customer ID is present in cookies and
        valid for activating a route.

        Args:
            f (Callable): The function to wrap.

        Returns:
            Callable: The decorated function.
        """
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Response:
            customer_id = request.cookies.get('customer_id')
            if not customer_id:
                error_msg = jsonify(
                    {'error': 'Customer ID not found in cookies'})
                return Response(error_msg, status=401)
            g.customer_id = int(customer_id)
            return f(*args, **kwargs)
        return decorated_function
