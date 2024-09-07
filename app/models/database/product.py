# app/models/database/product.py
from __future__ import annotations
from app import db
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped
if TYPE_CHECKING:
    from app.models.database.category import CategoryTable
    from app.models.database.point_transaction import PointTransactionTable


class ProductTable(db.Model):
    """
    Represents a product in the database.

    This model defines the structure of the 'products' table in the database,
    including fields for product identification, name, price, category,
    and timestamps for record creation and updates.

    Attributes:
        id (int): The primary key of the product record.
        name (str): The name of the product, limited to 100 characters.
        price (float): The price of the product.
        category_id (int): The foreign key referencing the associated
          category's id.
        created_at (datetime): The timestamp when the product record was
            created.
        updated_at (datetime): The timestamp when the product record was last
            updated.
        category (CategoryTable): The category associated with this product.
        transactions (List[PointTransactionTable]): The point transactions
            associated with this product.
    """

    __tablename__: str = 'products'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    price: Mapped[float] = db.Column(db.Float, nullable=False)
    image_url: Mapped[str] = db.Column(db.String(255), nullable=True)
    category_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    created_at: Mapped[datetime] = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    category: Mapped["CategoryTable"] = db.relationship(
        "CategoryTable", back_populates='products')
    transactions: Mapped[List["PointTransactionTable"]] = db.relationship(
        "PointTransactionTable", back_populates='product')
