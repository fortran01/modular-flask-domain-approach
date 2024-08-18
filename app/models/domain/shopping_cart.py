# app/models/domain/shopping_cart.py
from typing import List, Optional
from app.models.domain.product import Product


class ShoppingCart:
    """
    Represents a shopping cart in the domain model.

    This class encapsulates the core attributes and behaviors
    of a shopping cart, including its identification, associated customer,
    and items.

    Attributes:
        id (int): The unique identifier for the shopping cart.
        customer_id (int): The identifier of the customer associated
            with this cart.
        items (List['ShoppingCartItem']): A list of items in the shopping cart.
    """

    def __init__(
        self,
        id: int,
        customer_id: int,
        items: Optional[List['ShoppingCartItem']] = None
    ) -> None:
        """
        Initializes a new ShoppingCart instance.

        Args:
            id (int): The unique identifier for the shopping cart.
            customer_id (int): The identifier of the customer associated
              with this cart.
            items (Optional[List['ShoppingCartItem']], optional): A list of
                items in the shopping cart. Defaults to None.
        """
        self.id: int = id
        self.customer_id: int = customer_id
        self.items: List['ShoppingCartItem'] = items or []

    def add_item(self, product: 'Product', quantity: int) -> None:
        """
        Adds an item to the shopping cart or updates its quantity
        if it already exists.

        Args:
            product (Product): The product to add to the cart.
            quantity (int): The quantity of the product to add.
        """
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += quantity
                return
        self.items.append(ShoppingCartItem(product=product, quantity=quantity))

    def remove_item(self, product_id: int) -> None:
        """
        Removes an item from the shopping cart based on the product ID.

        Args:
            product_id (int): The ID of the product to remove from the cart.
        """
        self.items = [
            item for item in self.items if item.product.id != product_id]

    def update_item_quantity(self, product_id: int, quantity: int) -> None:
        """
        Updates the quantity of an item in the shopping cart.

        Args:
            product_id (int): The ID of the product to update.
            quantity (int): The new quantity for the product.
        """
        for item in self.items:
            if item.product.id == product_id:
                item.quantity = quantity
                return

    def clear(self) -> None:
        """
        Removes all items from the shopping cart.
        """
        self.items.clear()


class ShoppingCartItem:
    """
    Represents an item in a shopping cart.

    This class encapsulates a product and its quantity in the context
    of a shopping cart.

    Attributes:
        product (Product): The product associated with this cart item.
        quantity (int): The quantity of the product in the cart.
    """

    def __init__(self, product: 'Product', quantity: int) -> None:
        """
        Initializes a new ShoppingCartItem instance.

        Args:
            product (Product): The product to add to the cart.
            quantity (int): The quantity of the product.
        """
        self.product: 'Product' = product
        self.quantity: int = quantity
