# app/services/product_service.py
from typing import List, Optional
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.models.domain.product import Product
from app.schemas.product import (ProductCreateDto, ProductUpdateDto,
                                 ProductResponseDto)


class ProductService:
    """Service layer for managing product-related operations."""

    def __init__(self, product_repository: ProductRepository,
                 category_repository: CategoryRepository) -> None:
        """
        Initializes the ProductService with required repositories.

        Args:
            product_repository (ProductRepository): Repository for
                product data.
            category_repository (CategoryRepository): Repository for
                category data.
        """
        self.product_repository: ProductRepository = product_repository
        self.category_repository: CategoryRepository = category_repository

    def find_by_id(self, id: int) -> Optional[ProductResponseDto]:
        """
        Finds a product by its ID and returns its data.

        Args:
            id (int): The ID of the product to find.

        Returns:
            Optional[ProductResponseDto]: The product's data, or None
            if not found.
        """
        product: Optional[Product] = self.product_repository.find_by_id(id)
        if product:
            return ProductResponseDto(
                id=product.id,
                name=product.name,
                price=product.price,
                category_id=product.category_id,
                image_url=product.image_url
            )
        return None

    def create(self, product_dto: ProductCreateDto) -> ProductResponseDto:
        """
        Creates a new product and returns its data.

        Args:
            product_dto (ProductCreateDto): DTO containing product data.

        Returns:
            ProductResponseDto: The created product's data.

        Raises:
            ValueError: If the category does not exist.
        """
        category = self.category_repository.find_by_id(product_dto.category_id)
        if not category:
            raise ValueError("Category not found")

        product = Product(
            id=0,  # ID will be assigned by the database
            name=product_dto.name,
            price=product_dto.price,
            category_id=product_dto.category_id,
            image_url=product_dto.image_url
        )
        created_product: Product = self.product_repository.create(product)
        return ProductResponseDto(
            id=created_product.id,
            name=created_product.name,
            price=created_product.price,
            category_id=created_product.category_id,
            image_url=created_product.image_url
        )

    def update(self, id: int, product_dto: ProductUpdateDto) -> Optional[ProductResponseDto]:  # noqa: E501
        """
        Updates an existing product and returns its updated data.

        Args:
            id (int): The ID of the product to update.
            product_dto (ProductUpdateDto): DTO containing updated
            product data.

        Returns:
            Optional[ProductResponseDto]: The updated product's data,
              or None if not found.

        Raises:
            ValueError: If the new category does not exist.
        """
        product: Optional[Product] = self.product_repository.find_by_id(id)
        if product:
            if product_dto.name:
                product.name = product_dto.name
            if product_dto.price is not None:
                product.price = product_dto.price
            if product_dto.category_id:
                category = self.category_repository.find_by_id(
                    product_dto.category_id)
                if not category:
                    raise ValueError("Category not found")
                product.category_id = product_dto.category_id
            if product_dto.image_url:
                product.image_url = product_dto.image_url

            updated_product: Product = self.product_repository.update(product)
            return ProductResponseDto(
                id=updated_product.id,
                name=updated_product.name,
                price=updated_product.price,
                category_id=updated_product.category_id,
                image_url=updated_product.image_url
            )
        return None

    def delete(self, id: int) -> None:
        """
        Deletes a product by its ID.

        Args:
            id (int): The ID of the product to delete.
        """
        self.product_repository.delete(id)

    def find_all(self) -> List[ProductResponseDto]:
        """
        Retrieves all products and their data.

        Returns:
            List[ProductResponseDto]: List of all product data.
        """
        products: List[Product] = self.product_repository.find_all()
        return [ProductResponseDto(
            id=product.id,
            name=product.name,
            price=product.price,
            category_id=product.category_id,
            image_url=product.image_url
        ) for product in products]
