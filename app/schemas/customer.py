# app/schemas/customer.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .loyalty_account import LoyaltyAccountResponseDto
from .shopping_cart import ShoppingCartResponseDto


class CustomerCreateDto(BaseModel):
    """
    Data Transfer Object for creating a new customer.

    Attributes:
        name (str): The name of the customer.
        email (EmailStr): The email address of the customer.
    """
    name: str
    email: EmailStr


class CustomerUpdateDto(BaseModel):
    """
    Data Transfer Object for updating an existing customer.

    Attributes:
        name (Optional[str]): The updated name of the customer, if provided.
        email (Optional[EmailStr]): The updated email address of the customer,
            if provided.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerResponseDto(BaseModel):
    """
    Data Transfer Object for responding with customer information.

    Attributes:
        id (int): The unique identifier of the customer.
        name (str): The name of the customer.
        email (EmailStr): The email address of the customer.
        loyalty_account (Optional[LoyaltyAccountResponseDto]): The loyalty
            account associated with the customer, if any.
        shopping_carts (List[ShoppingCartResponseDto]): A list of shopping
            carts associated with the customer.
    """
    id: int
    name: str
    email: EmailStr
    loyalty_account: Optional[LoyaltyAccountResponseDto] = None
    shopping_carts: List[ShoppingCartResponseDto] = []
