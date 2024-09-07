# app/tests/services/test_shopping_cart_service.py
import pytest
from unittest.mock import Mock
from app.services.shopping_cart_service import ShoppingCartService
from app.models.domain.shopping_cart import ShoppingCart
from app.models.database.shopping_cart import ShoppingCartTable
from app.schemas.product import ProductResponseDto


@pytest.fixture
def shopping_cart_service():
    mock_shopping_cart_repository = Mock()
    mock_product_repository = Mock()
    return ShoppingCartService(
        mock_shopping_cart_repository,
        mock_product_repository
    )


def test_get_or_create_cart_existing_cart(shopping_cart_service):
    # Arrange
    mock_cart = ShoppingCart(id=1, customer_id=123)
    shopping_cart_service.shopping_cart_repository.find_by_customer_id. \
        return_value = mock_cart

    # Act
    result = shopping_cart_service.get_or_create_cart(123)

    # Assert
    assert isinstance(result, ShoppingCart)
    assert result.id == 1
    assert result.customer_id == 123
    shopping_cart_service.shopping_cart_repository.find_by_customer_id. \
        assert_called_once_with(123)


def test_get_or_create_cart_no_existing_cart(shopping_cart_service):
    # Arrange
    shopping_cart_service.shopping_cart_repository.find_by_customer_id. \
        return_value = None
    shopping_cart_service.shopping_cart_repository.create.return_value = \
        ShoppingCart(id=2, customer_id=123)

    # Act
    result = shopping_cart_service.get_or_create_cart(123)

    # Assert
    assert isinstance(result, ShoppingCart)
    assert result.id == 2
    assert result.customer_id == 123
    shopping_cart_service.shopping_cart_repository.find_by_customer_id. \
        assert_called_once_with(123)
    shopping_cart_service.shopping_cart_repository.create.assert_called_once()


def test_clear_cart(shopping_cart_service):
    # Arrange
    mock_cart = ShoppingCart(id=1, customer_id=123)
    shopping_cart_service.get_or_create_cart = Mock(return_value=mock_cart)

    # Act
    shopping_cart_service.clear_cart(123)

    # Assert
    assert mock_cart.items == []
    shopping_cart_service.shopping_cart_repository.update.assert_called_once()
    cart_arg = shopping_cart_service.shopping_cart_repository.update.\
        call_args[0][0]
    assert isinstance(cart_arg, ShoppingCartTable)
    assert cart_arg.id == 1
    assert cart_arg.customer_id == 123
    shopping_cart_service.get_or_create_cart.assert_called_once_with(123)


def test_add_item(shopping_cart_service):
    # Arrange
    mock_cart = ShoppingCart(id=1, customer_id=123)
    mock_product = ProductResponseDto(
        id=1, name="Test Product", price=100, category_id=1,
        image_url="test.jpg")
    shopping_cart_service.get_or_create_cart = Mock(return_value=mock_cart)
    shopping_cart_service.product_repository.find_by_id = Mock(
        return_value=mock_product)

    # Act
    shopping_cart_service.add_item(123, 1, 2)

    # Assert
    assert len(mock_cart.items) == 1
    assert mock_cart.items[0].product == mock_product
    assert mock_cart.items[0].quantity == 2
    shopping_cart_service.shopping_cart_repository.update.assert_called_once()
    cart_arg = shopping_cart_service.shopping_cart_repository.\
        update.call_args[0][0]
    assert isinstance(cart_arg, ShoppingCartTable)
    assert cart_arg.id == 1
    assert cart_arg.customer_id == 123


def test_remove_item(shopping_cart_service):
    # Arrange
    mock_cart = ShoppingCart(id=1, customer_id=123)
    mock_cart.add_item(Mock(id=1), 2)  # Adding an item to be removed
    shopping_cart_service.get_or_create_cart = Mock(return_value=mock_cart)

    # Act
    shopping_cart_service.remove_item(123, 1)

    # Assert
    assert len(mock_cart.items) == 0
    shopping_cart_service.shopping_cart_repository.update.assert_called_once()
    cart_arg = shopping_cart_service.shopping_cart_repository.update.\
        call_args[0][0]
    assert isinstance(cart_arg, ShoppingCartTable)
    assert cart_arg.id == 1
    assert cart_arg.customer_id == 123
    shopping_cart_service.get_or_create_cart.assert_called_once_with(123)


def test_update_item_quantity(shopping_cart_service):
    # Arrange
    mock_cart = ShoppingCart(id=1, customer_id=123)
    mock_product = Mock(id=1)
    mock_cart.add_item(mock_product, 2)  # Adding an item to update
    shopping_cart_service.get_or_create_cart = Mock(return_value=mock_cart)

    # Act
    shopping_cart_service.update_item_quantity(123, 1, 5)

    # Assert
    assert mock_cart.items[0].quantity == 5
    shopping_cart_service.shopping_cart_repository.update.assert_called_once()
    cart_arg = shopping_cart_service.shopping_cart_repository.update.\
        call_args[0][0]
    assert isinstance(cart_arg, ShoppingCartTable)
    assert cart_arg.id == 1
    assert cart_arg.customer_id == 123
    shopping_cart_service.get_or_create_cart.assert_called_once_with(123)
