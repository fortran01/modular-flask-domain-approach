# app/models/domain/point_transaction.py
from datetime import datetime
from typing import Optional
from app.models.domain.loyalty_account import LoyaltyAccount
from app.models.domain.product import Product


class PointTransaction:
    """
    Represents a point transaction in the domain model.

    This class encapsulates the core attributes and relationships
    of a point transaction, including its identification, associated
    loyalty account and product, points earned, and the transaction date.

    Attributes:
        id (int): The unique identifier for the point transaction.
        loyalty_account (LoyaltyAccount): The loyalty account associated
            with this transaction.
        product (Product): The product associated with this transaction.
        points_earned (int): The number of points earned in this transaction.
        transaction_date (datetime): The timestamp when the transaction
        occurred.
    """

    def __init__(
        self,
        id: int,
        loyalty_account: LoyaltyAccount,
        product: Product,
        points_earned: int,
        transaction_date: Optional[datetime] = None
    ):
        """
        Initializes a new PointTransaction instance.

        Args:
            id (int): The unique identifier for the point transaction.
            loyalty_account (LoyaltyAccount): The loyalty account associated
                with this transaction.
            product (Product): The product associated with this transaction.
            points_earned (int): The number of points earned
                in this transaction.
            transaction_date (Optional[datetime], optional): The timestamp when
                the transaction occurred. Defaults to None.
        """
        self.id: int = id
        self.loyalty_account: LoyaltyAccount = loyalty_account
        self.product: Product = product
        self.points_earned: int = points_earned
        self.transaction_date: datetime = transaction_date or datetime.utcnow()
