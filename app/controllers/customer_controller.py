# app/controllers/customer_controller.py
from flask import Blueprint, request, jsonify, g, Response
from app.serialization.customer_serializer import CustomerSerializer
from app.guards.auth_guard import AuthGuard
from typing import List, Dict, Any

bp = Blueprint('customer', __name__)


@bp.route('/customers', methods=['GET'])
@AuthGuard.auth_required
def get_all_customers() -> Response:
    """
    Retrieve all customers from the database and serialize their data.

    Returns:
        Response: A JSON response containing a list of serialized customers
        and HTTP status code 200.
    """
    customer_service = g.container.resolve('customer_service')
    customers = customer_service.find_all()
    serialized_customers: List[Dict[str, Any]] = [
        CustomerSerializer.serialize_response(customer) for customer in
        customers
    ]
    return jsonify(serialized_customers), 200


@bp.route('/customers/<int:id>', methods=['GET'])
@AuthGuard.auth_required
def get_customer(id: int) -> Response:
    """
    Retrieve a single customer by their unique identifier
    and serialize their data.

    Args:
        id (int): The unique identifier of the customer.

    Returns:
        Response: A JSON response containing the serialized customer
        or an error message, with appropriate HTTP status code.
    """
    customer_service = g.container.resolve('customer_service')
    customer = customer_service.find_by_id(id)
    if customer:
        serialized_customer: Dict[str, Any] = CustomerSerializer. \
            serialize_response(customer)
        return jsonify(serialized_customer), 200
    return jsonify({'message': 'Customer not found'}), 404


@bp.route('/customers', methods=['POST'])
@AuthGuard.auth_required
def create_customer() -> Response:
    """
    Create a new customer based on the provided JSON data
    and serialize the created customer.

    Returns:
        Response: A JSON response with the serialized created customer and HTTP
        status code 201.
    """
    customer_service = g.container.resolve('customer_service')
    data = request.json
    customer_dto = CustomerSerializer.deserialize_create(data)
    created_customer = customer_service.create(customer_dto)
    serialized_customer: Dict[str, Any] = CustomerSerializer. \
        serialize_response(created_customer)
    return jsonify(serialized_customer), 201


@bp.route('/customers/<int:id>', methods=['PUT'])
@AuthGuard.auth_required
def update_customer(id: int) -> Response:
    """
    Update an existing customer's information based on the provided JSON data
    and serialize the updated customer.

    Args:
        id (int): The unique identifier of the customer to update.

    Returns:
        Response: A JSON response with the serialized updated customer
        or an error message, with appropriate HTTP status code.
    """
    customer_service = g.container.resolve('customer_service')
    data = request.json
    customer_dto = CustomerSerializer.deserialize_update(data)
    updated_customer = customer_service.update(id, customer_dto)
    if updated_customer:
        serialized_customer: Dict[str, Any] = CustomerSerializer. \
            serialize_response(updated_customer)
        return jsonify(serialized_customer), 200
    return jsonify({'message': 'Customer not found'}), 404


@bp.route('/customers/<int:id>', methods=['DELETE'])
@AuthGuard.auth_required
def delete_customer(id: int) -> Response:
    """
    Delete a customer by their unique identifier.

    Args:
        id (int): The unique identifier of the customer to delete.

    Returns:
        Response: A JSON response with an empty string
        and the HTTP status code 204.
    """
    customer_service = g.container.resolve('customer_service')
    customer_service.delete(id)
    return '', 204
