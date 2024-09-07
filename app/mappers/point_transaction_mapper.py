# app/mappers/point_transaction_mapper.py

from typing import Dict, Any, List
from datetime import datetime
from app.mappers.base_mapper import BaseMapper
from app.models.domain.point_transaction import PointTransaction
from app.models.database.point_transaction import PointTransactionTable
from app.schemas.point_transaction import PointTransactionResponseDto
from app.mappers.loyalty_account_mapper import LoyaltyAccountMapper
from app.mappers.product_mapper import ProductMapper


class PointTransactionMapper(BaseMapper[PointTransaction]):
    """
    Mapper for PointTransaction entity. Handles conversions between
    domain model, database model, and DTOs.
    """

    @classmethod
    def to_domain(cls, data: Dict[str, Any]) -> PointTransaction:
        """
        Convert dict to PointTransaction domain model instance.

        Args:
            data (Dict[str, Any]): Dict with point transaction data.

        Returns:
            PointTransaction: PointTransaction domain model.
        """
        return PointTransaction(
            id=data.get('id'),
            loyalty_account=LoyaltyAccountMapper.to_domain(
                data['loyalty_account']) if data.get('loyalty_account') else None,  # noqa: E501
            product=ProductMapper.to_domain(
                data['product']) if data.get('product') else None,
            points_earned=data['points_earned'],
            transaction_date=data['transaction_date']
        )

    @classmethod
    def to_dto(
            cls, domain_model: PointTransaction
    ) -> PointTransactionResponseDto:
        """
        Convert PointTransaction domain model to DTO.

        Args:
            domain_model (PointTransaction): PointTransaction model.

        Returns:
            PointTransactionResponseDto: DTO for the transaction.
        """
        return PointTransactionResponseDto(
            id=domain_model.id,
            loyalty_account_id=domain_model.loyalty_account.id if domain_model.loyalty_account else None,  # noqa: E501
            product_id=domain_model.product.id if domain_model.product else None,  # noqa: E501
            points_earned=domain_model.points_earned,
            transaction_date=domain_model.transaction_date
        )

    @classmethod
    def from_persistence(
            cls, db_model: PointTransactionTable
    ) -> PointTransaction:
        """
        Convert PointTransactionTable model to domain model.

        Args:
            db_model (PointTransactionTable): Database model instance.

        Returns:
            PointTransaction: PointTransaction domain model.
        """
        return PointTransaction(
            id=db_model.id,
            loyalty_account=LoyaltyAccountMapper.from_persistence(
                db_model.loyalty_account) if db_model.loyalty_account else None,  # noqa: E501
            product=ProductMapper.from_persistence(
                db_model.product) if db_model.product else None,
            points_earned=db_model.points_earned,
            transaction_date=db_model.transaction_date
        )

    @classmethod
    def to_persistence_model(
            cls, domain_model: PointTransaction
    ) -> PointTransactionTable:
        """
        Convert PointTransaction model to database model.

        Args:
            domain_model (PointTransaction): Domain model instance.

        Returns:
            PointTransactionTable: Database model.
        """
        return PointTransactionTable(
            id=domain_model.id,
            loyalty_account_id=domain_model.loyalty_account.id if domain_model.loyalty_account else None,  # noqa: E501
            product_id=domain_model.product.id if domain_model.product else None,  # noqa: E501
            points_earned=domain_model.points_earned,
            transaction_date=domain_model.transaction_date
        )

    @classmethod
    def map_domain_list(
            cls, transactions: List[PointTransaction]
    ) -> List[PointTransactionResponseDto]:
        """
        Map domain models to DTOs.

        Args:
            transactions (List[PointTransaction]): Domain models.

        Returns:
            List[PointTransactionResponseDto]: DTOs.
        """
        return [cls.to_dto(transaction) for transaction in transactions]

    @classmethod
    def create_new_transaction(
            cls, loyalty_account_id: int, product_id: int, points_earned: int
    ) -> PointTransaction:
        """
        Create new PointTransaction model.

        Args:
            loyalty_account_id (int): Loyalty account ID.
            product_id (int): Product ID.
            points_earned (int): Points earned.

        Returns:
            PointTransaction: New domain model.
        """
        return PointTransaction(
            id=None,  # ID will be assigned by the database
            loyalty_account=None,  # LoyaltyAccount set separately
            product=None,  # Product set separately
            points_earned=points_earned,
            transaction_date=datetime.utcnow()
        )
