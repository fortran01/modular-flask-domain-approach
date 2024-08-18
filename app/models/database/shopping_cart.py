# app/models/database/shopping_cart.py
from __future__ import annotations
from typing import TYPE_CHECKING, List
from app import db
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.database.customer import CustomerTable
    from app.models.database.product import ProductTable


class ShoppingCartTable(db.Model):
    """
    Represents a shopping cart in the database.

    This model defines the structure of the 'shopping_carts' table in the
    database, including fields for cart identification, associated customer,
    and timestamps for record creation and updates.

    Attributes:
        id (int): The primary key of the shopping cart record.
        customer_id (int): The foreign key referencing the associated
            customer's id.
        created_at (datetime): The timestamp when the shopping cart record
            was created.
        updated_at (datetime): The timestamp when the shopping cart record
            was last updated.
        customer (CustomerTable): The customer associated with this
            shopping cart.
        items (List[ShoppingCartItemTable]): The items in this shopping cart.
    """

    __tablename__: str = 'shopping_carts'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    created_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer: Mapped["CustomerTable"] = relationship(
        "CustomerTable", back_populates="shopping_carts")
    items: Mapped[List['ShoppingCartItemTable']] = relationship(
        'ShoppingCartItemTable',
        back_populates='cart',
        cascade='all, delete-orphan'
    )


class ShoppingCartItemTable(db.Model):
    """
    Represents an item in a shopping cart in the database.

    This model defines the structure of the 'shopping_cart_items' table in the
    database, including fields for item identification, associated cart
    and product, and quantity.

    Attributes:
        id (int): The primary key of the shopping cart item record.
        cart_id (int): The foreign key referencing the associated
            shopping cart's id.
        product_id (int): The foreign key referencing the associated
            product's id.
        quantity (int): The quantity of the product in the shopping cart.
        cart (ShoppingCartTable): The shopping cart associated with this item.
        product (ProductTable): The product associated with this item.
    """

    __tablename__: str = 'shopping_cart_items'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    cart_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'shopping_carts.id'), nullable=False)
    product_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    quantity: Mapped[int] = db.Column(db.Integer, nullable=False)

    # Relationships
    cart: Mapped[ShoppingCartTable] = relationship(
        'ShoppingCartTable', back_populates='items')
    product: Mapped['ProductTable'] = relationship('ProductTable')
