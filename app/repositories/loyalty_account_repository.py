# app/repositories/loyalty_account_repository.py
from app.repositories.base_repository import BaseRepository
from app.models.database.loyalty_account import LoyaltyAccountTable
from app.models.database.point_transaction import PointTransactionTable
from app.models.database.product import ProductTable
from app.models.database.point_earning_rule import PointEarningRuleTable
from app.models.database.shopping_cart import ShoppingCartTable
from datetime import datetime
from typing import Optional, Dict
from app import db


class LoyaltyAccountRepository(BaseRepository[LoyaltyAccountTable]):
    def __init__(self):
        """Initializes the repository for LoyaltyAccount data."""
        super().__init__(LoyaltyAccountTable)

    def find_by_customer_id(self, customer_id: int) -> Optional[LoyaltyAccountTable]:  # noqa: E501
        """Finds a loyalty account by customer ID.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            Optional[LoyaltyAccountTable]: The found loyalty account or None.
        """
        return db.session.query(LoyaltyAccountTable).filter(
            LoyaltyAccountTable.customer_id == customer_id).first()

    def add_points(self, loyalty_account_id: int, points: int) -> LoyaltyAccountTable:  # noqa: E501
        """Adds points to a loyalty account.

        Args:
            loyalty_account_id (int): The ID of the loyalty account.
            points (int): Number of points to add.

        Returns:
            LoyaltyAccountTable: Updated loyalty account.
        """
        loyalty_account = self.find_by_id(loyalty_account_id)
        if loyalty_account:
            loyalty_account.points += points
            db.session.commit()
        return loyalty_account

    def checkout_transaction(self, customer_id: int) -> Dict[str, any]:
        """Processes a checkout transaction, calculating loyalty points.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            Dict[str, any]: A dictionary with transaction details.
        """
        result = {
            'totalPointsEarned': 0,
            'invalidProducts': [],
            'productsMissingCategory': [],
            'pointEarningRulesMissing': []
        }

        loyalty_account = self.find_by_customer_id(customer_id)
        if not loyalty_account:
            raise ValueError("Loyalty account not found")

        cart = db.session.query(ShoppingCartTable).filter(
            ShoppingCartTable.customer_id == customer_id).first()
        if not cart or not cart.items:
            raise ValueError("Shopping cart is empty or not found")

        current_date = datetime.utcnow().date()

        for item in cart.items:
            product = db.session.query(ProductTable).get(item.product_id)
            if not product:
                result['invalidProducts'].append(item.product_id)
                continue

            if not product.category:
                result['productsMissingCategory'].append(product.id)
                continue

            rule = db.session.query(PointEarningRuleTable).filter(
                PointEarningRuleTable.category_id == product.category_id,
                PointEarningRuleTable.start_date <= current_date,
                PointEarningRuleTable.end_date.is_(None) |
                PointEarningRuleTable.end_date >= current_date
            ).first()

            if not rule:
                result['pointEarningRulesMissing'].append(product.id)
                continue

            points_earned = int(
                product.price * rule.points_per_dollar) * item.quantity
            result['totalPointsEarned'] += points_earned

            transaction = PointTransactionTable(
                loyalty_account_id=loyalty_account.id,
                product_id=product.id,
                points_earned=points_earned,
                transaction_date=datetime.utcnow()
            )
            db.session.add(transaction)

        loyalty_account.points += result['totalPointsEarned']
        db.session.commit()

        return result
