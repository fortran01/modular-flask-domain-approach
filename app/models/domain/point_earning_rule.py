# app/models/domain/point_earning_rule.py
from datetime import date
from typing import Optional
from app.models.domain.category import Category


class PointEarningRule:
    """
    Represents a point earning rule in the domain model.

    This class encapsulates the core attributes and behaviors of a point
    earning rule, including its identification, associated category,
    points per dollar, and effective dates.

    Attributes:
        id (int): The unique identifier for the point earning rule.
        category (Category): The category associated with this rule.
        category_id (int): The identifier of the category associated
            with this rule.
        points_per_dollar (int): The number of points earned per dollar spent.
        start_date (date): The date when the rule becomes effective.
        end_date (Optional[date]): The date when the rule expires,
            if applicable.
    """

    def __init__(
        self,
        id: int,
        category: Category,
        category_id: int,
        points_per_dollar: int,
        start_date: date,
        end_date: Optional[date] = None
    ):
        """
        Initializes a new PointEarningRule instance.

        Args:
            id (int): The unique identifier for the point earning rule.
            category (Category): The category associated with this rule.
            category_id (int): The identifier of the category associated
                with this rule.
            points_per_dollar (int): The number of points earned per dollar
                spent.
            start_date (date): The date when the rule becomes effective.
            end_date (Optional[date], optional): The date when the rule
                expires, if applicable. Defaults to None.
        """
        self.id: int = id
        self.category: Category = category
        self.category_id: int = category_id
        self.points_per_dollar: int = points_per_dollar
        self.start_date: date = start_date
        self.end_date: Optional[date] = end_date

    def is_active(self, current_date: date) -> bool:
        """
        Checks if the rule is active on the given date.

        Args:
            current_date (date): The date to check against.

        Returns:
            bool: True if the rule is active on the given date, False
            otherwise.
        """
        return (self.start_date <= current_date and
                (self.end_date is None or current_date <= self.end_date))
