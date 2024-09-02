# app/mappers/loyalty_account_mapper.py

from typing import Dict, Any, List
from app.mappers.base_mapper import BaseMapper
from app.models.domain.loyalty_account import LoyaltyAccount
from app.models.database.loyalty_account import LoyaltyAccountTable
from app.schemas.points import PointsDto


class LoyaltyAccountMapper(BaseMapper[LoyaltyAccount]):
    """
    Mapper class for the LoyaltyAccount entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> LoyaltyAccount:
        """
        Convert a dictionary to a LoyaltyAccount domain model instance.

        Args:
            data (Dict[str, Any]): The dictionary containing
                loyalty account data.

        Returns:
            LoyaltyAccount: An instance of the LoyaltyAccount domain model.
        """
        return LoyaltyAccount(
            id=data.get('id'),
            customer_id=data['customer_id'],
            points=data['points'],
            transactions=data.get('transactions', [])
        )

    @classmethod
    def to_dto(cls, domain_model: LoyaltyAccount) -> PointsDto:
        """
        Convert a LoyaltyAccount domain model instance to a PointsDto.

        Args:
            domain_model (LoyaltyAccount): The LoyaltyAccount domain model
                instance.

        Returns:
            PointsDto: A DTO representing the loyalty account points.
        """
        return PointsDto(points=domain_model.points)

    @classmethod
    def to_persistence(cls, domain_model: LoyaltyAccount) -> Dict[str, Any]:
        """
        Convert a LoyaltyAccount domain model instance to a dictionary
        suitable for database persistence.

        Args:
            domain_model (LoyaltyAccount): The LoyaltyAccount domain
                model instance.

        Returns:
            Dict[str, Any]: A dictionary representing the loyalty account
            for persistence.
        """
        return {
            'id': domain_model.id,
            'customer_id': domain_model.customer_id,
            'points': domain_model.points
        }

    @classmethod
    def from_persistence(cls, db_model: LoyaltyAccountTable) -> LoyaltyAccount:
        """
        Convert a LoyaltyAccountTable database model to a LoyaltyAccount
            domain model.

        Args:
            db_model (LoyaltyAccountTable): The database model instance.

        Returns:
            LoyaltyAccount: An instance of the LoyaltyAccount domain model.
        """
        return LoyaltyAccount(
            id=db_model.id,
            customer_id=db_model.customer_id,
            points=db_model.points,
            transactions=[]  # Transactions would typically be loaded separately or lazily # noqa: E501
        )

    @classmethod
    def to_persistence_model(cls, domain_model: LoyaltyAccount) -> LoyaltyAccountTable:  # noqa: E501
        """
        Convert a LoyaltyAccount domain model to a LoyaltyAccountTable
        database model.

        Args:
            domain_model (LoyaltyAccount): The LoyaltyAccount domain model
                instance.

        Returns:
            LoyaltyAccountTable: An instance of the LoyaltyAccountTable
              database model.
        """
        return LoyaltyAccountTable(
            id=domain_model.id,
            customer_id=domain_model.customer_id,
            points=domain_model.points
        )

    @classmethod
    def map_domain_list(cls, loyalty_accounts: List[LoyaltyAccount]) -> List[PointsDto]:  # noqa: E501
        """
        Map a list of LoyaltyAccount domain models to a list of PointsDto.

        Args:
            loyalty_accounts (List[LoyaltyAccount]): A list of LoyaltyAccount
                domain models.

        Returns:
            List[PointsDto]: A list of PointsDto instances.
        """
        return [cls.to_dto(account) for account in loyalty_accounts]

    @classmethod
    def create_new_account(cls, customer_id: int) -> LoyaltyAccount:
        """
        Create a new LoyaltyAccount domain model instance for a new customer.

        Args:
            customer_id (int): The ID of the customer for whom
                to create the account.

        Returns:
            LoyaltyAccount: A new instance of the LoyaltyAccount domain model.
        """
        return LoyaltyAccount(
            id=None,  # ID will be assigned by the database
            customer_id=customer_id,
            points=0,
            transactions=[]
        )
