# app/services/shopping_cart_service.py
from typing import Optional
from app.repositories.shopping_cart_repository import ShoppingCartRepository
from app.repositories.product_repository import ProductRepository
from app.models.database.shopping_cart import ShoppingCartTable
from app.schemas.shopping_cart import (
    ShoppingCartResponseDto,
    ShoppingCartItemDto
)
from app.schemas.product import ProductResponseDto


class ShoppingCartService:
    def __init__(
        self,
        shopping_cart_repository: ShoppingCartRepository,
        product_repository: ProductRepository
    ):
        """
        Initializes the ShoppingCartService with required repositories.

        Args:
            shopping_cart_repository (ShoppingCartRepository): Repository for
                shopping cart operations.
            product_repository (ProductRepository): Repository for
            product data.
        """
        self.shopping_cart_repository = shopping_cart_repository
        self.product_repository = product_repository

    async def get_or_create_cart(self, customer_id: int) -> ShoppingCartTable:
        """
        Retrieves an existing shopping cart or creates a new one if it does not
        exist.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            ShoppingCartTable: The retrieved or newly created shopping cart.
        """
        cart = self.shopping_cart_repository.find_by_customer_id(customer_id)
        if not cart:
            cart = ShoppingCartTable(customer_id=customer_id)
            cart = self.shopping_cart_repository.create(cart)
        return cart

    async def add_item(
        self, customer_id: int, product_id: int, quantity: int
    ) -> None:
        """
        Adds an item to the shopping cart.

        Args:
            customer_id (int): The ID of the customer.
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add.
        """
        cart = await self.get_or_create_cart(customer_id)
        self.shopping_cart_repository.add_item(cart.id, product_id, quantity)

    async def remove_item(self, customer_id: int, product_id: int) -> None:
        """
        Removes an item from the shopping cart.

        Args:
            customer_id (int): The ID of the customer.
            product_id (int): The ID of the product to remove.
        """
        cart = await self.get_or_create_cart(customer_id)
        self.shopping_cart_repository.remove_item(cart.id, product_id)

    async def update_item_quantity(
        self, customer_id: int, product_id: int, quantity: int
    ) -> None:
        """
        Updates the quantity of an item in the shopping cart.

        Args:
            customer_id (int): The ID of the customer.
            product_id (int): The ID of the product to update.
            quantity (int): The new quantity of the product.
        """
        cart = await self.get_or_create_cart(customer_id)
        self.shopping_cart_repository.update_item_quantity(
            cart.id, product_id, quantity)

    async def get_cart(
        self, customer_id: int
    ) -> Optional[ShoppingCartResponseDto]:
        """
        Retrieves the shopping cart for a specified customer.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            Optional[ShoppingCartResponseDto]: The shopping cart data or None
                if the cart does not exist.
        """
        cart = self.shopping_cart_repository.find_by_customer_id(customer_id)
        if not cart:
            return None

        items = []
        for item in cart.items:
            product = self.product_repository.find_by_id(item.product_id)
            if product:
                items.append(ShoppingCartItemDto(
                    product=ProductResponseDto(
                        id=product.id,
                        name=product.name,
                        price=product.price,
                        category_id=product.category_id,
                        image_url=product.image_url
                    ),
                    quantity=item.quantity
                ))

        return ShoppingCartResponseDto(
            id=cart.id,
            customer_id=cart.customer_id,
            items=items
        )

    async def clear_cart(self, customer_id: int) -> None:
        """
        Clears all items from a customer's shopping cart.

        Args:
            customer_id (int): The ID of the customer.
        """
        cart = await self.get_or_create_cart(customer_id)
        self.shopping_cart_repository.clear_cart(cart.id)
