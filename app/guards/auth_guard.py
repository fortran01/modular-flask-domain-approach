# app/guards/auth_guard.py

from functools import wraps
from flask import request, jsonify, g, Response
from typing import Callable, Any, TypeVar

T = TypeVar('T', bound=Callable[..., Any])


class AuthGuard:
    @staticmethod
    def auth_required(f: T) -> T:
        """
        Decorator to ensure that a customer ID is present in cookies
        and is valid. This is required to access certain routes.

        Args:
            f (Callable[..., Any]): The function to be decorated.

        Returns:
            Callable[..., Any]: The decorated function which now includes
            authentication checks.
        """
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Response:
            customer_id = request.cookies.get('customer_id')
            if not customer_id:
                return jsonify({'error': 'Authentication required: \
                    No customer ID in cookies'}), 401
            g.customer_id = int(customer_id)
            return f(*args, **kwargs)
        return decorated_function
