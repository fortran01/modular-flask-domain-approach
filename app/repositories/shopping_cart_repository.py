# app/repositories/shopping_cart_repository.py
from typing import Optional
from app.repositories.base_repository import BaseRepository
from app.models.database.shopping_cart import (
    ShoppingCartTable,
    ShoppingCartItemTable,
)
from app.models.domain.shopping_cart import ShoppingCart
from app.mappers.shopping_cart_mapper import ShoppingCartMapper
from app import db


class ShoppingCartRepository(BaseRepository[ShoppingCartTable]):
    def __init__(self):
        """
        Initializes the ShoppingCartRepository with the
        ShoppingCartTable model.
        """
        super().__init__(ShoppingCartTable)

    def find_by_customer_id(self, customer_id: int) -> Optional[ShoppingCart]:
        """
        Retrieves a shopping cart by the customer ID.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            Optional[ShoppingCart]: The found shopping cart
            or None if not found.
        """
        cart_table = db.session.query(ShoppingCartTable).filter(
            ShoppingCartTable.customer_id == customer_id).first()
        return (
            ShoppingCartMapper.from_persistence(cart_table)
            if cart_table
            else None
        )

    def save(self, cart: ShoppingCart) -> ShoppingCart:
        """
        Saves a shopping cart to the database.

        Args:
            cart (ShoppingCart): The ShoppingCart object to save.

        Returns:
            ShoppingCart: The saved ShoppingCart object.
        """
        cart_table = ShoppingCartMapper.to_persistence(cart)
        if cart.id:
            saved_cart = super().update(cart_table)
        else:
            saved_cart = super().create(cart_table)
        return ShoppingCartMapper.to_domain(saved_cart)

    def add_item(self, cart_id: int, product_id: int, quantity: int) -> None:
        """
        Adds an item to the shopping cart or updates its quantity
        if it already exists.

        Args:
            cart_id (int): The ID of the cart.
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add.
        """
        cart_item = db.session.query(ShoppingCartItemTable).filter(
            ShoppingCartItemTable.cart_id == cart_id,
            ShoppingCartItemTable.product_id == product_id
        ).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = ShoppingCartItemTable(
                cart_id=cart_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()

    def remove_item(self, cart_id: int, product_id: int) -> None:
        """
        Removes an item from the shopping cart.

        Args:
            cart_id (int): The ID of the cart.
            product_id (int): The ID of the product to remove.
        """
        db.session.query(ShoppingCartItemTable).filter(
            ShoppingCartItemTable.cart_id == cart_id,
            ShoppingCartItemTable.product_id == product_id
        ).delete()
        db.session.commit()

    def update_item_quantity(
        self, cart_id: int, product_id: int, quantity: int
    ) -> None:
        """
        Updates the quantity of an item in the shopping cart.

        Args:
            cart_id (int): The ID of the cart.
            product_id (int): The ID of the product to update.
            quantity (int): The new quantity of the product.
        """
        cart_item = db.session.query(ShoppingCartItemTable).filter(
            ShoppingCartItemTable.cart_id == cart_id,
            ShoppingCartItemTable.product_id == product_id
        ).first()

        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()

    def clear_cart(self, cart_id: int) -> None:
        """
        Clears all items from the shopping cart.

        Args:
            cart_id (int): The ID of the cart to clear.
        """
        db.session.query(ShoppingCartItemTable).filter(
            ShoppingCartItemTable.cart_id == cart_id).delete()
        db.session.commit()

    def get_cart_with_items(self, cart_id: int) -> Optional[ShoppingCart]:
        """
        Retrieves a shopping cart along with its items.

        Args:
            cart_id (int): The ID of the cart.

        Returns:
            Optional[ShoppingCart]: The shopping cart with items
            or None if not found.
        """
        cart_table = db.session.query(ShoppingCartTable).filter(
            ShoppingCartTable.id == cart_id).options(
            db.joinedload(ShoppingCartTable.items).joinedload(
                ShoppingCartItemTable.product)
        ).first()
        return ShoppingCartMapper.to_domain(cart_table) if cart_table else None
