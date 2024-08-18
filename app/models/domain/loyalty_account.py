# app/models/domain/loyalty_account.py
from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models.domain.point_transaction import PointTransaction


class LoyaltyAccount:
    """
    Represents a loyalty account in the domain model.

    This class encapsulates the core attributes and behaviors
    of a loyalty account, including its identification, associated customer,
    point balance, and transactions.

    Attributes:
        id (int): The unique identifier for the loyalty account.
        customer_id (int): The identifier of the customer associated
            with this account.
        points (int): The current point balance of the account.
        transactions (List[PointTransaction]): A list of point transactions
        associated with this account.
    """

    def __init__(
        self,
        id: int,
        customer_id: int,
        points: int,
        transactions: Optional[List[PointTransaction]] = None
    ) -> None:
        """
        Initializes a new LoyaltyAccount instance.

        Args:
            id (int): The unique identifier for the loyalty account.
            customer_id (int): The identifier of the customer associated
            with this account.
            points (int): The initial point balance of the account.
            transactions (Optional[List[PointTransaction]], optional):
            A list of point transactions
                associated with this account. Defaults to None.
        """
        self.id: int = id
        self.customer_id: int = customer_id
        self.points: int = points
        self.transactions: List[PointTransaction] = transactions or []

    def add_points(self, points: int) -> None:
        """
        Adds points to the loyalty account.

        Args:
            points (int): The number of points to add to the account.
        """
        self.points += points

    def deduct_points(self, points: int) -> bool:
        """
        Attempts to deduct points from the loyalty account.

        Args:
            points (int): The number of points to deduct from the account.

        Returns:
            bool: True if the deduction was successful, False if there
            were insufficient points.
        """
        if self.points >= points:
            self.points -= points
            return True
        return False
