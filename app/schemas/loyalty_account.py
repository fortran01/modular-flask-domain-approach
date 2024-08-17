# app/schemas/loyalty_account.py
from pydantic import BaseModel


class LoyaltyAccountResponseDto(BaseModel):
    """
    Data Transfer Object for responding with loyalty account information.

    Attributes:
        id (int): The unique identifier of the loyalty account.
        customer_id (int): The identifier of the customer associated
            with this loyalty account.
        points (int): The current number of loyalty points in the account.
    """
    id: int
    customer_id: int
    points: int
