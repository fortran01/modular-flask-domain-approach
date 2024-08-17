# app/schemas/point_transaction.py
from pydantic import BaseModel
from datetime import datetime


class PointTransactionResponseDto(BaseModel):
    """
    Data Transfer Object for responding with point transaction information.

    Attributes:
        id (int): The unique identifier of the point transaction.
        loyalty_account_id (int): The identifier of the loyalty account
            associated with this transaction.
        product_id (int): The identifier of the product involved
        in this transaction.
        points_earned (int): The number of points earned in this transaction.
        transaction_date (datetime): The date and time
        when the transaction occurred.
    """
    id: int
    loyalty_account_id: int
    product_id: int
    points_earned: int
    transaction_date: datetime
