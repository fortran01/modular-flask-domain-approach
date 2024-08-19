# app/tests/controllers/test_loyalty_controller.py
import flask
import pytest
from flask import json
from app.controllers.loyalty_controller import bp as loyalty_bp
from app.controllers.customer_controller import bp as customer_bp
from app.services.loyalty_service import LoyaltyService
from app.services.customer_service import CustomerService
from unittest.mock import Mock, create_autospec


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(loyalty_bp)
    app.register_blueprint(customer_bp)
    # print(app.url_map)
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
def mock_loyalty_service(app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock = create_autospec(LoyaltyService)
        mocker.patch('flask.g.container.resolve', return_value=mock)
        return mock


def test_login(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_customer_service = create_autospec(CustomerService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_customer_service)

        # Arrange
        customer_data = {'customer_id': '1'}
        mock_customer_service.find_by_id.return_value = {'id': 1}

        # Act
        response = authenticated_client.post(
            '/login', json=customer_data)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == {'success': True}
        mock_customer_service.find_by_id.assert_called_once_with(1)


def test_logout(authenticated_client, app, mocker):
    # Arrange

    # Act
    response = authenticated_client.get('/logout')

    # Assert
    assert response.status_code == 200
    assert json.loads(response.data) == {'success': True}


def test_checkout(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_loyalty_service = create_autospec(LoyaltyService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_loyalty_service)
        # Arrange
        mock_loyalty_service.checkout.return_value = {
            'total': 100, 'points_used': 10}

        # Act
        response = authenticated_client.post('/checkout')

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == {'total': 100, 'points_used': 10}
        mock_loyalty_service.checkout.assert_called_once_with(1)


def test_get_points(authenticated_client, app, mocker):
    with app.app_context():
        if not hasattr(flask.g, 'container'):
            flask.g.container = Mock()
        mock_loyalty_service = create_autospec(LoyaltyService)
        mocker.patch('flask.g.container.resolve',
                     return_value=mock_loyalty_service)
        # Arrange
        mock_loyalty_service.get_customer_points.return_value = {
            'points': 150}

        # Act
        response = authenticated_client.get('/points')

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == {'points': 150}
        mock_loyalty_service.get_customer_points.assert_called_once_with(1)
