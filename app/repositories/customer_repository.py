# app/repositories/customer_repository.py
from typing import Optional
from app.repositories.base_repository import BaseRepository
from app.models.database.customer import CustomerTable
from app import db


class CustomerRepository(BaseRepository[CustomerTable]):
    def __init__(self):
        """
        Initializes the CustomerRepository with the CustomerTable model.
        """
        super().__init__(CustomerTable)

    def find_by_email(self, email: str) -> Optional[CustomerTable]:
        """
        Retrieves a customer by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            Optional[CustomerTable]: The found customer or None if not found.
        """
        return db.session.query(CustomerTable).filter(
            CustomerTable.email == email).first()
