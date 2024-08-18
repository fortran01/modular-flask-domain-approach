# app/services/customer_service.py
from typing import List, Optional
from app.repositories.customer_repository import CustomerRepository
from app.repositories.loyalty_account_repository import (
    LoyaltyAccountRepository
)
from app.models.domain.customer import Customer
from app.models.domain.loyalty_account import LoyaltyAccount
from app.schemas.customer import (
    CustomerCreateDto,
    CustomerUpdateDto,
    CustomerResponseDto
)


class CustomerService:
    """Service layer for handling customer-related operations."""

    def __init__(
        self,
        customer_repository: CustomerRepository,
        loyalty_account_repository: LoyaltyAccountRepository
    ):
        """
        Initializes the CustomerService with required repositories.

        Args:
            customer_repository (CustomerRepository): Repository for
                customer data.
            loyalty_account_repository (LoyaltyAccountRepository): Repository
            for loyalty account data.
        """
        self.customer_repository: CustomerRepository = customer_repository
        self.loyalty_account_repository: LoyaltyAccountRepository = loyalty_account_repository  # noqa: E501

    def find_by_id(self, id: int) -> Optional[CustomerResponseDto]:
        """
        Finds a customer by their ID and returns their data.

        Args:
            id (int): The ID of the customer to find.

        Returns:
            Optional[CustomerResponseDto]: The customer's data,
            or None if not found.
        """
        customer: Optional[Customer] = self.customer_repository.find_by_id(id)
        if customer:
            return CustomerResponseDto(
                id=customer.id,
                name=customer.name,
                email=customer.email
            )
        return None

    def create(self, customer_dto: CustomerCreateDto) -> CustomerResponseDto:
        """
        Creates a new customer and their associated loyalty account.

        Args:
            customer_dto (CustomerCreateDto): Data transfer object
            containing customer data.

        Returns:
            CustomerResponseDto: The created customer's data.
        """
        customer: Customer = Customer(
            id=0,  # ID will be assigned by the database
            name=customer_dto.name,
            email=customer_dto.email
        )
        created_customer: Customer = self.customer_repository.create(customer)

        loyalty_account: LoyaltyAccount = LoyaltyAccount(
            id=0,  # ID will be assigned by the database
            customer_id=created_customer.id,
            points=0
        )
        self.loyalty_account_repository.create(loyalty_account)

        return CustomerResponseDto(
            id=created_customer.id,
            name=created_customer.name,
            email=created_customer.email
        )

    def update(self, id: int, customer_dto: CustomerUpdateDto) -> Optional[CustomerResponseDto]:  # noqa: E501
        """
        Updates an existing customer's data.

        Args:
            id (int): The ID of the customer to update.
            customer_dto (CustomerUpdateDto): Data transfer object containing
            updated customer data.

        Returns:
            Optional[CustomerResponseDto]: The updated customer's data,
            or None if not found.
        """
        customer: Optional[Customer] = self.customer_repository.find_by_id(id)
        if customer:
            if customer_dto.name:
                customer.name = customer_dto.name
            if customer_dto.email:
                customer.email = customer_dto.email
            updated_customer: Customer = self.customer_repository.update(
                customer)
            return CustomerResponseDto(
                id=updated_customer.id,
                name=updated_customer.name,
                email=updated_customer.email
            )
        return None

    def delete(self, id: int) -> None:
        """
        Deletes a customer by their ID.

        Args:
            id (int): The ID of the customer to delete.
        """
        self.customer_repository.delete(id)

    def find_all(self) -> List[CustomerResponseDto]:
        """
        Retrieves all customers and their data.

        Returns:
            List[CustomerResponseDto]: List of all customer data.
        """
        customers: List[Customer] = self.customer_repository.find_all()
        return [CustomerResponseDto(
            id=customer.id,
            name=customer.name,
            email=customer.email
        ) for customer in customers]
