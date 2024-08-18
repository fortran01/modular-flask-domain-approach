# app/tests/services/test_product_service.py
import pytest
from unittest.mock import Mock
from app.services.product_service import ProductService
from app.models.domain.product import Product
from app.models.domain.category import Category
from app.schemas.product import (
    ProductCreateDto,
    ProductUpdateDto,
    ProductResponseDto
)


@pytest.fixture
def product_service():
    mock_product_repository = Mock()
    mock_category_repository = Mock()
    return ProductService(
        mock_product_repository,
        mock_category_repository
    )


def test_find_by_id_existing_product(product_service):
    # Arrange
    mock_product = Product(
        id=1,
        name="Widget",
        price=19.99,
        category_id=1,
        image_url="http://example.com/widget.jpg"
    )
    product_service.product_repository.find_by_id.return_value = mock_product

    # Act
    result = product_service.find_by_id(1)

    # Assert
    assert isinstance(result, ProductResponseDto)
    assert result.id == 1
    assert result.name == "Widget"
    assert result.price == 19.99
    assert result.category_id == 1
    assert result.image_url == "http://example.com/widget.jpg"
    product_service.product_repository.find_by_id.assert_called_once_with(1)


def test_find_by_id_non_existing_product(product_service):
    # Arrange
    product_service.product_repository.find_by_id.return_value = None

    # Act
    result = product_service.find_by_id(999)

    # Assert
    assert result is None
    product_service.product_repository.find_by_id.assert_called_once_with(999)


def test_create_product_with_existing_category(product_service):
    # Arrange
    create_dto = ProductCreateDto(
        name="New Widget",
        price=29.99,
        category_id=2,
        image_url="http://example.com/new_widget.jpg"
    )
    mock_category = Category(id=2, name="Gadgets")
    product_service.category_repository.find_by_id.return_value = mock_category
    mock_product = Product(
        id=2,
        name="New Widget",
        price=29.99,
        category_id=2,
        image_url="http://example.com/new_widget.jpg"
    )
    product_service.product_repository.create.return_value = mock_product

    # Act
    result = product_service.create(create_dto)

    # Assert
    assert isinstance(result, ProductResponseDto)
    assert result.id == 2
    assert result.name == "New Widget"
    assert result.price == 29.99
    assert result.category_id == 2
    assert result.image_url == "http://example.com/new_widget.jpg"
    product_service.category_repository.find_by_id.assert_called_once_with(2)
    product_service.product_repository.create.assert_called_once()


def test_create_product_with_non_existing_category(product_service):
    # Arrange
    create_dto = ProductCreateDto(
        name="New Widget",
        price=29.99,
        category_id=999,
        image_url="http://example.com/new_widget.jpg"
    )
    product_service.category_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Category not found"):
        product_service.create(create_dto)
    product_service.category_repository.find_by_id.assert_called_once_with(999)


def test_update_existing_product(product_service):
    # Arrange
    update_dto = ProductUpdateDto(
        name="Updated Widget",
        price=39.99,
        category_id=1,
        image_url="http://example.com/updated_widget.jpg"
    )
    mock_product = Product(
        id=1,
        name="Widget",
        price=19.99,
        category_id=1,
        image_url="http://example.com/widget.jpg"
    )
    product_service.product_repository.find_by_id.return_value = mock_product
    mock_category = Category(id=1, name="Gadgets")
    product_service.category_repository.find_by_id.return_value = mock_category
    updated_product = Product(
        id=1,
        name="Updated Widget",
        price=39.99,
        category_id=1,
        image_url="http://example.com/updated_widget.jpg"
    )
    product_service.product_repository.update.return_value = updated_product

    # Act
    result = product_service.update(1, update_dto)

    # Assert
    assert isinstance(result, ProductResponseDto)
    assert result.id == 1
    assert result.name == "Updated Widget"
    assert result.price == 39.99
    assert result.category_id == 1
    assert result.image_url == "http://example.com/updated_widget.jpg"
    product_service.product_repository.find_by_id.assert_called_once_with(1)
    product_service.category_repository.find_by_id.assert_called_once_with(1)
    product_service.product_repository.update.assert_called_once()


def test_update_non_existing_product(product_service):
    # Arrange
    update_dto = ProductUpdateDto(
        name="Updated Widget",
        price=39.99,
        category_id=1,
        image_url="http://example.com/updated_widget.jpg"
    )
    product_service.product_repository.find_by_id.return_value = None

    # Act
    result = product_service.update(999, update_dto)

    # Assert
    assert result is None
    product_service.product_repository.find_by_id.assert_called_once_with(999)


def test_delete_product(product_service):
    # Arrange
    product_id = 1

    # Act
    product_service.delete(product_id)

    # Assert
    product_service.product_repository.delete.assert_called_once_with(
        product_id)


def test_find_all_products(product_service):
    # Arrange
    mock_products = [
        Product(id=1, name="Widget", price=19.99, category_id=1,
                image_url="http://example.com/widget.jpg"),
        Product(id=2, name="Gadget", price=29.99, category_id=2,
                image_url="http://example.com/gadget.jpg")
    ]
    product_service.product_repository.find_all.return_value = mock_products

    # Act
    result = product_service.find_all()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(product, ProductResponseDto) for product in result)
    assert result[0].id == 1
    assert result[1].id == 2
    product_service.product_repository.find_all.assert_called_once()
