# app/models/domain/customer.py
from typing import Optional, List
from app.models.domain.loyalty_account import LoyaltyAccount
from app.models.domain.shopping_cart import ShoppingCart


class Customer:
    """
    Represents a customer in the domain model.

    This class encapsulates the core attributes and relationships
    of a customer, including their identification, contact information,
    loyalty account, and shopping carts.

    Attributes:
        id (int): The unique identifier for the customer.
        name (str): The name of the customer.
        email (str): The email address of the customer.
        loyalty_account (Optional['LoyaltyAccount']): The loyalty account
            associated with the customer, if any.
        shopping_carts (List['ShoppingCart']): A list of shopping carts
            associated with the customer.
    """

    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        loyalty_account: Optional['LoyaltyAccount'] = None,
        shopping_carts: Optional[List['ShoppingCart']] = None
    ) -> None:
        """
        Initializes a new Customer instance.

        Args:
            id (int): The unique identifier for the customer.
            name (str): The name of the customer.
            email (str): The email address of the customer.
            loyalty_account (Optional['LoyaltyAccount'], optional): The loyalty
                account associated with the customer. Defaults to None.
            shopping_carts (Optional[List['ShoppingCart']], optional): A list
                of shopping carts associated with the customer.
                Defaults to None.
        """
        self.id: int = id
        self.name: str = name
        self.email: str = email
        self.loyalty_account: Optional['LoyaltyAccount'] = loyalty_account
        self.shopping_carts: List['ShoppingCart'] = shopping_carts or []
