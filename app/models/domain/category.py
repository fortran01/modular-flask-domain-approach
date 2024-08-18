# app/models/domain/category.py
from typing import List
from app.models.domain.product import Product
from app.models.domain.point_earning_rule import PointEarningRule


class Category:
    """
    Represents a category in the domain model.

    This class encapsulates the core attributes and relationships
    of a category, including its identification, name, associated products,
    and point earning rules.

    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category.
        products (List[Product]): The list of products associated
            with this category.
        point_earning_rules (List[PointEarningRule]): The list of point
            earning rules associated with this category.
    """

    def __init__(
        self,
        id: int,
        name: str,
        products: List[Product] = None,
        point_earning_rules: List[PointEarningRule] = None
    ):
        """
        Initializes a new Category instance.

        Args:
            id (int): The unique identifier for the category.
            name (str): The name of the category.
            products (List[Product], optional): The list of products associated
                with this category. Defaults to None.
            point_earning_rules (List[PointEarningRule], optional): The list of
                point earning rules associated with this category.
                Defaults to None.
        """
        self.id: int = id
        self.name: str = name
        self.products: List[Product] = products or []
        self.point_earning_rules: List[PointEarningRule] = (
            point_earning_rules or []
        )
