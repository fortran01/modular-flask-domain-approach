# app/controllers/customer_controller.py
from flask import Blueprint, request, jsonify, g, Response
from app.serialization.customer_serializer import CustomerSerializer
from app.guards.auth_guard import auth_required

bp = Blueprint('customer', __name__)


@bp.route('/customers', methods=['GET'])
@auth_required
def get_all_customers() -> Response:
    """
    Retrieve all customers from the database.

    Returns:
        Response: A JSON response with the list of customers
        and HTTP status code 200.
    """
    customer_service = g.container.resolve('customer_service')
    customers = customer_service.find_all()
    serialized_customers = [CustomerSerializer.serialize_response(
        customer) for customer in customers]
    return Response(jsonify(serialized_customers), status=200)


@bp.route('/customers/<int:id>', methods=['GET'])
@auth_required
def get_customer(id: int) -> Response:
    """
    Retrieve a single customer by their unique identifier.

    Args:
        id (int): The unique identifier of the customer.

    Returns:
        Response: A JSON response containing the customer or an error message,
        with appropriate HTTP status code.
    """
    customer_service = g.container.resolve('customer_service')
    customer = customer_service.find_by_id(id)
    if customer:
        serialized_customer = CustomerSerializer.serialize_response(customer)
        return Response(jsonify(serialized_customer), status=200)
    return Response(jsonify({'message': 'Customer not found'}), status=404)


@bp.route('/customers', methods=['POST'])
@auth_required
def create_customer() -> Response:
    """
    Create a new customer based on the provided JSON data.

    Returns:
        Response: A JSON response with the created customer
        and HTTP status code 201.
    """
    customer_service = g.container.resolve('customer_service')
    data = request.json
    customer_dto = CustomerSerializer.deserialize_create(data)
    created_customer = customer_service.create(customer_dto)
    serialized_customer = CustomerSerializer.serialize_response(
        created_customer)
    return Response(jsonify(serialized_customer), status=201)


@bp.route('/customers/<int:id>', methods=['PUT'])
@auth_required
def update_customer(id: int) -> Response:
    """
    Update an existing customer's information.

    Args:
        id (int): The unique identifier of the customer to update.

    Returns:
        Response: A JSON response with the updated customer
        or an error message, with appropriate HTTP status code.
    """
    customer_service = g.container.resolve('customer_service')
    data = request.json
    customer_dto = CustomerSerializer.deserialize_update(data)
    updated_customer = customer_service.update(id, customer_dto)
    if updated_customer:
        serialized_customer = CustomerSerializer.serialize_response(
            updated_customer)
        return Response(jsonify(serialized_customer), status=200)
    return Response(jsonify({'message': 'Customer not found'}), status=404)


@bp.route('/customers/<int:id>', methods=['DELETE'])
@auth_required
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
    return Response('', status=204)
