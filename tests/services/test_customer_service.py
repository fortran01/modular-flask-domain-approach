# app/tests/services/test_customer_service.py
import pytest
from unittest.mock import Mock
from app.services.customer_service import CustomerService
from app.models.domain.customer import Customer
from app.models.domain.loyalty_account import LoyaltyAccount
from app.schemas.customer import (
    CustomerCreateDto,
    CustomerUpdateDto,
    CustomerResponseDto
)


@pytest.fixture
def customer_service():
    mock_customer_repository = Mock()
    mock_loyalty_account_repository = Mock()
    return CustomerService(
        mock_customer_repository,
        mock_loyalty_account_repository
    )


def test_find_by_id_existing_customer(customer_service):
    # Arrange
    mock_customer = Customer(id=1, name="John Doe", email="john@example.com")
    customer_service.customer_repository.find_by_id.return_value = (
        mock_customer
    )

    # Act
    result = customer_service.find_by_id(1)

    # Assert
    assert isinstance(result, CustomerResponseDto)
    assert result.id == 1
    assert result.name == "John Doe"
    assert result.email == "john@example.com"
    customer_service.customer_repository.find_by_id.assert_called_once_with(1)


def test_find_by_id_non_existing_customer(customer_service):
    # Arrange
    customer_service.customer_repository.find_by_id.return_value = None

    # Act
    result = customer_service.find_by_id(999)

    # Assert
    assert result is None
    customer_service.customer_repository.find_by_id.assert_called_once_with(
        999)


def test_create_customer(customer_service):
    # Arrange
    create_dto = CustomerCreateDto(name="Jane Doe", email="jane@example.com")
    mock_customer = Customer(id=2, name="Jane Doe", email="jane@example.com")
    customer_service.customer_repository.create.return_value = mock_customer
    customer_service.loyalty_account_repository.create.return_value = (
        LoyaltyAccount(id=1, customer_id=2, points=0)
    )

    # Act
    result = customer_service.create(create_dto)

    # Assert
    assert isinstance(result, CustomerResponseDto)
    assert result.id == 2
    assert result.name == "Jane Doe"
    assert result.email == "jane@example.com"
    customer_service.customer_repository.create.assert_called_once()
    customer_service.loyalty_account_repository.create.assert_called_once()


def test_update_existing_customer(customer_service):
    # Arrange
    update_dto = CustomerUpdateDto(
        name="John Updated", email="john.updated@example.com")
    mock_customer = Customer(id=1, name="John Doe", email="john@example.com")
    customer_service.customer_repository.find_by_id.return_value = (
        mock_customer
    )
    customer_service.customer_repository.update.return_value = Customer(
        id=1, name="John Updated", email="john.updated@example.com"
    )

    # Act
    result = customer_service.update(1, update_dto)

    # Assert
    assert isinstance(result, CustomerResponseDto)
    assert result.id == 1
    assert result.name == "John Updated"
    assert result.email == "john.updated@example.com"
    customer_service.customer_repository.find_by_id.assert_called_once_with(1)
    customer_service.customer_repository.update.assert_called_once()


def test_update_non_existing_customer(customer_service):
    # Arrange
    update_dto = CustomerUpdateDto(
        name="John Updated", email="john.updated@example.com")
    customer_service.customer_repository.find_by_id.return_value = None

    # Act
    result = customer_service.update(999, update_dto)

    # Assert
    assert result is None
    customer_service.customer_repository.find_by_id.assert_called_once_with(
        999)
    customer_service.customer_repository.update.assert_not_called()


def test_delete_customer(customer_service):
    # Arrange
    customer_id = 1

    # Act
    customer_service.delete(customer_id)

    # Assert
    customer_service.customer_repository.delete.assert_called_once_with(
        customer_id)


def test_find_all_customers(customer_service):
    # Arrange
    mock_customers = [
        Customer(id=1, name="John Doe", email="john@example.com"),
        Customer(id=2, name="Jane Doe", email="jane@example.com")
    ]
    customer_service.customer_repository.find_all.return_value = mock_customers

    # Act
    result = customer_service.find_all()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(customer, CustomerResponseDto)
               for customer in result)
    assert result[0].id == 1
    assert result[1].id == 2
    customer_service.customer_repository.find_all.assert_called_once()
