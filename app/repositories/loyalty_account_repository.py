# app/repositories/loyalty_account_repository.py
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from app.repositories.base_repository import BaseRepository
from app.models.database.loyalty_account import LoyaltyAccountTable
from app.models.database.point_transaction import PointTransactionTable
from app.models.database.product import ProductTable
from app.models.database.point_earning_rule import PointEarningRuleTable
from app.models.database.shopping_cart import ShoppingCartTable
from app.models.domain.loyalty_account import LoyaltyAccount
from app.mappers.loyalty_account_mapper import LoyaltyAccountMapper
from app.mappers.product_mapper import ProductMapper
from app import db
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class LoyaltyAccountRepository(BaseRepository[LoyaltyAccountTable]):
    def __init__(self):
        """
        Initializes the LoyaltyAccountRepository with the
        LoyaltyAccountTable model.
        """
        super().__init__(LoyaltyAccountTable)

    def find_by_id(self, id: int) -> Optional[LoyaltyAccount]:
        """
        Finds a loyalty account by its ID.

        Args:
            id (int): The unique identifier of the loyalty account.

        Returns:
            Optional[LoyaltyAccount]: The found loyalty account or None
                if not found.
        """
        loyalty_account_table = super().find_by_id(id)
        return (
            LoyaltyAccountMapper.to_domain(loyalty_account_table)
            if loyalty_account_table
            else None
        )

    def find_by_customer_id(
        self, customer_id: int
    ) -> Optional[LoyaltyAccount]:
        """
        Finds a loyalty account by customer ID.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            Optional[LoyaltyAccount]: The found loyalty account or None
                if not found.
        """
        loyalty_account_table = db.session.query(LoyaltyAccountTable).filter(
            LoyaltyAccountTable.customer_id == customer_id).first()
        return (
            LoyaltyAccountMapper.from_persistence(loyalty_account_table)
            if loyalty_account_table
            else None
        )

    def create(self, loyalty_account: LoyaltyAccount) -> LoyaltyAccount:
        """
        Creates a new loyalty account.

        Args:
            loyalty_account (LoyaltyAccount): The loyalty account object
            to create.

        Returns:
            LoyaltyAccount: The created LoyaltyAccount object.
        """
        loyalty_account_table: LoyaltyAccountTable = (
            LoyaltyAccountMapper.to_persistence_model(loyalty_account))
        created_account: LoyaltyAccountTable = super().create(
            loyalty_account_table)
        return LoyaltyAccountMapper.from_persistence(created_account)

    def update(self, loyalty_account: LoyaltyAccount) -> LoyaltyAccount:
        """
        Updates an existing loyalty account.

        Args:
            loyalty_account (LoyaltyAccount): The loyalty account object
            to update.

        Returns:
            LoyaltyAccount: The updated LoyaltyAccount object.
        """
        loyalty_account_table: LoyaltyAccountTable = (
            LoyaltyAccountMapper.to_persistence_model(loyalty_account))
        updated_account: LoyaltyAccountTable = super().update(
            loyalty_account_table)
        return LoyaltyAccountMapper.from_persistence(updated_account)

    def add_points(
        self, loyalty_account_id: int, points: int
    ) -> LoyaltyAccount:
        """
        Adds points to a loyalty account.

        Args:
            loyalty_account_id (int): The ID of the loyalty account.
            points (int): Number of points to add.

        Returns:
            LoyaltyAccount: Updated loyalty account.
        """
        loyalty_account = self.find_by_id(loyalty_account_id)
        if loyalty_account:
            loyalty_account.points += points
            return self.update(loyalty_account)
        return None

    def checkout_transaction(self, customer_id: int) -> Dict[str, Any]:
        """
        Processes a checkout transaction, calculating loyalty points.
        This method is executed within an atomic database transaction
        to ensure data consistency across multiple operations.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            Dict[str, Any]: A dictionary with transaction details.
        """
        result = {
            'totalPointsEarned': 0,
            'invalidProducts': [],
            'productsMissingCategory': [],
            'pointEarningRulesMissing': []
        }

        try:
            with db.session.begin():
                loyalty_account_table = self.find_by_customer_id(customer_id)
                loyalty_account = LoyaltyAccountMapper.from_persistence(
                    loyalty_account_table)
                if not loyalty_account:
                    raise ValueError("Loyalty account not found")

                cart = db.session.query(ShoppingCartTable).filter(
                    ShoppingCartTable.customer_id == customer_id).first()
                if not cart or not cart.items:
                    raise ValueError("Shopping cart is empty or not found")

                current_date = datetime.now(timezone.utc).date()

                for item in cart.items:
                    product_table = db.session.query(
                        ProductTable).get(item.product_id)
                    if not product_table:
                        result['invalidProducts'].append(item.product_id)
                        continue

                    product = ProductMapper.from_persistence(product_table)

                    if not product.category_id:
                        result['productsMissingCategory'].append(product.id)
                        continue

                    rule = db.session.query(PointEarningRuleTable).filter(
                        PointEarningRuleTable.category_id == product.category_id,  # noqa: E501
                        PointEarningRuleTable.start_date <= current_date,
                        db.or_(
                            PointEarningRuleTable.end_date.is_(None),
                            PointEarningRuleTable.end_date >= current_date
                        )
                    ).first()

                    if not rule:
                        result['pointEarningRulesMissing'].append(product.id)
                        continue

                    points_earned = int(
                        product.price * rule.points_per_dollar * item.quantity
                    )
                    logger.debug(f"Points earned: {points_earned}")
                    result['totalPointsEarned'] += points_earned
                    logger.debug(f"Total points earned: {
                                 result['totalPointsEarned']}")

                    transaction: PointTransactionTable = PointTransactionTable(
                        loyalty_account_id=loyalty_account.id,
                        product_id=product.id,
                        points_earned=points_earned,
                        transaction_date=datetime.now(timezone.utc)
                    )
                    db.session.add(transaction)

                loyalty_account.points += result['totalPointsEarned']
                loyalty_account_table: LoyaltyAccountTable = (
                    LoyaltyAccountMapper.to_persistence_model(loyalty_account))
                self.update(loyalty_account_table)

            # The commit is automatically done if no exception is raised
            return result
        except SQLAlchemyError as e:
            # Log the error
            logger.error(f"Error during checkout transaction: {str(e)}")
            # The transaction is automatically rolled back
            raise
