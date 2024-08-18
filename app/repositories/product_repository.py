# app/repositories/product_repository.py
from typing import List
from app.repositories.base_repository import BaseRepository
from app.models.database.product import ProductTable
from app import db


class ProductRepository(BaseRepository[ProductTable]):
    def __init__(self):
        """
        Initializes the ProductRepository with the ProductTable model.
        """
        super().__init__(ProductTable)

    def find_by_category(self, category_id: int) -> List[ProductTable]:
        """
        Retrieves products by their category ID.

        Args:
            category_id (int): The ID of the category to filter products by.

        Returns:
            List[ProductTable]: A list of products in the specified category.
        """
        return db.session.query(ProductTable).filter(
            ProductTable.category_id == category_id).all()
