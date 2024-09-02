# app/repositories/customer_repository.py

from typing import Optional, List
from app.repositories.base_repository import BaseRepository
from app.models.database.customer import CustomerTable
from app.models.domain.customer import Customer
from app.mappers.customer_mapper import CustomerMapper
from app import db
import logging

logger = logging.getLogger(__name__)


class CustomerRepository(BaseRepository[CustomerTable]):
    def __init__(self):
        """
        Initializes the CustomerRepository with the CustomerTable model.
        """
        super().__init__(CustomerTable)

    def find_by_id(self, id: int) -> Optional[Customer]:
        """
        Retrieves a customer by their ID.

        Args:
            id (int): The ID of the customer to find.

        Returns:
            Optional[Customer]: The found customer or None if not found.
        """
        customer_table: Optional[CustomerTable] = super().find_by_id(id)
        return (
            CustomerMapper.from_persistence(customer_table)
            if customer_table
            else None
        )

    def find_by_email(self, email: str) -> Optional[Customer]:
        """
        Retrieves a customer by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            Optional[Customer]: The found customer or None if not found.
        """
        customer_table = db.session.query(CustomerTable).filter(
            CustomerTable.email == email).first()
        return (
            CustomerMapper.to_domain(customer_table)
            if customer_table
            else None
        )

    def find_all(self) -> List[Customer]:
        """
        Retrieves all customers.

        Returns:
            List[Customer]: A list of all Customer objects.
        """
        customer_tables = super().find_all()
        return [
            CustomerMapper.to_domain(customer)
            for customer in customer_tables
        ]

    def create(self, customer: Customer) -> Customer:
        """
        Creates a new customer.

        Args:
            customer (Customer): The customer object to create.

        Returns:
            Customer: The created Customer object.
        """
        customer_table: CustomerTable = CustomerMapper.to_persistence_model(
            customer)
        created_customer: CustomerTable = super().create(customer_table)
        return CustomerMapper.from_persistence(created_customer)

    def update(self, customer: Customer) -> Customer:
        """
        Updates an existing customer.

        Args:
            customer (Customer): The customer object to update.

        Returns:
            Customer: The updated Customer object.
        """
        customer_table = CustomerMapper.to_persistence_model(customer)
        updated_customer = super().update(customer_table)
        return CustomerMapper.from_persistence(updated_customer)

    def delete(self, id: int) -> None:
        """
        Deletes a customer by their ID after verifying their existence.

        Args:
            id (int): The ID of the customer to delete.
        """
        customer = self.find_by_id(id)
        if customer:
            try:
                super().delete(id)
            except Exception as e:
                logger.error(f"Error deleting customer: {e}")
                raise e
        else:
            logger.error(f"Customer with ID {id} not found.")
            raise ValueError(f"Customer with ID {id} not found.")
