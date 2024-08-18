# app/tests/controllers/test_customer_controller.py
import flask
import pytest
from flask import json
from app.controllers.customer_controller import bp as customer_bp
from app.services.customer_service import CustomerService
from unittest.mock import Mock
from app.schemas.customer import CustomerUpdateDto


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(customer_bp)
    return app


@pytest.fixture
def test_client(app, mocker):
    mocker.patch('app.guards.auth_guard.AuthGuard.auth_required',
                 return_value=None)
    return app.test_client()


@pytest.fixture
def authenticated_client(test_client):
    test_client.set_cookie('customer_id', '1')
    return test_client


@pytest.fixture
def mock_customer_service(app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve', return_value=mock)
        return mock


def test_get_all_customers(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)

        # Arrange
        mock_customers = [
            {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane Doe', 'email': 'jane@example.com'}
        ]
        mock_customer_service.find_all.return_value = mock_customers

        # Act
        response = authenticated_client.get('/customers')

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == mock_customers
        mock_customer_service.find_all.assert_called_once()


def test_get_customer(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)
        # Arrange
        mock_customer = {'id': 1, 'name': 'John Doe',
                         'email': 'john@example.com'}
        mock_customer_service.find_by_id.return_value = mock_customer

        # Act
        response = authenticated_client.get('/customers/1')

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == mock_customer
        mock_customer_service.find_by_id.assert_called_once_with(1)


def test_get_customer_not_found(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)
        # Arrange
        mock_customer_service.find_by_id.return_value = None

        # Act
        response = authenticated_client.get('/customers/999')

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == {'message': 'Customer not found'}
        mock_customer_service.find_by_id.assert_called_once_with(999)


def test_create_customer(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)
        # Arrange
        customer_data = {'name': 'Jane Doe', 'email': 'jane@example.com'}
        mock_customer_service.create.return_value = {'id': 1, **customer_data}

        # Act
        response = authenticated_client.post('/customers', json=customer_data)

        # Assert
        assert response.status_code == 201
        assert json.loads(response.data) == {'id': 1, **customer_data}
        mock_customer_service.create.assert_called_once()


def test_update_customer(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)
        # Arrange
        customer_data = {'name': 'Jane Updated'}
        update_dto = CustomerUpdateDto(name='Jane Updated', email=None)
        mock_customer_service.update.return_value = {'id': 1, **customer_data}

        # Act
        response = authenticated_client.put('/customers/1', json=customer_data)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == {'id': 1, **customer_data}
        mock_customer_service.update.assert_called_once_with(1, update_dto)


def test_delete_customer(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = Mock(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)
        # Arrange

        # Act
        response = authenticated_client.delete('/customers/1')

        # Assert
        assert response.status_code == 204
        mock_customer_service.delete.assert_called_once_with(1)
