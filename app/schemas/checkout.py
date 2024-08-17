# app/schemas/checkout.py
from pydantic import BaseModel
from typing import List


class CheckoutResponseDto(BaseModel):
    """
    Data Transfer Object for the response of a checkout operation.

    Attributes:
        total_points_earned (int): Total loyalty points earned in this
            transaction.
        invalid_products (List[int]): List of product IDs that were invalid
            during the checkout process.
        products_missing_category (List[int]): List of product IDs missing
            a category assignment.
        point_earning_rules_missing (List[int]): List of product IDs for which
            point earning rules were missing.
        success (bool): Flag indicating if the checkout process was successful.
    """
    total_points_earned: int
    invalid_products: List[int]
    products_missing_category: List[int]
    point_earning_rules_missing: List[int]
    success: bool
