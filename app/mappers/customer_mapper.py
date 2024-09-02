# app/mappers/customer_mapper.py

from typing import Dict, Any, List
from app.mappers.base_mapper import BaseMapper
from app.models.domain.customer import Customer
from app.models.database.customer import CustomerTable
from app.schemas.customer import (
    CustomerCreateDto,
    CustomerUpdateDto,
    CustomerResponseDto
)
from app.mappers.loyalty_account_mapper import LoyaltyAccountMapper
import logging

logger = logging.getLogger(__name__)


class CustomerMapper(BaseMapper[Customer]):
    """
    Mapper class for the Customer entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> Customer:
        """
        Convert a dictionary to a Customer domain model instance.

        Args:
            data (Dict[str, Any]): The dictionary containing customer data.

        Returns:
            Customer: An instance of the Customer domain model.
        """
        return Customer(
            id=data.get('id'),
            name=data['name'],
            email=data['email'],
            loyalty_account=LoyaltyAccountMapper.to_domain(
                data['loyalty_account']) if data.get('loyalty_account') else None,  # noqa: E501
            shopping_carts=data.get('shopping_carts', [])
        )

    @classmethod
    def to_dto(cls, domain_model: Customer) -> CustomerResponseDto:
        """
        Convert a Customer domain model instance to a CustomerResponseDto.

        Args:
            domain_model (Customer): The Customer domain model instance.

        Returns:
            CustomerResponseDto: A DTO representing the customer.
        """
        return CustomerResponseDto(
            id=domain_model.id,
            name=domain_model.name,
            email=domain_model.email
        )

    # @classmethod
    # def to_persistence(cls, domain_model: Customer) -> Dict[str, Any]:
    #     """
    #     Convert a Customer domain model instance to a dictionary
    #     suitable for database persistence.

    #     Args:
    #         domain_model (Customer): The Customer domain model instance.

    #     Returns:
    #         Dict[str, Any]: A dictionary representing the customer
    #         for persistence.
    #     """
    #     return {
    #         'id': domain_model.id,
    #         'name': domain_model.name,
    #         'email': domain_model.email
    #     }

    @classmethod
    def from_create_dto(cls, dto: CustomerCreateDto) -> Customer:
        """
        Create a Customer domain model instance from a CustomerCreateDto.

        Args:
            dto (CustomerCreateDto): The DTO containing data
            for creating a customer.

        Returns:
            Customer: A new instance of the Customer domain model.
        """
        return Customer(
            id=None,  # ID will be assigned by the database
            name=dto.name,
            email=dto.email,
            loyalty_account=None,  # Loyalty account will be created separately
            shopping_carts=[]
        )

    @classmethod
    def from_update_dto(cls, dto: CustomerUpdateDto, existing_customer: Customer) -> Customer:  # noqa: E501
        """
        Update an existing Customer domain model instance
        from a CustomerUpdateDto.

        Args:
            dto (CustomerUpdateDto): The DTO containing data for updating
                a customer.
            existing_customer (Customer): The existing Customer domain model
                to update.

        Returns:
            Customer: The updated Customer domain model instance.
        """
        if dto.name is not None:
            existing_customer.name = dto.name
        if dto.email is not None:
            existing_customer.email = dto.email
        return existing_customer

    @classmethod
    def from_persistence(cls, db_model: CustomerTable) -> Customer:
        """
        Convert a CustomerTable database model to a Customer domain model.

        Args:
            db_model (CustomerTable): The database model instance.

        Returns:
            Customer: An instance of the Customer domain model.
        """
        return Customer(
            id=db_model.id,
            name=db_model.name,
            email=db_model.email,
            loyalty_account=LoyaltyAccountMapper.from_persistence(
                db_model.loyalty_account) if db_model.loyalty_account else None,  # noqa: E501
            shopping_carts=[]  # Shopping carts would typically be loaded separately or lazily # noqa: E501
        )

    @classmethod
    def to_persistence_model(cls, domain_model: Customer) -> CustomerTable:
        """
        Convert a Customer domain model to a CustomerTable database model.

        Args:
            domain_model (Customer): The Customer domain model instance.

        Returns:
            CustomerTable: An instance of the CustomerTable database model.
        """
        return CustomerTable(
            id=domain_model.id,
            name=domain_model.name,
            email=domain_model.email
        )

    @classmethod
    def map_domain_list(cls, customers: List[Customer]) -> List[CustomerResponseDto]:  # noqa: E501
        """
        Map a list of Customer domain models to a list of CustomerResponseDto.

        Args:
            customers (List[Customer]): A list of Customer domain models.

        Returns:
            List[CustomerResponseDto]: A list of CustomerResponseDto instances.
        """
        return [cls.to_dto(customer) for customer in customers]
