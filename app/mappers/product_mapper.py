# app/mappers/product_mapper.py

from typing import Dict, Any, List
from app.mappers.base_mapper import BaseMapper
from app.models.domain.product import Product
from app.models.database.product import ProductTable
from app.schemas.product import (
    ProductCreateDto,
    ProductUpdateDto,
    ProductResponseDto,
)


class ProductMapper(BaseMapper[Product]):
    """
    Mapper class for the Product entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> Product:
        """
        Convert a dictionary to a Product domain model instance.

        Args:
            data (Dict[str, Any]): The dictionary containing product data.

        Returns:
            Product: An instance of the Product domain model.
        """
        return Product(
            id=data.get('id'),
            name=data['name'],
            price=data['price'],
            category_id=data['category_id'],
            image_url=data.get('image_url')
        )

    @classmethod
    def to_dto(cls, domain_model: Product) -> ProductResponseDto:
        """
        Convert a Product domain model instance to a ProductResponseDto.

        Args:
            domain_model (Product): The Product domain model instance.

        Returns:
            ProductResponseDto: A DTO representing the product.
        """
        return ProductResponseDto(
            id=domain_model.id,
            name=domain_model.name,
            price=domain_model.price,
            category_id=domain_model.category_id,
            image_url=domain_model.image_url
        )

    @classmethod
    def to_persistence(cls, domain_model: Product) -> Dict[str, Any]:
        """
        Convert a Product domain model instance to a dictionary
        suitable for database persistence.

        Args:
            domain_model (Product): The Product domain model instance.

        Returns:
            Dict[str, Any]: A dictionary representing the product
                for persistence.
        """
        return {
            'id': domain_model.id,
            'name': domain_model.name,
            'price': domain_model.price,
            'category_id': domain_model.category_id,
            'image_url': domain_model.image_url
        }

    @classmethod
    def from_create_dto(cls, dto: ProductCreateDto) -> Product:
        """
        Create a Product domain model instance from a ProductCreateDto.

        Args:
            dto (ProductCreateDto): The DTO containing data for creating
            a product.

        Returns:
            Product: A new instance of the Product domain model.
        """
        return Product(
            id=None,  # ID will be assigned by the database
            name=dto.name,
            price=dto.price,
            category_id=dto.category_id,
            image_url=dto.image_url
        )

    @classmethod
    def from_update_dto(
        cls, dto: ProductUpdateDto, existing_product: Product
    ) -> Product:
        """
        Update an existing Product domain model instance from
        a ProductUpdateDto.

        Args:
            dto (ProductUpdateDto): The DTO containing data for updating
                a product.
            existing_product (Product): The existing Product domain model
                to update.

        Returns:
            Product: The updated Product domain model instance.
        """
        if dto.name is not None:
            existing_product.name = dto.name
        if dto.price is not None:
            existing_product.price = dto.price
        if dto.category_id is not None:
            existing_product.category_id = dto.category_id
        if dto.image_url is not None:
            existing_product.image_url = dto.image_url
        return existing_product

    @classmethod
    def from_persistence(cls, db_model: ProductTable) -> Product:
        """
        Convert a ProductTable database model to a Product domain model.

        Args:
            db_model (ProductTable): The database model instance.

        Returns:
            Product: An instance of the Product domain model.
        """
        return Product(
            id=db_model.id,
            name=db_model.name,
            price=db_model.price,
            category_id=db_model.category_id,
            image_url=db_model.image_url
        )

    @classmethod
    def to_persistence_model(cls, domain_model: Product) -> ProductTable:
        """
        Convert a Product domain model to a ProductTable database model.

        Args:
            domain_model (Product): The Product domain model instance.

        Returns:
            ProductTable: An instance of the ProductTable database model.
        """
        return ProductTable(
            id=domain_model.id,
            name=domain_model.name,
            price=domain_model.price,
            category_id=domain_model.category_id,
            image_url=domain_model.image_url
        )

    @classmethod
    def map_domain_list(
        cls, products: List[Product]
    ) -> List[ProductResponseDto]:
        """
        Map a list of Product domain models to a list of ProductResponseDto.

        Args:
            products (List[Product]): A list of Product domain models.

        Returns:
            List[ProductResponseDto]: A list of ProductResponseDto instances.
        """
        return [cls.to_dto(product) for product in products]
