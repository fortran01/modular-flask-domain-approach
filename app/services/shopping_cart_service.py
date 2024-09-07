# app/services/shopping_cart_service.py
from typing import Optional
from app.repositories.shopping_cart_repository import ShoppingCartRepository
from app.repositories.product_repository import ProductRepository
from app.models.domain.shopping_cart import ShoppingCart
from app.schemas.shopping_cart import (
    ShoppingCartResponseDto,
    ShoppingCartItemDto
)
from app.schemas.product import ProductResponseDto
from app.mappers.shopping_cart_mapper import ShoppingCartMapper
import logging

logger = logging.getLogger(__name__)


class ShoppingCartService:
    def __init__(
        self,
        shopping_cart_repository: ShoppingCartRepository,
        product_repository: ProductRepository
    ) -> None:
        """
        Initializes the ShoppingCartService with required repositories.

        Args:
            shopping_cart_repository (ShoppingCartRepository): Repository for
                shopping cart operations.
            product_repository (ProductRepository): Repository for
                product data.
        """
        self.shopping_cart_repository: ShoppingCartRepository = \
            shopping_cart_repository
        self.product_repository: ProductRepository = product_repository

    def get_or_create_cart(self, customer_id: int) -> ShoppingCart:
        """
        Retrieves an existing shopping cart or creates a new one if it does not
        exist.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            ShoppingCart: The retrieved or newly created shopping cart.
        """
        cart: Optional[ShoppingCart] = \
            self.shopping_cart_repository.find_by_customer_id(customer_id)
        if not cart:
            cart = ShoppingCart(id=0, customer_id=customer_id)
            cart = ShoppingCartMapper.to_persistence_model(cart)
            cart = self.shopping_cart_repository.create(cart)

        cart = ShoppingCartMapper.from_persistence(cart)
        return cart

    def add_item(
        self, customer_id: int, product_id: int, quantity: int
    ) -> None:
        """
        Adds an item to the shopping cart.

        Args:
            customer_id (int): The ID of the customer.
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add.
        """
        cart: ShoppingCart = self.get_or_create_cart(customer_id)
        product: Optional[ProductResponseDto] = \
            self.product_repository.find_by_id(product_id)
        if product:
            cart.add_item(product, quantity)
            cart = ShoppingCartMapper.to_persistence_model(cart)
            self.shopping_cart_repository.update(cart)

    def remove_item(self, customer_id: int, product_id: int) -> None:
        """
        Removes an item from the shopping cart.

        Args:
            customer_id (int): The ID of the customer.
            product_id (int): The ID of the product to remove.
        """
        cart: ShoppingCart = self.get_or_create_cart(customer_id)
        cart.remove_item(product_id)
        cart = ShoppingCartMapper.to_persistence_model(cart)
        self.shopping_cart_repository.update(cart)

    def update_item_quantity(
        self, customer_id: int, product_id: int, quantity: int
    ) -> None:
        """
        Updates the quantity of an item in the shopping cart.

        Args:
            customer_id (int): The ID of the customer.
            product_id (int): The ID of the product to update.
            quantity (int): The new quantity of the product.
        """
        cart: ShoppingCart = self.get_or_create_cart(customer_id)
        cart.update_item_quantity(product_id, quantity)
        cart = ShoppingCartMapper.to_persistence_model(cart)
        self.shopping_cart_repository.update(cart)

    def get_cart(
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
        cart: Optional[ShoppingCart] = \
            self.shopping_cart_repository.find_by_customer_id(customer_id)
        if not cart:
            return None

        items: list[ShoppingCartItemDto] = []
        for item in cart.items:
            product: ProductResponseDto = item.product
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

    def clear_cart(self, customer_id: int) -> None:
        """
        Clears all items from a customer's shopping cart.

        Args:
            customer_id (int): The ID of the customer.
        """
        cart: ShoppingCart = self.get_or_create_cart(customer_id)
        cart.clear()
        self.shopping_cart_repository.update(
            ShoppingCartMapper.to_persistence_model(cart)
        )
        logger.debug(f"Cleared cart for customer {customer_id}")
