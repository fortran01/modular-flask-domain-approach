# app/controllers/loyalty_controller.py
from typing import List, Dict, Any
from flask import render_template
from flask import (Blueprint, request, jsonify, g, make_response, abort,
                   Response)
from app.serialization.loyalty_serializer import LoyaltySerializer
from app.guards.auth_guard import AuthGuard
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('loyalty', __name__)


@bp.route('/')
def index() -> str:
    """
    Render the index page with customer and product data.

    This route checks if a customer is logged in by looking for a 'customer_id'
    cookie. If logged in, it fetches all products. It then renders the index
    template with the appropriate data.

    Returns:
        str: Rendered HTML content of the index page.
    """
    customer_id: str | None = request.cookies.get('customer_id')
    logged_in: bool = bool(customer_id)
    products: List[Dict[str, Any]] = []

    if logged_in:
        product_service = g.container.resolve('product_service')
        products: List[Dict[str, Any]] = product_service.find_all()

    return render_template('index.html',
                           logged_in=logged_in,
                           customer_id=customer_id,
                           products=products)


@bp.route('/login', methods=['POST'])
def login() -> Response:
    """
    Authenticate a customer and set a secure cookie with their ID.

    Returns:
        make_response: A JSON response indicating success or failure, with
        appropriate HTTP status code.
    """
    customer_service = g.container.resolve('customer_service')
    data = request.json
    customer_id = data.get('customer_id')
    if not customer_id:
        return make_response(jsonify({'error': 'Customer ID is required'}),
                             400)
    customer = customer_service.find_by_id(int(customer_id))
    if not customer:
        return make_response(jsonify({'error': 'Invalid customer ID'}), 401)
    response = make_response(jsonify({'success': True}), 200)
    response.set_cookie('customer_id', str(customer_id),
                        httponly=True, secure=True, samesite='Strict')
    return response


@bp.route('/logout', methods=['GET'])
def logout() -> Response:
    """
    Log out a customer by deleting their ID cookie.

    Returns:
        make_response: A JSON response indicating success,
        with HTTP status code.
    """
    response = make_response(jsonify({'success': True}), 200)
    response.delete_cookie('customer_id')
    return response


@bp.route('/checkout', methods=['POST'])
@AuthGuard.auth_required
def checkout() -> Response:
    """
    Processes a checkout request, applying loyalty points based on the
    customer's ID stored in cookies.

    Returns:
        make_response: A JSON response with checkout data and HTTP status code.
    """
    loyalty_service = g.container.resolve('loyalty_service')
    customer_id = g.customer_id
    result = loyalty_service.checkout(int(customer_id))
    serialized: Dict[str, Any] = LoyaltySerializer. \
        serialize_checkout_response(result)
    logger.debug(f"serialized: {serialized}")
    if serialized.get('success', False):
        shopping_cart_service = g.container.resolve('shopping_cart_service')
        shopping_cart_service.clear_cart(int(customer_id))
    return make_response(jsonify(serialized), 200)


@bp.route('/points', methods=['GET'])
@AuthGuard.auth_required
def get_points() -> Response:
    """
    Retrieves the loyalty points for a customer based on their ID stored in
    cookies.

    Returns:
        make_response: A JSON response with points data and HTTP status code.
    """
    loyalty_service = g.container.resolve('loyalty_service')
    customer_id = g.customer_id
    points = loyalty_service.get_customer_points(int(customer_id))
    serialized = LoyaltySerializer.serialize_points(points)
    return make_response(jsonify(serialized), 200)


@bp.route('/cart', methods=['POST'])
@AuthGuard.auth_required
def add_to_cart() -> Response:
    """
    Adds an item to the shopping cart.
    """
    shopping_cart_service = g.container.resolve('shopping_cart_service')
    customer_id = g.customer_id
    logger.info(f"request: {request.json}")
    product_id = request.json.get('productId')
    quantity = request.json.get('quantity')
    shopping_cart_service.add_item(
        int(customer_id), int(product_id), int(quantity))
    return make_response(jsonify({'success': True}), 200)


@bp.route('/cart', methods=['GET'])
@AuthGuard.auth_required
def get_cart() -> Response:
    """
    Retrieves the shopping cart for a customer.
    """
    shopping_cart_service = g.container.resolve('shopping_cart_service')
    customer_id = g.customer_id
    cart = shopping_cart_service.get_cart(int(customer_id))
    serialized = LoyaltySerializer.serialize_shopping_cart(cart)
    if not cart:
        abort(404, description="Shopping cart not found")
    return make_response(jsonify(serialized), 200)


@bp.route('/cart/<int:product_id>', methods=['PUT'])
@AuthGuard.auth_required
def update_cart_item(product_id) -> Response:
    """
    Updates a cart item's quantity.
    """
    shopping_cart_service = g.container.resolve('shopping_cart_service')
    customer_id = g.customer_id
    quantity = request.json.get('quantity')
    shopping_cart_service.update_item_quantity(
        int(customer_id), product_id, int(quantity))
    return make_response(jsonify({'success': True}), 200)


@bp.route('/cart/<int:product_id>', methods=['DELETE'])
@AuthGuard.auth_required
def remove_from_cart(product_id) -> Response:
    """
    Removes an item from the shopping cart.
    """
    shopping_cart_service = g.container.resolve('shopping_cart_service')
    customer_id = g.customer_id
    shopping_cart_service.remove_item(int(customer_id), product_id)
    return make_response(jsonify({'success': True}), 200)


@bp.route('/cart', methods=['DELETE'])
@AuthGuard.auth_required
def clear_cart() -> Response:
    """
    Clears the shopping cart for a customer.
    """
    shopping_cart_service = g.container.resolve('shopping_cart_service')
    customer_id = g.customer_id
    shopping_cart_service.clear_cart(int(customer_id))
    return make_response(jsonify({'success': True}), 200)
