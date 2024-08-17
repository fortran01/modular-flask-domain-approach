# app/schemas/point_earning_rule.py
from pydantic import BaseModel
from datetime import date
from typing import Optional


class PointEarningRuleCreateDto(BaseModel):
    """
    Data Transfer Object for creating a point earning rule.

    Attributes:
        category_id (int): The identifier of the category this rule applies to.
        points_per_dollar (int): The number of points earned per dollar spent.
        start_date (date): The start date from which the rule is applicable.
        end_date (Optional[date]): The optional end date until which the rule
            is applicable.
    """
    category_id: int
    points_per_dollar: int
    start_date: date
    end_date: Optional[date] = None


class PointEarningRuleResponseDto(BaseModel):
    """
    Data Transfer Object for responding with point earning rule information.

    Attributes:
        id (int): The unique identifier of the point earning rule.
        category_id (int): The identifier of the category this rule applies to.
        points_per_dollar (int): The number of points earned per dollar spent.
        start_date (date): The start date from which the rule is applicable.
        end_date (Optional[date]): The optional end date until which the rule
            is applicable.
    """
    id: int
    category_id: int
    points_per_dollar: int
    start_date: date
    end_date: Optional[date] = None
