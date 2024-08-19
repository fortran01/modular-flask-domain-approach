# app/controllers/product_controller.py
from flask import Blueprint, request, jsonify, g, make_response, Response
from app.serialization.product_serializer import ProductSerializer

bp = Blueprint('product', __name__)


@bp.route('/products', methods=['GET'])
def get_all_products() -> Response:
    """
    Retrieve all products.

    Returns:
        Response: A JSON response with list of products and HTTP status code.
    """
    product_service = g.container.resolve('product_service')
    products = product_service.find_all()
    serialized = ProductSerializer.serialize_response(products)
    return make_response(jsonify(serialized), 200)


@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id: int) -> Response:
    """
    Retrieve a single product by its ID.

    Args:
        id (int): The ID of the product to retrieve.

    Returns:
        Response: A JSON response with the product or error message
        and HTTP status code.
    """
    product_service = g.container.resolve('product_service')
    product = product_service.find_by_id(id)
    if product:
        serialized = ProductSerializer.serialize_response(product)
        return make_response(jsonify(serialized), 200)
    return make_response(jsonify({'message': 'Product not found'}), 404)


@bp.route('/products', methods=['POST'])
def create_product() -> Response:
    """
    Create a new product.

    Returns:
        Response: A JSON response with the created product
        and HTTP status code.
    """
    product_service = g.container.resolve('product_service')
    data = request.json
    product_dto = ProductSerializer.deserialize_create(data)
    created_product = product_service.create(product_dto)
    serialized = ProductSerializer.serialize_response(created_product)
    return make_response(jsonify(serialized), 201)


@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id: int) -> Response:
    """
    Update an existing product.

    Args:
        id (int): The ID of the product to update.

    Returns:
        Response: A JSON response with the updated product or error message
        and HTTP status code.
    """
    product_service = g.container.resolve('product_service')
    data = request.json
    product_dto = ProductSerializer.deserialize_update(data)
    updated_product = product_service.update(id, product_dto)
    if updated_product:
        serialized = ProductSerializer.serialize_response(updated_product)
        return make_response(jsonify(serialized), 200)
    return make_response(jsonify({'message': 'Product not found'}), 404)


@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id: int) -> Response:
    """
    Delete a product by its ID.

    Args:
        id (int): The ID of the product to delete.

    Returns:
        Response: A JSON response with an empty string and HTTP status code.
    """
    product_service = g.container.resolve('product_service')
    product_service.delete(id)
    return make_response('', 204)
