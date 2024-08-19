# app/tests/controllers/test_product_controller.py
import flask
import pytest
from flask import json
from app.controllers.product_controller import bp as product_bp
from app.services.product_service import ProductService
from unittest.mock import Mock, create_autospec


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(product_bp)
    return app


@pytest.fixture
def test_client(app, mocker):
    mocker.patch('app.guards.auth_guard.AuthGuard.auth_required',
                 return_value=None)
    return app.test_client()


@pytest.fixture
def mock_product_service(app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock = create_autospec(ProductService)
        mocker.patch('flask.g.container.resolve', return_value=mock)
        return mock


def test_get_all_products(test_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_product_service = create_autospec(ProductService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_product_service)
        # Arrange
        mock_product_service.find_all.return_value = [
            {'id': 1, 'name': 'Test Product'}]
        # Act
        response = test_client.get('/products')
        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == [{'id': 1, 'name': 'Test Product'}]


def test_get_product(test_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_product_service = create_autospec(ProductService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_product_service)
        # Arrange
        mock_product_service.find_by_id.return_value = {
            'id': 1, 'name': 'Test Product'}
        # Act
        response = test_client.get('/products/1')
        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == {'id': 1, 'name': 'Test Product'}


def test_create_product(test_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_product_service = create_autospec(ProductService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_product_service)
        # Arrange
        product_data = {'name': 'New Product', 'price': 20, 'category_id': 1}
        mock_product_service.create.return_value = {
            'id': 2, 'name': 'New Product', 'price': 20, 'category_id': 1}
        # Act
        response = test_client.post('/products', json=product_data)
        # Assert
        assert response.status_code == 201
        assert json.loads(response.data) == {
            'id': 2, 'name': 'New Product', 'price': 20, 'category_id': 1}


def test_update_product(test_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_product_service = create_autospec(ProductService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_product_service)
        # Arrange
        product_data = {'name': 'Updated Product', 'price': 25}
        mock_product_service.update.return_value = {
            'id': 1, 'name': 'Updated Product', 'price': 25}
        # Act
        response = test_client.put('/products/1', json=product_data)
        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == {
            'id': 1, 'name': 'Updated Product', 'price': 25}


def test_delete_product(test_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_product_service = create_autospec(ProductService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_product_service)
        # Arrange
        # Act
        response = test_client.delete('/products/1')
        # Assert
        assert response.status_code == 204
        assert response.data == b''
