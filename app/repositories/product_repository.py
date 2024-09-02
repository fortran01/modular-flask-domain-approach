# app/repositories/product_repository.py
from typing import List, Optional
from app.repositories.base_repository import BaseRepository
from app.models.database.product import ProductTable
from app.models.domain.product import Product
from app.mappers.product_mapper import ProductMapper
from app import db


class ProductRepository(BaseRepository[ProductTable]):
    def __init__(self):
        """
        Initializes the ProductRepository with the ProductTable model.
        """
        super().__init__(ProductTable)

    def find_by_id(self, id: int) -> Optional[Product]:
        """
        Retrieves a product by its ID.

        Args:
            id (int): The ID of the product to find.

        Returns:
            Optional[Product]: The found product or None if not found.
        """
        product_table = super().find_by_id(id)
        return (
            ProductMapper.to_domain(product_table)
            if product_table
            else None
        )

    def find_all(self) -> List[Product]:
        """
        Retrieves all products.

        Returns:
            List[Product]: A list of all Product objects.
        """
        product_tables = super().find_all()
        return [ProductMapper.to_domain(product) for product in product_tables]

    def find_by_category(self, category_id: int) -> List[Product]:
        """
        Retrieves products by their category ID.

        Args:
            category_id (int): The ID of the category to filter products by.

        Returns:
            List[Product]: A list of products in the specified category.
        """
        product_tables = db.session.query(ProductTable).filter(
            ProductTable.category_id == category_id).all()
        return [ProductMapper.to_domain(product) for product in product_tables]

    def create(self, product: Product) -> Product:
        """
        Creates a new product in the repository.

        Args:
            product (Product): The Product object to create.

        Returns:
            Product: The created Product object.
        """
        product_table = ProductMapper.to_persistence(product)
        created_product = super().create(product_table)
        return ProductMapper.to_domain(created_product)

    def update(self, product: Product) -> Product:
        """
        Updates an existing product in the repository.

        Args:
            product (Product): The Product object to update.

        Returns:
            Product: The updated Product object.
        """
        product_table = ProductMapper.to_persistence(product)
        updated_product = super().update(product_table)
        return ProductMapper.to_domain(updated_product)

    def delete(self, id: int) -> None:
        """
        Deletes a product by its ID.

        Args:
            id (int): The ID of the product to delete.
        """
        super().delete(id)
