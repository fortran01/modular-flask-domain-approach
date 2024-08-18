# app/repositories/base_repository.py
from typing import TypeVar, Generic, List, Optional
from app import db

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    A generic base repository that provides CRUD operations for a given model.

    Attributes:
        model (T): The database model the repository will manage.
    """

    def __init__(self, model: T):
        """
        Initializes the BaseRepository with the specified model.

        Args:
            model (T): The model class for database operations.
        """
        self.model = model

    def find_by_id(self, id: int) -> Optional[T]:
        """
        Finds an entity by its ID.

        Args:
            id (int): The ID of the entity to find.

        Returns:
            Optional[T]: The found entity or None if not found.
        """
        return db.session.query(self.model).filter(self.model.id == id).first()

    def find_all(self) -> List[T]:
        """
        Finds all entities of the model.

        Returns:
            List[T]: A list of all entities.
        """
        return db.session.query(self.model).all()

    def create(self, entity: T) -> T:
        """
        Creates a new entity in the database.

        Args:
            entity (T): The entity to create.

        Returns:
            T: The created entity.
        """
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity: T) -> T:
        """
        Updates an existing entity in the database.

        Args:
            entity (T): The entity to update.

        Returns:
            T: The updated entity.
        """
        db.session.merge(entity)
        db.session.commit()
        return entity

    def delete(self, id: int) -> None:
        """
        Deletes an entity by its ID.

        Args:
            id (int): The ID of the entity to delete.
        """
        entity = self.find_by_id(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()
