# app/schemas/shopping_cart.py
from pydantic import BaseModel
from typing import List
from .product import ProductResponseDto


class ShoppingCartItemDto(BaseModel):
    """
    Data Transfer Object for an item in a shopping cart.

    Attributes:
        product (ProductResponseDto): The product details.
        quantity (int): The quantity of the product in the cart.
    """
    product: ProductResponseDto
    quantity: int


class ShoppingCartResponseDto(BaseModel):
    """
    Data Transfer Object for a shopping cart.

    Attributes:
        id (int): The unique identifier of the shopping cart.
        customer_id (int): The identifier of the customer owning the cart.
        items (List[ShoppingCartItemDto]): List of items in the shopping cart.
    """
    id: int
    customer_id: int
    items: List[ShoppingCartItemDto]


class AddToCartDto(BaseModel):
    """
    Data Transfer Object for adding a product to a shopping cart.

    Attributes:
        product_id (int): The identifier of the product to add.
        quantity (int): The quantity of the product to add.
    """
    product_id: int
    quantity: int


class UpdateCartItemDto(BaseModel):
    """
    Data Transfer Object for updating the quantity of an item
    in the shopping cart.

    Attributes:
        quantity (int): The updated quantity of the item.
    """
    quantity: int
