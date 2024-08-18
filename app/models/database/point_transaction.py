# app/models/database/point_transaction.py
from __future__ import annotations
from typing import TYPE_CHECKING
from app import db
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.database.loyalty_account import LoyaltyAccountTable
    from app.models.database.product import ProductTable


class PointTransactionTable(db.Model):
    """
    Represents a point transaction in the database.

    This model defines the structure of the 'point_transactions' table
    in the database, including fields for transaction identification,
    associated loyalty account and product, points earned, and the
    transaction date.

    Attributes:
        id (int): The primary key of the point transaction record.
        loyalty_account_id (int): The foreign key referencing the associated
            loyalty account's id.
        product_id (int): The foreign key referencing the associated
            product's id.
        points_earned (int): The number of points earned in this transaction.
        transaction_date (datetime): The timestamp when
            the transaction occurred.
        loyalty_account (LoyaltyAccountTable): The loyalty account associated
        with this transaction.
        product (ProductTable): The product associated with this transaction.
    """

    __tablename__: str = 'point_transactions'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    loyalty_account_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'loyalty_accounts.id'), nullable=False)
    product_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    points_earned: Mapped[int] = db.Column(db.Integer, nullable=False)
    transaction_date: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow)

    # Relationships
    loyalty_account: Mapped["LoyaltyAccountTable"] = relationship(
        "LoyaltyAccountTable", back_populates="transactions")
    product: Mapped["ProductTable"] = relationship(
        "ProductTable", back_populates="transactions")
