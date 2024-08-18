# app/controllers/loyalty_controller.py
from flask import Blueprint, request, jsonify, g, Response, make_response
from app.serialization.loyalty_serializer import LoyaltySerializer
from app.guards.auth_guard import AuthGuard
bp = Blueprint('loyalty', __name__)


@bp.route('/login', methods=['POST'])
def login() -> Response:
    """
    Authenticate a customer and set a secure cookie with their ID.

    Returns:
        Response: A JSON response indicating success or failure, with
        appropriate HTTP status code.
    """
    customer_service = g.container.resolve('customer_service')
    data = request.json
    customer_id = data.get('customer_id')
    if not customer_id:
        return Response(jsonify({'error': 'Customer ID is required'}),
                        status=400)
    customer = customer_service.find_by_id(int(customer_id))
    if not customer:
        return Response(jsonify({'error': 'Invalid customer ID'}), status=401)
    response = make_response(jsonify({'success': True}))
    response.set_cookie('customer_id', str(customer_id),
                        httponly=True, secure=True, samesite='Strict')
    return response, 200


@bp.route('/logout', methods=['GET'])
def logout() -> Response:
    """
    Log out a customer by deleting their ID cookie.

    Returns:
        Response: A JSON response indicating success, with HTTP status code.
    """
    response = make_response(jsonify({'success': True}))
    response.delete_cookie('customer_id')
    return response, 200


@bp.route('/checkout', methods=['POST'])
@AuthGuard.auth_required
def checkout() -> Response:
    """
    Processes a checkout request, applying loyalty points based on the
    customer's ID stored in cookies.

    Returns:
        Response: A JSON response with checkout data and HTTP status code.
    """
    loyalty_service = g.container.resolve('loyalty_service')
    customer_id = g.customer_id
    result = loyalty_service.checkout(int(customer_id))
    serialized = LoyaltySerializer.serialize_checkout_response(result)
    return Response(jsonify(serialized), status=200)


@bp.route('/points', methods=['GET'])
@AuthGuard.auth_required
def get_points() -> Response:
    """
    Retrieves the loyalty points for a customer based on their ID stored in
    cookies.

    Returns:
        Response: A JSON response with points data and HTTP status code.
    """
    loyalty_service = g.container.resolve('loyalty_service')
    customer_id = g.customer_id
    points = loyalty_service.get_customer_points(int(customer_id))
    serialized = LoyaltySerializer.serialize_points(points)
    return Response(jsonify(serialized), status=200)
