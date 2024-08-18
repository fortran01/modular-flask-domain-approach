# app/repositories/category_repository.py
from app.repositories.base_repository import BaseRepository
from app.models.database.category import CategoryTable


class CategoryRepository(BaseRepository[CategoryTable]):
    def __init__(self) -> None:
        """
        Initializes the CategoryRepository with the CategoryTable model.
        """
        super().__init__(CategoryTable)
