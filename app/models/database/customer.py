# app/models/database/customer.py
from __future__ import annotations
from app import db
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.database.loyalty_account import LoyaltyAccountTable
from app.models.database.shopping_cart import ShoppingCartTable


class CustomerTable(db.Model):
    """
    Represents a customer in the database.

    This model defines the structure of the 'customers' table in the database,
    including fields for customer identification, contact information, and
    timestamps for record creation and updates.

    Attributes:
        id (int): The primary key of the customer record.
        name (str): The name of the customer, limited to 100 characters.
        email (str): The unique email address of the customer, limited to
            120 characters.
        created_at (datetime): The timestamp when the customer record
            was created.
        updated_at (datetime): The timestamp when the customer record
            was last updated.
        loyalty_account (Optional[LoyaltyAccountTable]): The loyalty account
            associated with this customer, if any.
        shopping_carts (List[ShoppingCartTable]): The shopping carts
            associated with this customer.
    """

    __tablename__: str = 'customers'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    email: Mapped[str] = db.Column(db.String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    loyalty_account: Mapped[Optional[LoyaltyAccountTable]] = relationship(
        'LoyaltyAccountTable', back_populates='customer', uselist=False)
    shopping_carts: Mapped[List[ShoppingCartTable]] = relationship(
        'ShoppingCartTable', back_populates='customer')
