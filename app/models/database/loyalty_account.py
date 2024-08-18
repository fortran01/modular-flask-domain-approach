# app/models/database/loyalty_account.py
from __future__ import annotations
from app import db
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.database.customer import CustomerTable
    from app.models.database.point_transaction import PointTransactionTable


class LoyaltyAccountTable(db.Model):
    """
    Represents a loyalty account in the database.

    This model defines the structure of the 'loyalty_accounts' table in the
    database, including fields for account identification, associated customer,
    points balance, and timestamps for record creation and updates.

    Attributes:
        id (int): The primary key of the loyalty account record.
        customer_id (int): The foreign key referencing the associated
            customer's id.
        points (int): The current balance of loyalty points for this account.
        created_at (datetime): The timestamp when the loyalty account record
            was created.
        updated_at (datetime): The timestamp when the loyalty account record
            was last updated.
        customer (CustomerTable): The customer associated with
        this loyalty account.
        transactions (List[PointTransactionTable]): The list of point
            transactions associated with this loyalty account.
    """

    __tablename__: str = 'loyalty_accounts'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    customer_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey('customers.id'), nullable=False)
    points: Mapped[int] = db.Column(db.Integer, default=0)
    created_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer: Mapped["CustomerTable"] = relationship(
        "CustomerTable", back_populates="loyalty_account", uselist=False)
    transactions: Mapped[List["PointTransactionTable"]] = relationship(
        "PointTransactionTable", back_populates="loyalty_account")
